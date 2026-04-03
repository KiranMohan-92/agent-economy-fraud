"""Poll Dune execution status and download results when ready."""

import csv
import json
import sys
import time

import httpx

DUNE_API_KEY = "HrBeJCELgfMTjUBuGQgxvv3hafVS5YzB"
DUNE_MCP_URL = "https://api.dune.com/mcp/v1"
HEADERS = {
    "x-dune-api-key": DUNE_API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def mcp_call(tool, args, timeout=60):
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
    return {}


def check_status(execution_id):
    r = mcp_call("getExecutionResults", {"executionId": execution_id, "limit": 0, "offset": 0, "timeout": 0})
    return r.get("state", "UNKNOWN"), r


def download_all(execution_id, output_path):
    all_rows = []
    offset = 0
    while True:
        r = mcp_call("getExecutionResults", {"executionId": execution_id, "limit": 100, "offset": offset, "timeout": 0})
        total = r.get("resultMetadata", {}).get("totalRowCount", 0)
        rows = r.get("data", {}).get("rows", [])
        if not rows:
            break
        all_rows.extend(rows)
        offset += len(rows)
        print(f"  Downloaded {len(all_rows)}/{total} rows...")

    if all_rows:
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
            writer.writeheader()
            writer.writerows(all_rows)
    print(f"Saved {len(all_rows)} rows to {output_path}")
    return len(all_rows)


def main():
    executions = {
        "1505-agent (Base USDC)": ("01KN837VT8RJPV9YK9XK6FFN2X", "data/dune_agent_transactions.csv"),
        "50-agent (Base USDC)": ("01KN83WFEG2DFZ2JTQCVAEGQB8", "data/dune_50agent_transactions.csv"),
    }

    max_wait = 1800  # 30 minutes
    elapsed = 0
    completed = set()

    while elapsed < max_wait and len(completed) < len(executions):
        for label, (eid, path) in executions.items():
            if label in completed:
                continue
            try:
                state, result = check_status(eid)
            except Exception as e:
                print(f"[{elapsed}s] {label}: poll error ({e})")
                continue

            if state == "COMPLETED":
                total = result.get("resultMetadata", {}).get("totalRowCount", 0)
                cost = result.get("resultMetadata", {}).get("executionCostCredits", "?")
                print(f"[{elapsed}s] {label}: COMPLETED! {total} rows, {cost} credits")
                download_all(eid, path)
                completed.add(label)
            elif state in ("FAILED", "CANCELLED", "EXPIRED"):
                msg = result.get("errorMessage", "unknown")
                print(f"[{elapsed}s] {label}: {state} — {msg}")
                completed.add(label)
            else:
                print(f"[{elapsed}s] {label}: {state}")

        if len(completed) < len(executions):
            time.sleep(30)
            elapsed += 30

    print(f"\nDone. {len(completed)}/{len(executions)} executions resolved.")


if __name__ == "__main__":
    main()
