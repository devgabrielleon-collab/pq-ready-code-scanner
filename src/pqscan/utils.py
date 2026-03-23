from __future__ import annotations

import html
from pathlib import Path

from .models import SEVERITY_ORDER


def severity_meets_threshold(finding_severity: str, threshold: str) -> bool:
    return SEVERITY_ORDER[finding_severity] >= SEVERITY_ORDER[threshold]



def is_supported_file(path: Path, supported_extensions: set[str]) -> bool:
    if path.is_dir():
        return False
    if path.suffix.lower() in supported_extensions:
        return True
    return path.name.lower() in {"ssh_config", "sshd_config", "dockerfile"}



def safe_read_text(path: Path) -> str | None:
    for encoding in ("utf-8", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
        except OSError:
            return None
    return None



def html_escape(value: str) -> str:
    return html.escape(value, quote=True)
