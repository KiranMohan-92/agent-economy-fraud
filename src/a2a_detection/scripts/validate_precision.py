"""Compatibility entry point for the superseded precision-validation command.

The historical command treated registry owners as agents and counterparties as
verified humans, rewrote result files, and reported precision/FPR as if outcome
ground truth existed. Those semantics are invalid. This module now delegates to
the deterministic, read-only research-artifact audit and makes no precision,
fraud, or operational claim.

Use ``python -m a2a_detection.scripts.audit_research_claims --help`` for the
authoritative interface. The old module name is retained only so existing
automation fails honestly rather than silently reproducing misleading output.
"""

from __future__ import annotations

import sys

from a2a_detection.scripts.audit_research_claims import main as audit_main


def main(argv: list[str] | None = None) -> int:
    """Run the research-artifact audit under the deprecated command name."""
    sys.stderr.write(
        "validate_precision is superseded: registry proxy/unknown labels do not "
        "support precision or false-positive-rate claims. Running the read-only "
        "research audit instead.\n"
    )
    return audit_main(argv)


if __name__ == "__main__":
    sys.exit(main())
