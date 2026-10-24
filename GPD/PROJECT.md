# Agentic Payment Control and Financial-Crime Research

**Integrity-repair date:** 2026-07-09  
**Canonical status:** research repair complete; confirmatory empirical program blocked by missing admissible data and outcome labels

## Objective

Determine what the repository's registry and transaction evidence can actually
support, construct a hard-to-vary explanation of agentic-payment loss, and
define the observations and experiments required to test attribution,
control-plane security, fraud, AML, and market-abuse hypotheses without
conflating them.

## Core research question

Where can delegated software execution break the causal chain from accountable
principal and bounded mandate through instruction provenance, tool/wallet
authorization, settlement, and outcome; which controls prevent or limit harm;
and what evidence is required to demonstrate incremental detection or
intervention value?

## Hard-to-vary explanation

Financial loss becomes possible where the chain from controller intent and
mandate, through instruction provenance and tool/wallet authorization, to
settlement is not cryptographically and operationally preserved. Automation
changes speed, scale, delegation depth, and coordination; it does not make
actor type fraudulent. Controls must bind each action to an authenticated
controller and bounded mandate, enforce least privilege and payment limits,
preserve provenance, and monitor value, counterparty, and graph outcomes
independently of executor substrate.

This explanation is falsifiable at specific links. Intact mandate, provenance,
authorization, and settlement should permit legitimate high-speed execution.
Breaking a link should increase unauthorized action or loss risk under matched
conditions; if it does not, that link is not causally load-bearing.

## Scoping contract

### In scope

- construct, label, provenance, and reproducibility audit of the existing work;
- registry/automation attribution as a task separate from fraud;
- control-plane, wallet-policy, settlement, entity-network, market, and outcome
  observation planes;
- separately specified fraud/scam, AML, sanctions, and market-abuse hypotheses;
- leakage-safe confirmatory study design and operational safety gates;
- primary-source verification of platform, registry, identity, privacy, and
  financial-crime claims.

### Out of scope for current evidence

- validated autonomous-agent identification;
- fraud, AML, sanctions, or market-abuse performance;
- banking generalization;
- adversarial robustness or incidence/prevalence claims;
- deployment thresholds, costs, timelines, or regulatory/legal conclusions.

## Evidence boundary

The local empirical snapshot reaches registry-association evidence only. Its
positive class is a historical owner/default-wallet proxy; its comparison class
is unknown. It contains no verified current wallet, autonomous execution,
mandate, fraud outcome, victim harm, case disposition, beneficial ownership, or
banking data. Historical transaction derivatives also inherit a lossy event-key
defect and are inadmissible for confirmatory inference.

## Workstreams

1. **Attribution:** verified executor/controller classes, with unknown retained.
2. **Control security:** mandate, instruction, tool, key, and policy failures.
3. **Fraud/scams:** unauthorized/deceptive loss and intervention outcomes.
4. **AML/sanctions:** entity, proceeds, suspicion, and investigator outcomes.
5. **Market abuse:** orders, trades, ownership, coordination, and price impact.

## Acceptance tests

The repair milestone is complete only when unsupported claims are withdrawn,
code and labels fail closed, old artifacts are marked superseded, exact audit
calculations are preserved, a claim ledger and primary-source record exist, and
fresh adversarial review finds the new boundaries coherent.

A confirmatory empirical milestone is complete only after an immutable
event-complete corpus, verified execution/control evidence, independently
adjudicated outcomes, outer temporal/component holdout, frozen analysis plan,
clean-checkout reproduction, and external review. Synthetic motifs alone can
never satisfy this gate.

## Stop/rethink conditions

- the target is not directly observed or label uncertainty is hidden;
- an event, entity, time, or graph dependency can leak across the holdout;
- a below-chance or failed result receives a post-hoc mechanism without being
  labeled exploratory;
- the claimed data plane cannot observe the proposed mechanism;
- a score is proposed for adverse action without outcome and intervention
  evidence;
- a primary source contradicts the platform, legal, or protocol claim.

## Authoritative outputs

- `GPD/analysis/discovery-agentic-fraud-economy-research-hardening.md`
- `GPD/CLAIM-LEDGER.md`
- `GPD/PRIMARY-SOURCE-EVIDENCE.md`
- `GPD/VERIFICATION-2026-07-09.md`
- `paper/agent-economy-fraud-arxiv.md`
- `data/MANIFEST.md`
- `analysis/STATUS.md`

Historical phase artifacts remain for traceability and are not authoritative
where they conflict with these outputs.
