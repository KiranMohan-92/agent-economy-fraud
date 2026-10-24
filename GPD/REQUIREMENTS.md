# Research-integrity and confirmatory requirements

**Defined:** 2026-07-09  
**Status vocabulary:** `complete`, `blocked-external`, `pending`, `withdrawn`

## Integrity repair

| ID | Requirement | Status | Evidence |
|---|---|---|---|
| IR-01 | Separate observed registry proxy from autonomy, humanity, and fraud constructs. | complete | manuscript, code labels, claim ledger |
| IR-02 | Replace the nine-invariant claim with a causal mandate-to-settlement model and explicit falsifiers. | complete | discovery, threat model |
| IR-03 | Separate control, wallet, settlement, entity, market, and outcome observation planes. | complete | threat model |
| IR-04 | Recompute historical metrics and correct averaging/threshold semantics. | complete | empirical audit, audit script |
| IR-05 | Detect and repair event identity loss; fail closed without `evt_index`. | complete in code; historical data invalid | query, bridge, data manifest |
| IR-06 | Repair injection pseudoreplication and demote results to motif sensitivity. | complete in code; old metrics withdrawn | generator, tests, audit |
| IR-07 | Remove fraud decisions/adverse-action tiers from the research score. | complete | fusion implementation, manuscript |
| IR-08 | Remove embedded credentials and document provider-side rotation. | code complete; rotation requires owner | ingestion scripts, SECURITY.md |
| IR-09 | Mark legacy artifacts and prior final verification superseded. | complete | analysis/STATUS.md, VERIFICATION-FINAL.md |
| IR-10 | Create a source-backed claim ledger and deep GPD discovery. | complete | GPD artifacts |
| IR-11 | Run current software, static, manuscript, GPD regression, and adversarial review gates. | pending verification | verification report |

## Confirmatory data and labels

| ID | Requirement | Status | Pass condition |
|---|---|---|---|
| CD-01 | Immutable event-complete transaction release. | blocked-external | versioned query/cutoff, `(chain, tx_hash, evt_index)`, schema, license, SHA-256 |
| CD-02 | Verified executor/control labels with explicit unknown class. | blocked-external | registry owner, current wallet, service, execution and controller evidence separated |
| CD-03 | Independently adjudicated task outcomes. | blocked-external | authorization, deception, victim harm, proceeds/manipulation and case disposition as applicable |
| CD-04 | Post-registration and entity-resolved inclusion flow. | blocked-external | cohort diagram and timestamped evidence without future leakage |
| CD-05 | Privacy/governance review. | blocked-external | lawful basis, minimization, access/retention, DPIA assessment, sharing controls |

## Confirmatory methods

| ID | Requirement | Status | Pass condition |
|---|---|---|---|
| CM-01 | Preregister construct, unit, features, direction, benign twins, model, metrics and kill criteria. | pending | timestamped plan before final holdout |
| CM-02 | Outer temporal or connected-component holdout. | pending | cohort cleaning, graph construction, fitting, calibration and thresholding all train-only |
| CM-03 | Compare with established control baselines. | pending | incremental lift and uncertainty on untouched data |
| CM-04 | Capacity and intervention evaluation. | pending | calibrated precision/recall at capacity plus measured harm reduction |
| CM-05 | Independent red team and held-out generators. | pending | realistic histories, benign automation twins, sufficient entity counts |
| CM-06 | Clean-checkout and external reproduction. | pending | one command from immutable inputs produces machine-checked tables |

## Claim gates

- No `agent` claim above registry association without the corresponding evidence
  tier.
- No `fraud`, `AML`, or `market abuse` metric without task-specific adjudicated
  labels.
- No `false-positive rate` when the comparison class is unknown.
- No `robustness` claim when the detector informed the generator.
- No banking or production claim from public Base-chain transfers.
- No deployment recommendation before CM-04 and governance review pass.
- No completion claim based only on file presence, internal arithmetic, or unit
  tests.
