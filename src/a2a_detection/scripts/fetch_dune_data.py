"""Fetch full agent transaction histories from Dune Analytics.

Creates a query with all 1,505 ERC-8004 agent addresses, executes it,
and downloads the complete result set as CSV. Uses real evt_block_time
timestamps to close verification gaps GAP-01 (Value Flow) and GAP-02
(Temporal Consistency).
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
QUERIES_DIR = PROJECT_ROOT / "queries"

DUNE_API_KEY = os.environ.get("DUNE_API_KEY", "HrBeJCELgfMTjUBuGQgxvv3hafVS5YzB")
DUNE_BASE = "https://api.dune.com/api/v1"
HEADERS = {"x-dune-api-key": DUNE_API_KEY}

POLL_INTERVAL = 5  # seconds
MAX_WAIT = 600  # 10 minutes

# Dune MCP endpoint (works on free/community plan for query creation)
DUNE_MCP_URL = "https://api.dune.com/mcp/v1"


def create_query_via_mcp(name: str, sql: str) -> int:
    """Create a Dune query via the MCP endpoint (works on free plan).

    The REST API v1 /query endpoint returns 403 on community plans,
    but the MCP endpoint accepts query creation with the same API key.
    Uses Streamable HTTP MCP transport (SSE response format).
    """
    import re

    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "createDuneQuery",
            "arguments": {
                "name": name,
                "query": sql,
                "is_private": True,
                "is_temp": True,
            },
        },
        "id": 1,
    }
    resp = httpx.post(
        DUNE_MCP_URL,
        headers={
            **HEADERS,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()

    # Parse SSE response: look for "data:" lines containing JSON
    for line in resp.text.splitlines():
        if not line.startswith("data:"):
            continue
        data_str = line[len("data:"):].strip()
        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            continue

        if "error" in data:
            print(f"MCP error: {data['error']}")
            sys.exit(1)

        # Extract query_id from structured content or text content
        result = data.get("result", {})
        structured = result.get("structuredContent", {})
        if "query_id" in structured:
            query_id = structured["query_id"]
            print(f"Created query {query_id}: {name}")
            return query_id

        # Fallback: parse from text content
        for item in result.get("content", []):
            if item.get("type") == "text":
                match = re.search(r'"query_id"\s*:\s*(\d+)', item["text"])
                if match:
                    query_id = int(match.group(1))
                    print(f"Created query {query_id}: {name}")
                    return query_id

    print(f"Could not parse query_id from MCP response: {resp.text[:500]}")
    sys.exit(1)


def _mcp_call(tool_name: str, arguments: dict, timeout: int = 120) -> dict:
    """Make an MCP tool call and return the parsed result."""
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
        "id": 1,
    }
    resp = httpx.post(
        DUNE_MCP_URL,
        headers={
            **HEADERS,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        json=payload,
        timeout=timeout,
    )
    resp.raise_for_status()

    # Parse SSE response
    for line in resp.text.splitlines():
        if not line.startswith("data:"):
            continue
        try:
            data = json.loads(line[len("data:"):].strip())
        except json.JSONDecodeError:
            continue

        if "error" in data:
            raise RuntimeError(f"MCP error: {data['error']}")

        result = data.get("result", {})
        # Return structured content if available, else text
        structured = result.get("structuredContent")
        if structured:
            return structured

        for item in result.get("content", []):
            if item.get("type") == "text":
                try:
                    return json.loads(item["text"])
                except (json.JSONDecodeError, TypeError):
                    return {"text": item["text"]}

    raise RuntimeError(f"No valid MCP response: {resp.text[:300]}")


def execute_query(query_id: int) -> str:
    """Execute a query via MCP and return execution ID."""
    result = _mcp_call("executeQueryById", {"query_id": query_id})
    execution_id = result.get("execution_id")
    state = result.get("state", "unknown")
    print(f"Execution started: {execution_id} (state: {state})")
    return execution_id


def poll_until_complete(execution_id: str) -> None:
    """Poll execution status with short timeouts until complete."""
    elapsed = 0
    while elapsed < MAX_WAIT:
        try:
            result = _mcp_call(
                "getExecutionResults",
                {"executionId": execution_id, "limit": 0, "offset": 0, "timeout": 0},
                timeout=30,
            )
            state = result.get("state", "")
        except Exception as e:
            # Transient connection errors during polling — retry
            print(f"  [{elapsed}s] Poll error (retrying): {e}")
            time.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL
            continue

        if state == "COMPLETED":
            total = result.get("resultMetadata", {}).get("totalRowCount", "?")
            print(f"  Execution completed in ~{elapsed}s. Total rows: {total}")
            return
        elif state in ("FAILED", "CANCELLED", "EXPIRED"):
            msg = result.get("errorMessage", "unknown")
            print(f"  Execution {state}: {msg}")
            sys.exit(1)

        print(f"  [{elapsed}s] {state}...")
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL

    print(f"Timeout after {MAX_WAIT}s")
    sys.exit(1)


def get_results_batch(execution_id: str, limit: int = 100, offset: int = 0) -> dict:
    """Fetch a single batch of results (execution must be complete)."""
    return _mcp_call(
        "getExecutionResults",
        {"executionId": execution_id, "limit": limit, "offset": offset, "timeout": 0},
        timeout=60,
    )


def download_results(execution_id: str, output_path: Path) -> int:
    """Poll for completion, then download all results via MCP pagination."""
    print("  Waiting for execution to complete...")
    poll_until_complete(execution_id)

    # Get first batch + metadata
    result = get_results_batch(execution_id, limit=100, offset=0)
    total_rows = result.get("resultMetadata", {}).get("totalRowCount", 0)
    rows = result.get("data", {}).get("rows", [])
    all_rows = list(rows)
    print(f"  Fetched {len(all_rows)}/{total_rows} rows...")

    # Paginate through remaining rows
    while len(all_rows) < total_rows:
        batch = get_results_batch(execution_id, limit=100, offset=len(all_rows))
        batch_rows = batch.get("data", {}).get("rows", [])
        if not batch_rows:
            break
        all_rows.extend(batch_rows)
        if len(all_rows) % 500 == 0 or len(all_rows) >= total_rows:
            print(f"  Fetched {len(all_rows)}/{total_rows} rows...")

    # Write as CSV
    if all_rows:
        keys = list(all_rows[0].keys())
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_rows)

    print(f"Downloaded {len(all_rows)} rows to {output_path}")
    return len(all_rows)


def run_query_04():
    """Query 04: Full Base chain USDC transaction histories."""
    sql_path = QUERIES_DIR / "04_agent_transaction_histories_full.sql"
    sql = sql_path.read_text()

    print(f"\n{'='*60}")
    print("Query 04: Agent USDC Transaction Histories (Base)")
    print(f"SQL size: {len(sql):,} chars")
    print(f"{'='*60}\n")

    query_id = create_query_via_mcp(
        "A2A Research: ERC-8004 Agent USDC Histories (Base, 1505 agents)", sql
    )
    execution_id = execute_query(query_id)

    output = DATA_DIR / "dune_agent_transactions.csv"
    row_count = download_results(execution_id, output)

    return query_id, row_count


def build_multichain_sql() -> str:
    """Build Query 05: Multi-chain agent activity."""
    agents_path = DATA_DIR / "base_erc8004_agents.json"
    with open(agents_path) as f:
        data = json.load(f)
    addrs = data["addresses"]

    values = ",\n    ".join([f"(0x{a[2:]})" for a in addrs])

    sql = f"""-- Multi-chain ERC-8004 agent USDC activity (Base + Ethereum + BNB)
-- For Cross-Platform Correlation signal validation
WITH agents(addr) AS (
  VALUES
    {values}
)

SELECT
    'base' AS chain,
    t.evt_tx_hash,
    t.evt_block_number,
    t.evt_block_time,
    t."from" AS sender,
    t."to" AS receiver,
    CAST(t.value AS DOUBLE) / 1e6 AS amount_usdc
FROM erc20_base.evt_transfer t
INNER JOIN agents a ON t."from" = a.addr
WHERE t.contract_address = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
  AND t.evt_block_date >= DATE '2024-06-01'

UNION ALL

SELECT
    'base' AS chain,
    t.evt_tx_hash,
    t.evt_block_number,
    t.evt_block_time,
    t."from" AS sender,
    t."to" AS receiver,
    CAST(t.value AS DOUBLE) / 1e6 AS amount_usdc
FROM erc20_base.evt_transfer t
INNER JOIN agents a ON t."to" = a.addr
WHERE t.contract_address = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
  AND t.evt_block_date >= DATE '2024-06-01'

UNION ALL

SELECT
    'ethereum' AS chain,
    t.evt_tx_hash,
    t.evt_block_number,
    t.evt_block_time,
    t."from" AS sender,
    t."to" AS receiver,
    CAST(t.value AS DOUBLE) / 1e6 AS amount_usdc
FROM erc20_ethereum.evt_transfer t
INNER JOIN agents a ON t."from" = a.addr
WHERE t.contract_address = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
  AND t.evt_block_date >= DATE '2024-06-01'

UNION ALL

SELECT
    'ethereum' AS chain,
    t.evt_tx_hash,
    t.evt_block_number,
    t.evt_block_time,
    t."from" AS sender,
    t."to" AS receiver,
    CAST(t.value AS DOUBLE) / 1e6 AS amount_usdc
FROM erc20_ethereum.evt_transfer t
INNER JOIN agents a ON t."to" = a.addr
WHERE t.contract_address = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
  AND t.evt_block_date >= DATE '2024-06-01'

UNION ALL

SELECT
    'bnb' AS chain,
    t.evt_tx_hash,
    t.evt_block_number,
    t.evt_block_time,
    t."from" AS sender,
    t."to" AS receiver,
    CAST(t.value AS DOUBLE) / 1e6 AS amount_usdc
FROM erc20_bnb.evt_transfer t
INNER JOIN agents a ON t."from" = a.addr
WHERE t.contract_address = 0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d
  AND t.evt_block_date >= DATE '2024-06-01'

UNION ALL

SELECT
    'bnb' AS chain,
    t.evt_tx_hash,
    t.evt_block_number,
    t.evt_block_time,
    t."from" AS sender,
    t."to" AS receiver,
    CAST(t.value AS DOUBLE) / 1e6 AS amount_usdc
FROM erc20_bnb.evt_transfer t
INNER JOIN agents a ON t."to" = a.addr
WHERE t.contract_address = 0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d
  AND t.evt_block_date >= DATE '2024-06-01'

ORDER BY evt_block_time ASC"""

    return sql


def run_query_05():
    """Query 05: Multi-chain agent presence."""
    sql = build_multichain_sql()

    # Save SQL for reference
    sql_path = QUERIES_DIR / "05_multichain_agent_activity_full.sql"
    sql_path.write_text(sql)

    print(f"\n{'='*60}")
    print("Query 05: Multi-Chain Agent Activity (Base + ETH + BNB)")
    print(f"SQL size: {len(sql):,} chars")
    print(f"{'='*60}\n")

    query_id = create_query_via_mcp(
        "A2A Research: ERC-8004 Multi-Chain Activity (1505 agents)", sql
    )
    execution_id = execute_query(query_id)

    output = DATA_DIR / "dune_multichain_activity.csv"
    row_count = download_results(execution_id, output)

    return query_id, row_count


def main():
    print("Dune Analytics Data Fetch for A2A Fraud Research")
    print(f"API Key: {DUNE_API_KEY[:8]}...{DUNE_API_KEY[-4:]}")
    print()

    # Query 04: Base chain full histories (closes GAP-01 + GAP-02)
    q04_id, q04_rows = run_query_04()

    # Query 05: Multi-chain presence (closes NOTE-01)
    q05_id, q05_rows = run_query_05()

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Query 04 (Base USDC histories): {q04_rows:,} rows [query_id={q04_id}]")
    print(f"Query 05 (Multi-chain):         {q05_rows:,} rows [query_id={q05_id}]")
    print(f"\nOutput files:")
    print(f"  {DATA_DIR / 'dune_agent_transactions.csv'}")
    print(f"  {DATA_DIR / 'dune_multichain_activity.csv'}")


if __name__ == "__main__":
    main()
