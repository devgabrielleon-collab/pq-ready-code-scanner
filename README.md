# pq-ready-code-scanner 🛡️

[![CI](https://github.com/devgabrielleon-collab/pq-ready-code-scanner/actions/workflows/ci.yml/badge.svg)](https://github.com/devgabrielleon-collab/pq-ready-code-scanner/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Static discovery of quantum-vulnerable cryptography in code, configs, and certificates.**

`pq-ready-code-scanner` is a developer-friendly CLI tool designed to scan source code and infrastructure files for cryptographic algorithms that may require review during post-quantum migration planning.

## 🚀 Quick Start

### 1. Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/devgabrielleon-collab/pq-ready-code-scanner.git
cd pq-ready-code-scanner
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### 2. Run a Scan

Scan a directory for quantum-vulnerable cryptography:

```bash
pqscan scan ./samples/demo_vulnerable --output ./out
```

## 🔍 What it Scans

The scanner inspects various file types (Python, JS, Java, Go, YAML, JSON, etc.) for:
- **Public-Key Algorithms**: RSA, ECC, ECDSA, ECDH, DH, DSA.
- **Legacy TLS**: Versions below TLS 1.3.
- **SSH Algorithms**: Non-PQC compliant algorithms.
- **Certificate Material**: PEM, CRT, and KEY files.

## 📊 Outputs

The tool generates two types of reports in the specified output directory:
- `report.json`: Structured data for integration with other tools.
- `report.html`: A human-readable dashboard with findings and recommendations.

## 🛠️ Development

### Running Tests
```bash
pip install -e .[dev]
pytest tests/ -v
```

### CI/CD
This project uses **GitHub Actions** for Continuous Integration. Every push to `main` triggers an automated test suite across multiple Python versions.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built for post-quantum readiness planning.*
