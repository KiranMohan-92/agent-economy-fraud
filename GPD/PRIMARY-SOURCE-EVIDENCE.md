# Primary-Source Evidence Register

**Status:** Authoritative external-evidence register  
**Version:** 1.0  
**Verified through:** 2026-07-10  
**Companion:** `GPD/CLAIM-LEDGER.md`

## Inclusion rule

This register contains only:

1. official technical specifications or product documentation;
2. official regulatory or standards guidance; and
3. original scholarly papers or preprints inspected for this audit.

Trade press, vendor marketing, secondary summaries, unattributed statistics, and internal
project prose are deliberately excluded as load-bearing evidence. A source appearing here
does not validate every claim made by that source. Each entry states both what was verified
and what the source does **not** establish.

## Evidence-use rule

- Cite the exact URL or identifier below, not a search-result page.
- Keep preprints labeled as preprints unless publication status is independently verified.
- Do not infer autonomous execution from protocol use, registry presence, or wallet activity.
- Do not infer fraud from automation or agent identity.
- Do not use a platform control-plane capability as proof of settlement capability without
  an explicit authorization and transaction bridge.

## Retrieval and snapshot control

Every entry records retrieval date, pinned version where the publisher supplies one,
snapshot state, and content-hash state. `Not preserved` is a limitation, not a checksum:
the proposition was verified against the identified source on the retrieval date, but this
repository cannot reproduce later changes to that source. Mutable official web pages must be
reverified before publication or status promotion. Versioned arXiv identifiers are pinned to
the stated version; no later version may silently replace them. Version metadata for all
eight arXiv entries was checked against the official arXiv API on 2026-07-10.

---

## Official specifications and guidance

### PSE-001 — ERC-8004: Trustless Agents

- **Type:** Official Ethereum ERC specification
- **URL:** https://ercs.ethereum.org/ERCS/erc-8004
- **Retrieved:** 2026-07-10
- **Version/snapshot:** Mutable official specification page; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions:**
  - ERC-8004 defines identity, reputation, and validation registries.
  - Payments are explicitly orthogonal to the protocol.
  - The identity is an ERC-721 token and is transferable.
  - `agentWallet` is separate reserved state. It is initially set to the owner address,
    can be changed only with proof of wallet control, and is cleared when ownership is
    transferred.
  - Registration may occur before an agent URI is added.
  - The specification warns that registration cannot cryptographically guarantee that
    advertised capabilities are functional or non-malicious.
- **Does not establish:** That a registered owner is currently an operational agent; that a
  transaction was autonomously initiated; that a payment was A2A commerce; or that conduct
  was fraudulent.
- **Controls claims:** AEF-C002, AEF-C003, AEF-C010, AEF-C011.

### PSE-002 — OpenClaw Session Tools

- **Type:** Official product documentation
- **URL:** https://docs.openclaw.ai/concepts/session-tool
- **Retrieved:** 2026-07-10
- **Version/snapshot:** Mutable official documentation page; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions:**
  - `sessions_send` sends a message to another session and may optionally wait.
  - `sessions_history` returns a bounded, safety-filtered conversation transcript.
  - `sessions_spawn` creates an isolated sub-agent session.
  - Session tools remain subject to tool profiles and allow/deny policies.
- **Does not establish:** That `sessions_send` signs or submits a financial transaction;
  that `sessions_history` exposes arbitrary wallet histories; or that every session may
  access every other session.
- **Controls claims:** AEF-C010, AEF-C011.

### PSE-003 — OpenClaw Session Visibility Configuration

- **Type:** Official product documentation
- **URL:** https://docs.openclaw.ai/gateway/config-tools
- **Retrieved:** 2026-07-10
- **Version/snapshot:** Mutable official documentation page; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions:**
  - Session-tool visibility defaults to `tree`, meaning the current session and sessions it
    spawned.
  - Broader `all` visibility still requires cross-agent authorization through
    `tools.agentToAgent`.
  - Sandboxing can clamp visibility further.
- **Does not establish:** A publicly enumerable global session or agent registry available
  to any caller.
- **Controls claims:** AEF-C010, AEF-C011.

### PSE-004 — OpenClaw Sub-agents

- **Type:** Official product documentation
- **URL:** https://docs.openclaw.ai/tools/subagents
- **Retrieved:** 2026-07-10
- **Version/snapshot:** Mutable official documentation page; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions:**
  - `cleanup: "delete"` archives the sub-agent session after announcement.
  - The transcript is retained through a renamed transcript file.
  - Sub-agent creation is policy-, depth-, concurrency-, and sandbox-constrained.
- **Does not establish:** Forensic erasure, wallet creation, a fresh blockchain address, or
  transaction execution.
- **Controls claims:** AEF-C010, AEF-C011.

### PSE-005 — OpenClaw Channel Docking and `identityLinks`

- **Type:** Official product documentation
- **URL:** https://docs.openclaw.ai/concepts/channel-docking
- **Retrieved:** 2026-07-10
- **Version/snapshot:** Mutable official documentation page; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions:**
  - `identityLinks` groups channel identifiers belonging to the same sender.
  - Docking changes the reply-delivery route while retaining the same session.
  - Docking does not create accounts, grant access, bypass allowlists, or merge unrelated
    users.
- **Does not establish:** Disposable cross-platform personas or identity-control bypass.
- **Controls claims:** AEF-C010.

### PSE-006 — NIST SP 800-63B-4: Authentication and Authenticator Management

- **Type:** Official NIST guidance
- **URL:** https://pages.nist.gov/800-63-4/sp800-63b.html
- **Retrieved:** 2026-07-10
- **Version/snapshot:** NIST SP 800-63B-4 official web edition; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions:**
  - Cryptographic authenticators are recognized at multiple assurance levels.
  - A biometric characteristic is not an authenticator by itself and is used in conjunction
    with a physical authenticator when selected.
  - The guidance requires an alternative non-biometric authentication option.
  - Higher-assurance designs can use public-key cryptography, non-exportable keys, replay
    resistance, and authentication intent.
- **Does not establish:** That biometrics are universally required, or that software agents
  cannot be authenticated through cryptographic and delegated-control mechanisms.
- **Controls claims:** AEF-C012, AEF-C022.

### PSE-007 — FinCEN Interagency Interpretive Guidance on Customer Identification Programs

- **Type:** Official United States regulatory guidance
- **URL:** https://www.fincen.gov/resources/statutes-regulations/guidance/interagency-interpretive-guidance-customer-identification
- **Retrieved:** 2026-07-10
- **Version/snapshot:** Mutable official guidance page; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions:**
  - Customer identification is risk-based and must give a bank a reasonable belief that it
    knows the customer’s true identity.
  - A digital certificate may be used as one non-documentary identity-verification method
    for electronic account opening.
- **Does not establish:** A universal biometric, device-fingerprint, or geolocation mandate.
- **Controls claims:** AEF-C012, AEF-C022.

### PSE-008 — EDPB Guidelines 02/2025 on Personal Data Processing Through Blockchain Technologies

- **Type:** Official European Data Protection Board guidance
- **URL:** https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf
- **Retrieved:** 2026-07-10
- **Version/snapshot:** Official Guidelines 02/2025 version 2 PDF; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions:**
  - Public keys or related blockchain identifiers can qualify as personal data when a
    natural person is reasonably identifiable using means reasonably likely to be used.
  - Replacing or pseudonymizing an identifier does not by itself remove all data-protection
    implications.
- **Does not establish:** That every wallet address is always personal data; the assessment
  remains processing- and context-specific.
- **Controls claims:** AEF-C021.

---

## Primary scholarly sources: ERC-8004 and agentic commerce

### PSE-009 — Xiong et al., *Can Trustless Agents Be Trusted?*

- **Type:** Primary empirical preprint
- **Identifier:** arXiv:2606.26028v2
- **URL:** https://arxiv.org/abs/2606.26028v2
- **Retrieved:** 2026-07-10
- **Version/snapshot:** arXiv v2, updated 2026-07-08; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions from the paper abstract:**
  - The study crawls ERC-8004 identity and reputation data across Ethereum, BNB Smart Chain,
    and Base through 2026-05-13.
  - Most registrations are reported as placeholders rather than active agents.
  - Only 3%, 4%, and 15% of registrations on Ethereum, BSC, and Base respectively exposed a
    valid registration file with at least one live service endpoint.
  - The study reports substantial coordinated-Sybil behavior among reviewers.
- **Does not establish:** The operational status of every address in this repository’s exact
  cohort; autonomous initiation of this repository’s transactions; or fraud labels.
- **Controls claims:** AEF-C003, AEF-C020.

### PSE-010 — Mafrur and Khusumanegara, *From Agent Identity to Agent Economy*

- **Type:** Primary empirical preprint
- **Identifier:** arXiv:2606.12128v1
- **URL:** https://arxiv.org/abs/2606.12128v1
- **Retrieved:** 2026-07-10
- **Version/snapshot:** arXiv v1, submitted 2026-06-10; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions from the paper abstract:**
  - The study separates identity registration from operational readiness.
  - Early ERC-8004 adoption is described as registration-heavy but operationally shallow.
  - Metadata, service exposure, reputation formation, and cross-chain evidence are limited
    and concentrated among a subset of participants.
- **Does not establish:** Fraud prevalence or fraud-detection performance.
- **Controls claims:** AEF-C003, AEF-C020.

### PSE-011 — Liu, *A Dataset of Early Blockchain-Registered AI Agents on Ethereum*

- **Type:** Primary dataset preprint
- **Identifier:** arXiv:2604.22652v1
- **URL:** https://arxiv.org/abs/2604.22652v1
- **Retrieved:** 2026-07-10
- **Version/snapshot:** arXiv v1, submitted 2026-04-24; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions from the paper abstract:**
  - The released dataset covers 10,000 ERC-8004 registrations on Ethereum within a defined
    block range.
  - It distinguishes identity records, mint transactions, transfer events, reputation, and
    resolved metadata where available.
- **Does not establish:** That registration alone proves a live or autonomous agent. Its
  layered fields instead demonstrate why those constructs should be kept separate.
- **Controls claims:** AEF-C003, AEF-C020.

### PSE-012 — Gong, *Agent-to-Agent Finance*

- **Type:** Primary conceptual preprint
- **Identifier:** arXiv:2607.00245v1
- **URL:** https://arxiv.org/abs/2607.00245v1
- **Retrieved:** 2026-07-10
- **Version/snapshot:** arXiv v1, submitted 2026-06-30; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions from the paper abstract:**
  - Agent-to-agent finance requires infrastructure for identity, authorization, payment,
    verification, reputation, and accountability.
  - The decisive design question is bounded autonomy, rather than unrestricted autonomous
    access to funds.
- **Does not establish:** Empirical fraud prevalence, a detector, or the correctness of this
  repository’s proxy labels.
- **Controls claims:** AEF-C011, AEF-C013.

### PSE-017 — Zhang et al., *SoK: Blockchain Agent-to-Agent Payments*

- **Type:** Primary systematization preprint
- **Identifier:** arXiv:2604.03733v1
- **URL:** https://arxiv.org/abs/2604.03733v1
- **Retrieved:** 2026-07-10
- **Version/snapshot:** arXiv v1, submitted 2026-04-04; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions from the paper abstract:**
  - The paper organizes blockchain A2A payments into discovery, authorization, execution,
    and accounting stages.
  - It identifies weak intent binding, misuse under valid authorization,
    payment–service decoupling, and limited accountability as cross-stage challenges.
- **Does not establish:** On-chain fraud-detector performance or this repository’s claimed
  nine-invariant taxonomy.
- **Controls claims:** AEF-C011, AEF-C020.

### PSE-018 — Mao et al., *SoK: Security of Autonomous LLM Agents in Agentic Commerce*

- **Type:** Primary systematization preprint
- **Identifier:** arXiv:2604.15367v2
- **URL:** https://arxiv.org/abs/2604.15367v2
- **Retrieved:** 2026-07-10
- **Version/snapshot:** arXiv v2, updated 2026-05-01; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions from the paper abstract:**
  - The work treats agentic-commerce security as a cross-layer problem spanning agent
    integrity, transaction authorization, inter-agent trust, market manipulation, and
    regulatory compliance.
  - It derives twelve attack vectors and proposes a layered defense architecture.
- **Does not establish:** This repository’s empirical detection claims or novelty over all
  possible detection work. It is close prior work for threat-taxonomy positioning.
- **Controls claims:** AEF-C011, AEF-C020.

### PSE-019 — Li et al., *A402: Binding Cryptocurrency Payments to Service Execution for Agentic Commerce*

- **Type:** Primary protocol preprint
- **Identifier:** arXiv:2603.01179v2
- **URL:** https://arxiv.org/abs/2603.01179v2
- **Retrieved:** 2026-07-10
- **Version/snapshot:** arXiv v2, updated 2026-03-19; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions from the paper abstract:**
  - A402 separates and then cryptographically binds service execution, payment, and result
    delivery using Atomic Service Channels and TEE-assisted adaptor signatures.
  - The paper implements and evaluates the protocol on Bitcoin and Ethereum.
- **Does not establish:** Population-level behavioral fraud detection. It demonstrates that
  payment–service binding is a protocol-layer control distinct from post-hoc transaction
  scoring.
- **Controls claims:** AEF-C011, AEF-C020.

---

## Primary scholarly sources: graph and financial-crime detection

### PSE-013 — Weber et al., *Anti-Money Laundering in Bitcoin*

- **Type:** Primary peer-reviewed research paper
- **Venue:** KDD 2019
- **URL:** https://research.ibm.com/publications/anti-money-laundering-in-bitcoin-experimenting-with-graph-convolutional-networks-for-financial-forensics
- **Retrieved:** 2026-07-10
- **Version/snapshot:** KDD 2019 publisher record; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified proposition:** Graph-based learning over blockchain transaction data was used
  for anti-money-laundering classification before this work.
- **Does not establish:** Agent-specific detection or ERC-8004 constructs.
- **Controls claims:** AEF-C014, AEF-C015, AEF-C019.

### PSE-014 — Song et al., *Identifying Money Laundering Subgraphs on the Blockchain*

- **Type:** Primary peer-reviewed research paper
- **Venue:** ICAIF 2024
- **URL:** https://research.ibm.com/publications/identifying-money-laundering-subgraphs-on-the-blockchain
- **Retrieved:** 2026-07-10
- **Version/snapshot:** ICAIF 2024 publisher record; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified proposition:** Transaction subgraphs and multi-transaction laundering
  structures are established AML research objects.
- **Does not establish:** That every coordinated pattern is fraud or that the method solves
  agentic-commerce attribution.
- **Controls claims:** AEF-C014, AEF-C015, AEF-C017, AEF-C019.

### PSE-015 — Blanusa et al., *Graph Feature Preprocessor*

- **Type:** Primary peer-reviewed research paper
- **Venue:** ICAIF 2024
- **URL:** https://research.ibm.com/publications/graph-feature-preprocessor-real-time-subgraph-based-feature-extraction-for-financial-crime-detection
- **Retrieved:** 2026-07-10
- **Version/snapshot:** ICAIF 2024 publisher record; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified propositions:**
  - The work extracts transaction-subgraph features in real time for downstream financial
    crime detection.
  - Its implementation maintains a streaming dynamic graph and evaluates graph-derived
    features against AML and phishing datasets.
- **Does not establish:** That a production system exists at every chain’s block cadence or
  that this repository’s collective detector has been implemented.
- **Controls claims:** AEF-C014, AEF-C015, AEF-C017, AEF-C019.

### PSE-016 — Simchowitz, Pfrommer, and Jadbabaie, *The Pitfalls of Imitation Learning when Actions are Continuous*

- **Type:** Primary theoretical preprint
- **Identifier:** arXiv:2503.09722v4
- **URL:** https://arxiv.org/abs/2503.09722v4
- **Retrieved:** 2026-07-10
- **Version/snapshot:** arXiv v4, updated 2025-07-26; no local snapshot preserved.
- **Content hash:** Not preserved.
- **Verified proposition:** The paper studies limitations of imitation learning with
  continuous actions and stochastic experts.
- **Does not establish:** A universal theorem that deterministic software cannot reproduce
  a transaction-timing distribution, that a seeded pseudorandom generator is detectably
  regular, or that coefficient of variation below 0.05 is an agent invariant.
- **Controls claims:** AEF-C014.

## Source gaps retained as unknowns

The following require new primary evidence rather than stronger prose:

- independently adjudicated agent-fraud transaction labels;
- verified autonomous execution traces linked to on-chain transactions;
- a verified human-controlled negative cohort;
- external temporal, chain, and institutional validation;
- independent adaptive red-team attack traces;
- a systematic production-system survey for collective detection;
- jurisdiction- and deployment-specific privacy and model-risk analysis; and
- archived snapshots plus content hashes for the mutable official web sources above.

Until those gaps are filled, the corresponding claims remain exploratory, untested, or
withdrawn in `GPD/CLAIM-LEDGER.md`.
