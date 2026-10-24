"""Research-integrity contracts for proxy labels and synthetic motif audits."""

from __future__ import annotations

import json

import pandas as pd
import pytest

from a2a_detection.scripts import validate_precision
from a2a_detection.scripts.audit_research_claims import (
    audit_event_identity,
    audit_injection_sender_uniqueness,
    audit_stage2_metrics,
)
from a2a_detection.scripts.bridge_dune_data import (
    build_labels,
    bridge_base_transactions,
    bridge_multichain,
)
from a2a_detection.scripts.validate_fraud_detection import (
    compute_metrics,
    write_report,
)
from a2a_detection.signals.label_cleaner import (
    COUNTERPARTY_UNKNOWN_LABEL,
    REGISTRY_OWNER_PROXY_LABEL,
    clean_labels,
    filter_thin_counterparties,
)


def _raw_event_rows(*, include_event_index: bool = True) -> pd.DataFrame:
    rows = pd.DataFrame(
        {
            "evt_tx_hash": ["0xaaa", "0xaaa", "0xaaa"],
            "evt_block_number": [1, 1, 1],
            "evt_block_time": [
                "2026-01-01T00:00:00Z",
                "2026-01-01T00:00:00Z",
                "2026-01-01T00:00:00Z",
            ],
            "sender": ["0xagent", "0xagent", "0xagent"],
            "receiver": ["0xone", "0xtwo", "0xone"],
            "amount_usdc": [1.0, 2.0, 1.0],
        }
    )
    if include_event_index:
        rows.insert(1, "evt_index", [7, 8, 7])
    return rows


def test_bridge_requires_event_index_and_preserves_distinct_events(tmp_path):
    missing_index = tmp_path / "missing.csv"
    _raw_event_rows(include_event_index=False).to_csv(missing_index, index=False)

    with pytest.raises(ValueError, match="evt_index"):
        bridge_base_transactions(missing_index, {"0xagent"})

    indexed = tmp_path / "indexed.csv"
    _raw_event_rows().to_csv(indexed, index=False)
    bridged = bridge_base_transactions(indexed, {"0xagent"})

    assert len(bridged) == 2
    assert set(bridged["event_index"]) == {7, 8}
    assert set(bridged["receiver"]) == {"0xone", "0xtwo"}


@pytest.mark.parametrize("bad_hash", [None, "", "   "])
def test_bridge_rejects_missing_tx_hash_before_string_normalization(tmp_path, bad_hash):
    rows = _raw_event_rows()
    rows["evt_tx_hash"] = rows["evt_tx_hash"].astype(object)
    rows.loc[0, "evt_tx_hash"] = bad_hash
    path = tmp_path / "null_hash.csv"
    rows.to_csv(path, index=False)

    with pytest.raises(ValueError, match="Null event identity"):
        bridge_base_transactions(path, {"0xagent"})

    multi = tmp_path / "null_hash_multi.csv"
    rows.assign(chain="base").to_csv(multi, index=False)
    with pytest.raises(ValueError, match="Null event identity"):
        bridge_multichain(multi, {"0xagent"})


def test_multichain_bridge_maps_event_index_before_fail_closed_dedupe(tmp_path):
    rows = _raw_event_rows().assign(chain="base")
    path = tmp_path / "multi.csv"
    rows.to_csv(path, index=False)

    bridged = bridge_multichain(path, {"0xagent"})

    assert len(bridged) == 2
    assert "event_index" in bridged.columns


def test_labels_are_explicit_proxies_and_unknowns_not_humans():
    tx = pd.DataFrame(
        {
            "sender": ["0xproxy", "0xunknown"],
            "receiver": ["0xunknown", "0xproxy"],
        }
    )

    labels = build_labels(tx, {"0xproxy"})

    assert labels["address"].tolist() == ["0xproxy", "0xunknown"]
    assert labels.set_index("address")["label"].to_dict() == {
        "0xproxy": REGISTRY_OWNER_PROXY_LABEL,
        "0xunknown": COUNTERPARTY_UNKNOWN_LABEL,
    }
    assert not labels["label"].isin({"agent", "human"}).any()
    assert labels.loc[labels["label"] == COUNTERPARTY_UNKNOWN_LABEL, "confidence"].eq(0.0).all()


def test_thin_filter_targets_unknown_counterparties_without_relabeling():
    labels = pd.DataFrame(
        [
            {"address": "0xproxy", "label": REGISTRY_OWNER_PROXY_LABEL},
            {"address": "0xthin", "label": COUNTERPARTY_UNKNOWN_LABEL},
            {"address": "0xactive", "label": COUNTERPARTY_UNKNOWN_LABEL},
        ]
    )
    tx = pd.DataFrame(
        {
            "sender": ["0xthin", "0xactive", "0xactive", "0xactive"],
            "receiver": ["0xproxy", "0xproxy", "0xproxy", "0xproxy"],
            "timestamp": pd.date_range("2026-01-01", periods=4, freq="1h", tz="UTC"),
        }
    )

    cleaned, stats = filter_thin_counterparties(labels, tx, min_tx_count=2)

    assert set(cleaned["address"]) == {"0xproxy", "0xactive"}
    assert set(cleaned["label"]) == {
        REGISTRY_OWNER_PROXY_LABEL,
        COUNTERPARTY_UNKNOWN_LABEL,
    }
    assert stats["counterparty_unknown_before"] == 2
    assert stats["thin_counterparties_removed"] == 1
    assert stats["remaining_counterparties_are_verified_humans"] is False


def test_cleaner_rejects_legacy_agent_human_schema():
    labels = pd.DataFrame(
        {
            "address": ["0xagent", "0xhuman"],
            "label": ["agent", "human"],
        }
    )
    tx = pd.DataFrame({"sender": ["0xagent"], "receiver": ["0xhuman"]})

    with pytest.raises(ValueError, match="Legacy agent/human labels"):
        clean_labels(labels, tx)


def test_motif_metrics_use_sensitivity_and_unlabeled_alert_rate_only():
    scores = pd.DataFrame(
        {
            "composite_score": [0.9, 0.2, 0.8, 0.1],
            "synthetic_motif": [True, True, False, False],
            "attack_chain": ["CHAIN_1", "CHAIN_1", "", ""],
            "attack_difficulty": ["EASY", "EASY", "", ""],
        }
    )

    metrics = compute_metrics(scores, reference_threshold=0.5)

    assert metrics["study_type"] == "synthetic_transaction_motif_sensitivity"
    assert metrics["motif_sensitivity"] == 0.5
    assert metrics["unlabeled_alert_rate"] == 0.5
    assert metrics["negative_ground_truth_available"] is False
    assert metrics["operational_claims_valid"] is False
    banned = {"fpr", "precision", "f1", "recall", "tp", "tn", "fp", "fn"}
    assert banned.isdisjoint(metrics)


def test_motif_report_contains_no_operational_or_ground_truth_language(tmp_path):
    scores = pd.DataFrame(
        {
            "composite_score": [0.9, 0.2, 0.8, 0.1],
            "synthetic_motif": [True, True, False, False],
            "attack_chain": ["CHAIN_1", "CHAIN_1", "", ""],
            "attack_difficulty": ["EASY", "EASY", "", ""],
        }
    )
    metrics = compute_metrics(scores, reference_threshold=0.5)
    path = tmp_path / "report.md"

    write_report(metrics, [], None, str(path))
    report = path.read_text(encoding="utf-8").lower()

    for banned in ("fraud", "fpr", "benign", "adversarial", "precision", "operating point"):
        assert banned not in report
    assert "unlabeled alert rate" in report
    assert "synthetic transaction-motif sensitivity" in report


def test_stage2_audit_reproduces_legacy_numbers_but_marks_them_invalid(tmp_path):
    scores = pd.DataFrame(
        {
            "address": ["0xa", "0xb", "0xc", "0xd"],
            "composite_score": [0.9, 0.8, 0.7, 0.1],
            "signal_network_topology": [0.9, 0.8, 0.7, 0.1],
        }
    )
    labels = pd.DataFrame(
        {
            "address": ["0xa", "0xb", "0xc", "0xd"],
            "label": ["agent", "agent", "human", "human"],
        }
    )
    scores_path = tmp_path / "scores.csv"
    labels_path = tmp_path / "labels.parquet"
    scores.to_csv(scores_path, index=False)
    labels.to_parquet(labels_path, index=False)

    audit = audit_stage2_metrics(scores_path, labels_path, reference_threshold=0.75)

    assert audit["status"] == "invalid_legacy_label_semantics"
    assert audit["fraud_ground_truth_available"] is False
    assert audit["verified_human_negative_class_available"] is False
    assert audit["historical_metric_reproduction"]["precision"] == 1.0
    assert audit["historical_metric_reproduction"]["recall"] == 1.0
    assert audit["historical_metric_reproduction"]["fpr"] == 0.0
    assert audit["historical_metric_reproduction"]["valid_for_operational_claims"] is False


def test_event_audit_quantifies_minimum_distinct_events_lost_without_index(tmp_path):
    path = tmp_path / "raw.csv"
    _raw_event_rows(include_event_index=False).to_csv(path, index=False)

    audit = audit_event_identity(path)

    assert audit["status"] == "invalid_missing_event_index"
    assert audit["rows"] == 3
    assert audit["unique_transaction_hashes"] == 1
    assert audit["exact_duplicate_rows"] == 1
    assert audit["minimum_distinct_events_lost_by_hash_dedupe"] == 1
    assert audit["safe_event_dedupe_possible"] is False


@pytest.mark.parametrize("column", ["evt_tx_hash", "evt_index"])
def test_event_audit_rejects_whitespace_only_identity(tmp_path, column):
    rows = _raw_event_rows()
    rows[column] = rows[column].astype(object)
    rows.loc[0, column] = "   "
    path = tmp_path / "blank_identity.csv"
    rows.to_csv(path, index=False)

    audit = audit_event_identity(path)

    assert audit["null_event_identity_rows"] == 1
    assert audit["status"] != "valid_event_identity"
    assert audit["safe_event_dedupe_possible"] is False


def test_injection_audit_detects_sender_reuse_across_instances(tmp_path):
    injected = pd.DataFrame(
        {
            "sender": ["0xreused", "0xreused", "0xindependent"],
            "is_injected": [True, True, True],
            "attack_chain": ["CHAIN_1", "CHAIN_1", "CHAIN_2"],
            "attack_instance": ["one", "two", "one"],
        }
    )
    path = tmp_path / "injected.parquet"
    injected.to_parquet(path, index=False)

    audit = audit_injection_sender_uniqueness(path)

    assert audit["status"] == "invalid_pseudoreplication"
    assert audit["unique_senders"] == 2
    assert audit["senders_reused_across_instances"] == 1
    assert audit["independent_attack_population_established"] is False
    assert audit["external_validity_established"] is False


def test_audit_sections_are_deterministic_json(tmp_path):
    path = tmp_path / "raw.csv"
    _raw_event_rows(include_event_index=False).to_csv(path, index=False)

    first = json.dumps(audit_event_identity(path), sort_keys=True)
    second = json.dumps(audit_event_identity(path), sort_keys=True)

    assert first == second


def test_validate_precision_compatibility_wrapper_forwards_audit_cli(monkeypatch, capsys):
    forwarded: list[list[str] | None] = []

    def fake_audit_main(argv: list[str] | None = None) -> int:
        forwarded.append(argv)
        return 7

    monkeypatch.setattr(validate_precision, "audit_main", fake_audit_main)

    result = validate_precision.main(["--strict", "--scores", "scores.csv"])

    assert result == 7
    assert forwarded == [["--strict", "--scores", "scores.csv"]]
    warning = capsys.readouterr().err.lower()
    assert "superseded" in warning
    assert "precision" in warning
    assert "read-only" in warning
