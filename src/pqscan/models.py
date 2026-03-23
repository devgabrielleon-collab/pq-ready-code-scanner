from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


SEVERITY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


@dataclass(slots=True)
class Rule:
    id: str
    title: str
    description: str
    pattern: str
    severity: str
    category: str
    recommendation: str
    applies_to: tuple[str, ...] = field(default_factory=tuple)
    flags: int = 0


@dataclass(slots=True)
class Finding:
    rule_id: str
    title: str
    description: str
    severity: str
    category: str
    recommendation: str
    file_path: str
    line_number: int
    line_text: str
    match_text: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ScanResult:
    target_path: str
    files_scanned: int
    findings: list[Finding]
    supported_extensions: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_path": self.target_path,
            "files_scanned": self.files_scanned,
            "findings_count": len(self.findings),
            "supported_extensions": self.supported_extensions,
            "findings": [finding.to_dict() for finding in self.findings],
        }


@dataclass(slots=True)
class ScanContext:
    target_path: Path
    min_severity: str = "low"
    exclude_dirs: tuple[str, ...] = (
        ".git",
        "node_modules",
        ".venv",
        "venv",
        "dist",
        "build",
        "__pycache__",
    )
