# Data manifest and admissibility status

Status date: 2026-07-09

This file identifies the local historical artifacts used in the audit. It is
not a public dataset release. All listed artifacts are ignored by Git and are
therefore absent from a clean checkout.

## Decisive defects

- `dune_agent_transactions.csv` was produced without `evt_index`.
- The old bridge deduplicated by `tx_hash`, discarding 13,539 of 107,118 rows
  (12.64%). Of those, 10,626 were distinct transfer-event tuples, not exact
  duplicates.
- All Stage 2 derivatives and metrics below inherit that event-loss defect.
- `attack_injection_dataset.parquet` reused sender identities across injection
  instances. The corrected generator changes the sender population from 82 to
  689, so all Stage 3 derivatives and metrics are stale.
- Labels represent historical registry-owner/default-wallet proxies and unknown
  counterparties, not agents/humans or fraud/legitimate outcomes.

## Forensic artifact identities

| Local file | SHA-256 | Status |
|---|---|---|
| `dune_agent_transactions.csv` | `F1DBA355ADC899C34AAFB2D25ADDEFD8236D446FBDB48700F68C8C4F19A69484` | Superseded raw extraction; missing event index. |
| `transactions_dune.parquet` | `E4B57AF4EA27D27680182DDFCE750CDA1545E9DC81E0FF53530095F3F0386A6A` | Invalid derivative of lossy bridge. |
| `labels_dune.parquet` | `EF0021805453925245A6BFF5B0C722137159A8D8903069E3C2157EEF7CD7096D` | Historical proxy/unknown labels; old strings overstate semantics. |
| `detection_results_dune.csv` | `A7AA06AC0E77643542FAA923DBBB8A35096023A28B6680E285B15CA6BAA78F07` | Forensic reconstruction only. |
| `validation_metrics.json` | `282212B8BB929B63E3328972FD5D279CBCA7EDA2A2E02288438D66F2BA81371E` | Historical/post-hoc result; not confirmatory. |
| `attack_injection_dataset.parquet` | `943087D7CA90263401B8DBEAA1BB68A4D4C233A8576770F26910AD3458B1F522` | Stale pseudoreplicated motif corpus. |
| `fraud_detection_results.parquet` | `E0B6B36DCD212686F3B28C2758558E7565A09FE668CA9E656AA1AB54D88370F4` | Withdrawn terminology and stale population. |
| `fraud_detection_metrics.json` | `3FE0A4568229EF785374FE282BAB8DD06FE6785746786E42C9FA0E40888F3C31` | Withdrawn Stage 3 metrics. |

Hashes establish which files were audited; they do not validate the files.

## Deterministic forensic audit output

`GPD/verification/research-audit-results.json` is the tracked, machine-readable
recomputation of the defects and historical arithmetic above.  It was generated
twice with identical bytes using:

```text
PYTHONPATH=src python -B -m a2a_detection.scripts.audit_research_claims \
  --output GPD/verification/research-audit-results.json
```

Its SHA-256 is
`c5185d10c6d6beae31bd6c6581d02e20d772c5d7af8b2303cd72d32e71a2950f`.
Strict mode exits nonzero because the underlying artifacts are invalid or
stale; that is the intended fail-closed result.  The audit output preserves the
historical composite AUC and defect counts, but it does not make the ignored
inputs reproducible from a clean clone or validate operational performance.

## Requirements for a valid replacement

A new version must use `(chain, tx_hash, evt_index)` as event identity; bound
the query by block or timestamp; record query ID, exact SQL, extraction time,
schema and inclusion flow; distinguish registry owner from current verified
agent wallet; preserve unknown labels; document license and privacy controls;
publish file sizes and SHA-256 hashes; and use a new version identifier. It must
not overwrite or silently inherit any historical metric.
