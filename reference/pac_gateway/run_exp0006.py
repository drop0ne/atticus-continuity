"""Execute EXP-0006 trusted-correlation conformance tests and emit JSON evidence.

This runner is inert: it uses only synthetic in-memory authority/correlation fixtures.
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

from .test_exp0006 import TrustedCorrelationExperimentTests


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--revision",
        default="UNKNOWN",
        help="Exact repository revision being tested. Supply git commit SHA when known.",
    )
    args = parser.parse_args()

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TrustedCorrelationExperimentTests)
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
        "experiment_ref": "EXP-0006",
        "implementation_ref": "REF-PAC-GW-0001",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "revision": args.revision,
        "runtime": {
            "language": "Python",
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "command": "python -m reference.pac_gateway.run_exp0006 --revision <REVISION>",
        "suites": ["reference.pac_gateway.test_exp0006.TrustedCorrelationExperimentTests"],
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
            "The experiment tests the trusted-correlation governance interface, not upstream semantic-equivalence accuracy.",
            "A faulty trusted resolver can still under-correlate or over-correlate actions.",
            "All authority, target, and correlation objects are synthetic in-memory fixtures.",
            "Passing does not establish production security or general AI alignment.",
        ],
    }

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
