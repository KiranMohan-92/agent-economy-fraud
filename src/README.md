> [!CAUTION]
> **WITHDRAWN DRAFT (July 2026): Stage 1 results are withdrawn; see
> [README](../README.md) and [GPD/CLAIM-LEDGER.md](../GPD/CLAIM-LEDGER.md).
> Kept for the record.**

# a2a-fincrime-detection (research audit toolkit)

This package preserves and repairs an exploratory study of transaction-derived
features on ERC-8004 registry-associated addresses. Despite the historical
distribution name, it is **not a fraud detector** and exposes no allow/block
decision tiers.

The observed target is `registry_owner_proxy` versus
`counterparty_unknown`. Registry association does not prove a current agent
wallet, live service, autonomous execution, transaction purpose, or fraud.

## Local installation

From the repository root:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e "src[dev]"
.venv\Scripts\python -m pytest -q -p no:cacheprovider src/a2a_detection/tests
```

## Research scoring

```python
import pandas as pd

from a2a_detection.signals import SignalFusion

transactions = pd.read_parquet("data/transactions.parquet")
fusion = SignalFusion()  # equal-weight, untuned research baseline
results = fusion.score_batch(["0x..."], transactions)  # pandas DataFrame
print(results.iloc[0]["composite_score"])
```

The score is a descriptive research output, not a probability. The historical
threshold `0.09` exists only to reconstruct old reports. `SignalFusion.exploratory()`
loads post-hoc weights and must not be treated as confirmatory performance.

## Data and audit status

- The historical local corpus lost distinct ERC-20 events through
  transaction-hash deduplication and is superseded.
- Historical injection results are stale because injected identities were
  reused across instances.
- Large data files are not tracked, so a clean checkout cannot reproduce the
  numerical audit yet.
- The bridge now requires `evt_index` and fails closed if event identity is
  unavailable.
- Dune access requires `DUNE_API_KEY` in the environment; there is no embedded
  credential or fallback.

See `../data/MANIFEST.md`, `../GPD/CLAIM-LEDGER.md`, and the repaired manuscript
for the evidence boundary and confirmatory research protocol.

## Safety boundary

Do not use this code to block payments, restrict accounts, accuse customers,
file regulatory reports, or make law-enforcement referrals. Any future
operational use requires independently adjudicated outcomes, leakage-safe
validation, calibration, model-risk and privacy review, intervention evidence,
and human governance.

## License

Apache License 2.0. See `../LICENSE`.
