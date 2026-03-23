from __future__ import annotations

import re
from pathlib import Path

from .models import Finding, Rule, ScanContext, ScanResult
from .rules import RULES, SUPPORTED_EXTENSIONS
from .utils import is_supported_file, safe_read_text, severity_meets_threshold


class RepositoryScanner:
    def __init__(self, context: ScanContext, rules: list[Rule] | None = None) -> None:
        self.context = context
        self.rules = rules or RULES
        self.supported_extensions = SUPPORTED_EXTENSIONS

    def scan(self) -> ScanResult:
        findings: list[Finding] = []
        files_scanned = 0

        for path in self._iter_files(self.context.target_path):
            if not is_supported_file(path, self.supported_extensions):
                continue
            text = safe_read_text(path)
            if text is None:
                continue
            files_scanned += 1
            findings.extend(self._scan_file(path, text))

        findings.sort(key=lambda f: (-self._severity_rank(f.severity), f.file_path, f.line_number, f.rule_id))
        return ScanResult(
            target_path=str(self.context.target_path),
            files_scanned=files_scanned,
            findings=findings,
            supported_extensions=sorted(self.supported_extensions),
        )

    def _iter_files(self, root: Path):
        for path in root.rglob("*"):
            if any(part in self.context.exclude_dirs for part in path.parts):
                continue
            yield path

    def _scan_file(self, path: Path, text: str) -> list[Finding]:
        findings: list[Finding] = []
        lines = text.splitlines()
        suffix = path.suffix.lower()
        pseudo_ext = suffix if suffix else path.name.lower()

        for rule in self.rules:
            if not self._rule_applies(rule, pseudo_ext):
                continue
            pattern = re.compile(rule.pattern, rule.flags)
            for line_number, line in enumerate(lines, start=1):
                for match in pattern.finditer(line):
                    finding = Finding(
                        rule_id=rule.id,
                        title=rule.title,
                        description=rule.description,
                        severity=rule.severity,
                        category=rule.category,
                        recommendation=rule.recommendation,
                        file_path=str(path),
                        line_number=line_number,
                        line_text=line.strip(),
                        match_text=match.group(0),
                    )
                    if severity_meets_threshold(finding.severity, self.context.min_severity):
                        findings.append(finding)
        return self._deduplicate(findings)

    @staticmethod
    def _rule_applies(rule: Rule, file_ext: str) -> bool:
        return "*" in rule.applies_to or file_ext in rule.applies_to

    @staticmethod
    def _severity_rank(severity: str) -> int:
        order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        return order[severity]

    @staticmethod
    def _deduplicate(findings: list[Finding]) -> list[Finding]:
        seen: set[tuple[str, int, str, str]] = set()
        deduped: list[Finding] = []
        for finding in findings:
            key = (finding.file_path, finding.line_number, finding.rule_id, finding.match_text.lower())
            if key in seen:
                continue
            seen.add(key)
            deduped.append(finding)
        return deduped
