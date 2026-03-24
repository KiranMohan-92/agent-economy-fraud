-- ============================================================================
-- Query 01: Extract all ERC-8004 registered agent addresses
-- Target: Dune Analytics
-- Chain: Base (expand to Ethereum, BNB after initial analysis)
-- Contract: 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432 (Identity Registry)
-- ============================================================================
-- ERC-8004 is an ERC-721 extension. Each minted NFT represents a registered
-- agent identity. We extract all Transfer events from address(0) (minting)
-- to get the complete set of registered agent owner addresses.
-- ============================================================================

WITH erc8004_mints AS (
    SELECT
        evt_block_time AS registration_time,
        evt_block_number,
        evt_tx_hash,
        "to" AS agent_owner_address,
        "tokenId" AS agent_token_id
    FROM erc721_base.evt_Transfer
    WHERE contract_address = 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432
      AND "from" = 0x0000000000000000000000000000000000000000  -- mint events only
    ORDER BY evt_block_time ASC
)

SELECT
    agent_owner_address,
    agent_token_id,
    registration_time,
    evt_tx_hash AS registration_tx,
    -- Count registrations per owner (some owners register multiple agents)
    COUNT(*) OVER (PARTITION BY agent_owner_address) AS agents_per_owner
FROM erc8004_mints
ORDER BY registration_time DESC;

-- Summary statistics
-- SELECT
--     COUNT(DISTINCT agent_owner_address) AS unique_agent_owners,
--     COUNT(*) AS total_agent_registrations,
--     MIN(registration_time) AS earliest_registration,
--     MAX(registration_time) AS latest_registration,
--     COUNT(*) FILTER (WHERE registration_time >= NOW() - INTERVAL '30' DAY) AS registrations_last_30d
-- FROM erc8004_mints;
