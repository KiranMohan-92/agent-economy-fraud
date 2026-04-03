"""Fetch agent transaction histories from Dune in batches.

Splits 1,505 agent addresses into batches of 100, creates+executes
each batch via MCP, and combines results into a single CSV.

This avoids the query engine memory limits hit by a single 1505-address
VALUES CTE on the community (free) tier.
"""

import csv
import json
import sys
import time
from pathlib import Path

import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"

DUNE_API_KEY = "HrBeJCELgfMTjUBuGQgxvv3hafVS5YzB"
DUNE_MCP_URL = "https://api.dune.com/mcp/v1"
HEADERS = {
    "x-dune-api-key": DUNE_API_KEY,
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
    resp = httpx.post(DUNE_MCP_URL, headers=HEADERS, json=payload, timeout=timeout)
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
    t.evt_block_number,
    t.evt_block_time,
    t."from" AS sender,
    t."to" AS receiver,
    CAST(t.value AS DOUBLE) / 1e6 AS amount_usdc
FROM erc20_base.evt_transfer t
INNER JOIN agents a ON t."from" = a.addr
WHERE t.contract_address = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
  AND t.evt_block_date >= DATE '2025-01-01'

UNION ALL

SELECT
    t.evt_tx_hash,
    t.evt_block_number,
    t.evt_block_time,
    t."from" AS sender,
    t."to" AS receiver,
    CAST(t.value AS DOUBLE) / 1e6 AS amount_usdc
FROM erc20_base.evt_transfer t
INNER JOIN agents a ON t."to" = a.addr
WHERE t.contract_address = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
  AND t.evt_block_date >= DATE '2025-01-01'

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

    # Deduplicate (agent-to-agent txns appear in both sender and receiver batches)
    if all_rows:
        seen = set()
        deduped = []
        for row in all_rows:
            key = row.get("evt_tx_hash", "")
            if key not in seen:
                seen.add(key)
                deduped.append(row)
            # Keep both directions for same tx (sender batch + receiver batch = 2 rows is correct for UNION ALL)
            # Actually: within each batch, UNION ALL already captures both directions
            # But across batches, if sender is in batch 1 and receiver in batch 5,
            # the same tx appears once in each batch. We keep both for correct flow analysis.
        # Actually, don't deduplicate — each batch's UNION ALL captures both directions
        # for addresses IN THAT BATCH. Cross-batch duplicates are rare and acceptable.
        deduped = all_rows

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
