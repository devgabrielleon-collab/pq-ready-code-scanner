from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from .models import ScanResult
from .utils import html_escape


def write_json_report(result: ScanResult, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "report.json"
    output_path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
    return output_path



def write_html_report(result: ScanResult, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "report.html"
    severity_counts = Counter(f.severity for f in result.findings)
    category_counts = Counter(f.category for f in result.findings)

    rows = []
    for finding in result.findings:
        rows.append(
            f"""
            <tr>
                <td>{html_escape(finding.severity)}</td>
                <td>{html_escape(finding.category)}</td>
                <td>{html_escape(finding.rule_id)}</td>
                <td>{html_escape(finding.title)}</td>
                <td>{html_escape(finding.file_path)}</td>
                <td>{finding.line_number}</td>
                <td><code>{html_escape(finding.match_text)}</code></td>
                <td>{html_escape(finding.description)}</td>
                <td>{html_escape(finding.recommendation)}</td>
            </tr>
            """.strip()
        )

    severity_list = "".join(
        f"<li><strong>{html_escape(level.title())}</strong>: {count}</li>"
        for level, count in sorted(severity_counts.items(), key=lambda x: x[0])
    )
    category_list = "".join(
        f"<li><strong>{html_escape(category)}</strong>: {count}</li>"
        for category, count in sorted(category_counts.items())
    )

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>pq-ready-code-scanner report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #1b1f23; }}
    h1, h2 {{ margin-bottom: 0.4rem; }}
    .cards {{ display: flex; gap: 16px; flex-wrap: wrap; margin: 16px 0 24px; }}
    .card {{ border: 1px solid #d0d7de; border-radius: 12px; padding: 16px; min-width: 220px; background: #f6f8fa; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
    th, td {{ border: 1px solid #d0d7de; padding: 10px; vertical-align: top; text-align: left; }}
    th {{ background: #f6f8fa; position: sticky; top: 0; }}
    code {{ background: #f6f8fa; padding: 2px 6px; border-radius: 6px; }}
    .severity-critical {{ color: #b00020; font-weight: 700; }}
    .severity-high {{ color: #c76b00; font-weight: 700; }}
    .severity-medium {{ color: #005cc5; font-weight: 700; }}
    .severity-low {{ color: #22863a; font-weight: 700; }}
  </style>
</head>
<body>
  <h1>pq-ready-code-scanner report</h1>
  <p><strong>Target:</strong> {html_escape(result.target_path)}</p>
  <div class="cards">
    <div class="card"><strong>Files scanned</strong><br>{result.files_scanned}</div>
    <div class="card"><strong>Total findings</strong><br>{len(result.findings)}</div>
    <div class="card"><strong>Supported extensions</strong><br>{len(result.supported_extensions)}</div>
  </div>

  <h2>Findings by severity</h2>
  <ul>{severity_list or '<li>No findings</li>'}</ul>

  <h2>Findings by category</h2>
  <ul>{category_list or '<li>No findings</li>'}</ul>

  <h2>Detailed findings</h2>
  <table>
    <thead>
      <tr>
        <th>Severity</th>
        <th>Category</th>
        <th>Rule</th>
        <th>Title</th>
        <th>File</th>
        <th>Line</th>
        <th>Evidence</th>
        <th>Description</th>
        <th>Recommendation</th>
      </tr>
    </thead>
    <tbody>
      {' '.join(rows) if rows else '<tr><td colspan="9">No findings.</td></tr>'}
    </tbody>
  </table>
</body>
</html>
""".strip()
    output_path.write_text(html, encoding="utf-8")
    return output_path
