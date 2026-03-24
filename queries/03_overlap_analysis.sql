-- ============================================================================
-- Query 03: GO/NO-GO GATE — ERC-8004 ↔ Transaction Overlap Analysis
-- Target: Dune Analytics
-- Purpose: Determine if ERC-8004 registered agents have on-chain tx activity
-- ============================================================================
-- This is the critical go/no-go query. We cross-reference ERC-8004 registered
-- agent addresses with ALL their on-chain activity on Base (not just x402).
-- If registered agents are actively transacting, we have ground-truth labels.
-- ============================================================================

-- Step 1: Get all ERC-8004 agent owner addresses on Base
WITH erc8004_agents AS (
    SELECT DISTINCT
        "to" AS agent_address,
        "tokenId" AS token_id,
        evt_block_time AS registration_time
    FROM erc721_base.evt_Transfer
    WHERE contract_address = 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432
      AND "from" = 0x0000000000000000000000000000000000000000
),

-- Step 2: Check USDC transfer activity for these addresses
agent_usdc_activity AS (
    SELECT
        a.agent_address,
        a.token_id,
        a.registration_time,
        COUNT(DISTINCT t.evt_tx_hash) AS usdc_tx_count,
        SUM(CAST(t.value AS DOUBLE) / 1e6) AS total_usdc_volume,
        MIN(t.evt_block_time) AS first_usdc_tx,
        MAX(t.evt_block_time) AS last_usdc_tx
    FROM erc8004_agents a
    LEFT JOIN erc20_base.evt_Transfer t
        ON (t."from" = a.agent_address OR t."to" = a.agent_address)
        AND t.contract_address = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913  -- USDC
        AND t.evt_block_time >= a.registration_time  -- only post-registration activity
    GROUP BY a.agent_address, a.token_id, a.registration_time
),

-- Step 3: Check general Base transaction activity
agent_base_activity AS (
    SELECT
        a.agent_address,
        COUNT(DISTINCT t.hash) AS base_tx_count,
        SUM(CAST(t.value AS DOUBLE) / 1e18) AS total_eth_volume
    FROM erc8004_agents a
    LEFT JOIN base.transactions t
        ON (t."from" = a.agent_address OR t."to" = a.agent_address)
        AND t.block_time >= DATE '2026-01-01'
    GROUP BY a.agent_address
)

-- Step 4: Produce overlap summary
SELECT
    -- Overall statistics
    COUNT(DISTINCT u.agent_address) AS total_erc8004_agents,
    COUNT(DISTINCT CASE WHEN u.usdc_tx_count > 0 THEN u.agent_address END) AS agents_with_usdc_activity,
    COUNT(DISTINCT CASE WHEN b.base_tx_count > 0 THEN u.agent_address END) AS agents_with_any_base_activity,
    COUNT(DISTINCT CASE WHEN u.usdc_tx_count >= 10 THEN u.agent_address END) AS agents_with_10plus_usdc_txns,
    -- Volume statistics
    SUM(u.usdc_tx_count) AS total_usdc_transactions,
    SUM(u.total_usdc_volume) AS total_usdc_volume,
    SUM(b.base_tx_count) AS total_base_transactions,
    -- Overlap ratios
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN u.usdc_tx_count > 0 THEN u.agent_address END)
          / NULLIF(COUNT(DISTINCT u.agent_address), 0), 2) AS pct_agents_with_usdc,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN b.base_tx_count > 0 THEN u.agent_address END)
          / NULLIF(COUNT(DISTINCT u.agent_address), 0), 2) AS pct_agents_with_base_activity
FROM agent_usdc_activity u
LEFT JOIN agent_base_activity b ON u.agent_address = b.agent_address;

-- Detailed per-agent breakdown (top 100 most active)
-- SELECT
--     u.agent_address,
--     u.token_id,
--     u.registration_time,
--     u.usdc_tx_count,
--     u.total_usdc_volume,
--     b.base_tx_count,
--     b.total_eth_volume,
--     u.first_usdc_tx,
--     u.last_usdc_tx
-- FROM agent_usdc_activity u
-- LEFT JOIN agent_base_activity b ON u.agent_address = b.agent_address
-- WHERE u.usdc_tx_count > 0 OR b.base_tx_count > 0
-- ORDER BY u.usdc_tx_count DESC
-- LIMIT 100;
