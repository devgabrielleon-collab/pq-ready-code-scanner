from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .models import ScanContext
from .reporting import write_html_report, write_json_report
from .scanner import RepositoryScanner

app = typer.Typer(help="Static discovery of quantum-vulnerable cryptography in code, configs, and certificates.", no_args_is_help=True)
console = Console()


@app.callback()
def main() -> None:
    """pqscan command group."""


@app.command()
def scan(
    target: str = typer.Argument(..., help="Path to the repository or directory to scan."),
    output: str = typer.Option("./out", "--output", "-o", help="Directory where reports will be written."),
    min_severity: str = typer.Option(
        "low",
        "--min-severity",
        help="Minimum severity to include: low, medium, high, critical.",
        case_sensitive=False,
    ),
) -> None:
    target_path = Path(target).resolve()
    output_dir = Path(output).resolve()

    if not target_path.exists():
        raise typer.BadParameter(f"Target path does not exist: {target}")

    valid_levels = {"low", "medium", "high", "critical"}
    min_severity = min_severity.lower()
    if min_severity not in valid_levels:
        raise typer.BadParameter("--min-severity must be one of: low, medium, high, critical")

    context = ScanContext(target_path=target_path, min_severity=min_severity)
    scanner = RepositoryScanner(context)
    result = scanner.scan()

    json_path = write_json_report(result, output_dir)
    html_path = write_html_report(result, output_dir)

    summary = Table(title="Scan Summary")
    summary.add_column("Metric")
    summary.add_column("Value")
    summary.add_row("Scanned path", str(result.target_path))
    summary.add_row("Files inspected", str(result.files_scanned))
    summary.add_row("Findings", str(len(result.findings)))
    summary.add_row("JSON report", str(json_path))
    summary.add_row("HTML report", str(html_path))
    console.print(summary)


if __name__ == "__main__":
    app()
