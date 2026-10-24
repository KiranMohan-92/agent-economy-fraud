"""Fetch agent transaction histories from Dune in batches.

Splits the 1,505 ERC-8004 registry-associated addresses into batches of 100,
creates+executes each batch via MCP, and combines results into a single CSV.
Each row carries ``evt_index`` so the bridge can key events on
``(tx_hash, evt_index)``; the run fails closed if any row lacks it.

Note: the output path is the same ``data/dune_agent_transactions.csv`` that
``data/MANIFEST.md`` records as the superseded forensic extraction. Copy that
file aside (its SHA-256 is in the manifest) before re-running, and treat any
new extraction as a new data version.

This avoids the query engine memory limits hit by a single 1505-address
VALUES CTE on the community (free) tier.
"""

import csv
import json
import os
import sys
import time
from pathlib import Path

import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"

DUNE_MCP_URL = "https://api.dune.com/mcp/v1"


def _dune_headers() -> dict[str, str]:
    """Build authenticated headers without shipping a credential fallback."""
    api_key = os.environ.get("DUNE_API_KEY")
    if not api_key:
        raise RuntimeError("DUNE_API_KEY is required; set it in the environment")
    return {
        "x-dune-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

BATCH_SIZE = 100
POLL_INTERVAL = 10
MAX_WAIT = 600


def mcp_call(tool, args, timeout=120):
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": tool, "arguments": args},
        "id": 1,
    }
    resp = httpx.post(DUNE_MCP_URL, headers=_dune_headers(), json=payload, timeout=timeout)
    resp.raise_for_status()
    for line in resp.text.splitlines():
        if not line.startswith("data:"):
            continue
        try:
            data = json.loads(line[5:].strip())
        except json.JSONDecodeError:
            continue
        result = data.get("result", {})
        s = result.get("structuredContent")
        if s:
            return s
        for item in result.get("content", []):
            if item.get("type") == "text":
                try:
                    return json.loads(item["text"])
                except (json.JSONDecodeError, TypeError):
                    return {"text": item["text"]}
    raise RuntimeError("No valid MCP response")


def build_batch_sql(addresses: list[str]) -> str:
    values = ",\n    ".join([f"(0x{a[2:]})" for a in addresses])
    return f"""WITH agents(addr) AS (
  VALUES
    {values}
)
SELECT
    t.evt_tx_hash,
    t.evt_index,
    t.evt_block_number,
    t.evt_block_time,
    t."from" AS sender,
    t."to" AS receiver,
    CAST(t.value AS DOUBLE) / 1e6 AS amount_usdc
FROM erc20_base.evt_transfer t
INNER JOIN agents a ON t."from" = a.addr
WHERE t.contract_address = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
  AND t.evt_block_date >= DATE '2025-01-01'
  AND t.evt_block_date < DATE '2026-04-04'

UNION ALL

SELECT
    t.evt_tx_hash,
    t.evt_index,
    t.evt_block_number,
    t.evt_block_time,
    t."from" AS sender,
    t."to" AS receiver,
    CAST(t.value AS DOUBLE) / 1e6 AS amount_usdc
FROM erc20_base.evt_transfer t
INNER JOIN agents a ON t."to" = a.addr
WHERE t.contract_address = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
  AND t.evt_block_date >= DATE '2025-01-01'
  AND t.evt_block_date < DATE '2026-04-04'

ORDER BY evt_block_time ASC"""


def run_batch(batch_num: int, addresses: list[str]) -> list[dict]:
    """Create, execute, and download results for one batch."""
    sql = build_batch_sql(addresses)

    # Create query
    r = mcp_call("createDuneQuery", {
        "name": f"A2A batch {batch_num}: {len(addresses)} agents",
        "query": sql,
        "is_private": True,
        "is_temp": True,
    })
    query_id = r.get("query_id")
    print(f"  Batch {batch_num}: created query {query_id}", flush=True)

    # Execute
    r = mcp_call("executeQueryById", {"query_id": query_id})
    execution_id = r.get("execution_id")
    print(f"  Batch {batch_num}: executing {execution_id}", flush=True)

    # Poll for completion
    elapsed = 0
    while elapsed < MAX_WAIT:
        try:
            r = mcp_call("getExecutionResults", {
                "executionId": execution_id, "limit": 0, "offset": 0, "timeout": 0,
            }, timeout=30)
            state = r.get("state", "")
        except Exception as e:
            print(f"  Batch {batch_num}: poll error ({e}), retrying...", flush=True)
            time.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL
            continue

        if state == "COMPLETED":
            total = r.get("resultMetadata", {}).get("totalRowCount", 0)
            cost = r.get("resultMetadata", {}).get("executionCostCredits", "?")
            print(f"  Batch {batch_num}: COMPLETED ({total} rows, {cost} credits)", flush=True)
            break
        elif state in ("FAILED", "CANCELLED", "EXPIRED"):
            msg = r.get("errorMessage", "unknown")
            print(f"  Batch {batch_num}: {state} — {msg}", flush=True)
            return []

        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL

    if elapsed >= MAX_WAIT:
        print(f"  Batch {batch_num}: TIMEOUT after {MAX_WAIT}s", flush=True)
        return []

    # Download all rows
    all_rows = []
    offset = 0
    while True:
        r = mcp_call("getExecutionResults", {
            "executionId": execution_id, "limit": 100, "offset": offset, "timeout": 0,
        }, timeout=60)
        rows = r.get("data", {}).get("rows", [])
        if not rows:
            break
        all_rows.extend(rows)
        offset += len(rows)

    return all_rows


def main():
    # Load addresses
    with open(DATA_DIR / "base_erc8004_agents.json") as f:
        data = json.load(f)
    addresses = data["addresses"]
    print(f"Total addresses: {len(addresses)}", flush=True)
    print(f"Batch size: {BATCH_SIZE}", flush=True)
    print(f"Total batches: {(len(addresses) + BATCH_SIZE - 1) // BATCH_SIZE}", flush=True)
    print(flush=True)

    # Process in batches
    all_rows = []
    total_batches = (len(addresses) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(0, len(addresses), BATCH_SIZE):
        batch_num = i // BATCH_SIZE + 1
        batch_addrs = addresses[i:i + BATCH_SIZE]
        print(f"=== Batch {batch_num}/{total_batches} ({len(batch_addrs)} addresses) ===", flush=True)

        rows = run_batch(batch_num, batch_addrs)
        all_rows.extend(rows)
        print(f"  Running total: {len(all_rows)} rows\n", flush=True)

    # No deduplication here: event identity is (tx_hash, evt_index), and the
    # bridge deduplicates on that key and fails closed if it is missing.
    missing_index = sum(1 for row in all_rows if row.get("evt_index") in (None, ""))
    if missing_index:
        raise RuntimeError(
            f"{missing_index} rows lack evt_index; refusing to write a CSV the "
            "bridge would reject (transaction hash alone is not an event key)"
        )

    # Write CSV
    output = DATA_DIR / "dune_agent_transactions.csv"
    if all_rows:
        keys = list(all_rows[0].keys())
        with open(output, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_rows)

    print(f"\n{'='*60}")
    print(f"COMPLETE: {len(all_rows)} total rows saved to {output}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
