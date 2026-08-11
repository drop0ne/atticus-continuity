"""Execute EXP-0004 conformance suites and emit a JSON evidence summary.

This runner does not write files, invoke subprocesses, or contact external systems.
Use shell redirection if you want to preserve its JSON output as an experiment artifact.
"""

from __future__ import annotations

import argparse
import io
import json
import platform
import sys
import time
import unittest
from datetime import datetime, timezone

from . import test_gateway, test_plan


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--revision",
        default="UNKNOWN",
        help="Exact repository revision being tested. Supply git commit SHA when known.",
    )
    args = parser.parse_args()

    suite = unittest.TestSuite(
        [
            unittest.defaultTestLoader.loadTestsFromModule(test_gateway),
            unittest.defaultTestLoader.loadTestsFromModule(test_plan),
        ]
    )
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)

    started = time.perf_counter()
    result = runner.run(suite)
    duration = time.perf_counter() - started

    failures = [
        {"test": str(test), "traceback": traceback}
        for test, traceback in result.failures
    ]
    errors = [
        {"test": str(test), "traceback": traceback}
        for test, traceback in result.errors
    ]
    skipped = [
        {"test": str(test), "reason": reason}
        for test, reason in getattr(result, "skipped", [])
    ]

    payload = {
        "schema": "experiment-result-v0.1",
        "experiment_ref": "EXP-0004",
        "implementation_ref": "REF-PAC-GW-0001",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "revision": args.revision,
        "runtime": {
            "language": "Python",
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "command": "python -m reference.pac_gateway.run_exp0004 --revision <REVISION>",
        "suites": [
            "reference.pac_gateway.test_gateway",
            "reference.pac_gateway.test_plan",
        ],
        "observed": {
            "tests_run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "skipped": len(skipped),
            "successful": result.wasSuccessful(),
            "duration_seconds": round(duration, 6),
        },
        "pass_criteria_met": result.wasSuccessful(),
        "failure_details": failures,
        "error_details": errors,
        "skipped_details": skipped,
        "unittest_output": stream.getvalue(),
        "limitations": [
            "Conformance tests exercise an inert local reference implementation only.",
            "A passing run is not proof of general AI alignment or production security.",
            "semantic_action_id correlation remains a trusted-orchestrator assumption in v0.1.",
            "PlanLedger aggregate checks use explicitly represented budgets and do not solve arbitrary semantic composition.",
        ],
    }

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
