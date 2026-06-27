# Notation Conventions

## Domain-Specific Notes

This research is not a traditional physics problem but rather an analysis of agent-to-agent commerce and fraud detection systems. Conventions from physics (metric signature, Fourier transforms, etc.) are not directly applicable.

## Relevant Conventions

### Time Notation
- Transaction timestamps: ISO 8601 format (e.g., `2026-03-16T01:00:00Z`)
- Time intervals: Use SI units (seconds, minutes, hours) or descriptive terms

### Agent Notation
- Agent transactions: `A → B` denotes agent A sending to agent B
- Agent sets: `𝔸` denotes set of agents, `|𝔸|` denotes cardinality

### Transaction Notation
- Transaction velocity: `v` (transactions per unit time)
- Detection latency: `τ` (time from transaction to detection)
- Fraud probability: `P(fraud|pattern)` conditional probability

### References
- OpenClaw platform: `ref-openclaw-docs`
- Moltbook platform: `ref-moltbook-docs`
- Academic literature: `ref-agent-econ-lit` (to be expanded during Phase 1)

## Unit System

No natural units. Use standard SI units for:
- Time: seconds (s), minutes (min), hours (h)
- Data: bytes (B), megabytes (MB)
- Transaction rates: transactions per second (tx/s)

## Custom Conventions

- Hard-to-vary criterion: From Deutsch's epistemology — explanation quality test
- Invariant mapping: Human invariant → Agent violation relationship
