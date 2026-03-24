-- ============================================================================
-- Query 02: Extract x402 facilitator USDC transactions on Base
-- Target: Dune Analytics
-- Chain: Base
-- USDC Contract: 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
-- ============================================================================
-- x402 payments settle as standard USDC ERC-20 transfers routed through
-- known facilitator contracts. We identify x402 transactions by filtering
-- for transfers where the sender or receiver interacts with known facilitator
-- addresses. The CDP production facilitator is the primary one.
--
-- NOTE: x402 facilitator addresses need to be confirmed from on-chain data.
-- The approach below uses heuristics: high-frequency, small-value USDC
-- transfers with programmatic patterns (uniform amounts, rapid succession).
-- ============================================================================

-- Step 1: All USDC transfers on Base (last 90 days for manageability)
WITH usdc_transfers AS (
    SELECT
        evt_block_time AS transfer_time,
        evt_block_number,
        evt_tx_hash,
        "from" AS sender,
        "to" AS receiver,
        CAST(value AS DOUBLE) / 1e6 AS amount_usdc  -- USDC has 6 decimals
    FROM erc20_base.evt_Transfer
    WHERE contract_address = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913  -- USDC on Base
      AND evt_block_time >= NOW() - INTERVAL '90' DAY
),

-- Step 2: Identify likely x402 micro-payment patterns
-- x402 average payment is ~$0.20; look for high-frequency small transfers
micropayment_senders AS (
    SELECT
        sender,
        COUNT(*) AS tx_count,
        AVG(amount_usdc) AS avg_amount,
        STDDEV(amount_usdc) AS stddev_amount,
        MIN(amount_usdc) AS min_amount,
        MAX(amount_usdc) AS max_amount,
        MIN(transfer_time) AS first_tx,
        MAX(transfer_time) AS last_tx
    FROM usdc_transfers
    WHERE amount_usdc < 10  -- x402 transactions are typically micropayments
    GROUP BY sender
    HAVING COUNT(*) >= 10  -- at least 10 transactions (filtering noise)
)

-- Step 3: Extract candidate x402 transactions
SELECT
    t.transfer_time,
    t.evt_tx_hash,
    t.sender,
    t.receiver,
    t.amount_usdc,
    ms.tx_count AS sender_total_txns,
    ms.avg_amount AS sender_avg_amount
FROM usdc_transfers t
INNER JOIN micropayment_senders ms ON t.sender = ms.sender
WHERE t.amount_usdc < 10
ORDER BY t.transfer_time DESC
LIMIT 50000;
