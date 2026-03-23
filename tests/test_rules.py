from pathlib import Path

from pqscan.models import ScanContext
from pqscan.scanner import RepositoryScanner


def test_scanner_detects_rsa_and_crypto_library(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    file_path = project / "app.py"
    file_path.write_text(
        "from cryptography.hazmat.primitives.asymmetric import rsa\n"
        "KEY_TYPE = 'RSA'\n",
        encoding="utf-8",
    )

    scanner = RepositoryScanner(ScanContext(target_path=project))
    result = scanner.scan()

    rule_ids = {finding.rule_id for finding in result.findings}
    assert "PQC001" in rule_ids
    assert "PQC008" in rule_ids


def test_min_severity_filters_low_findings(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    file_path = project / "notes.txt"
    file_path.write_text("This mentions quantum-safe migration", encoding="utf-8")

    supported = project / "notes.conf"
    supported.write_text("# quantum-safe migration placeholder\n", encoding="utf-8")

    scanner = RepositoryScanner(ScanContext(target_path=project, min_severity="medium"))
    result = scanner.scan()

    assert all(finding.severity in {"medium", "high", "critical"} for finding in result.findings)
