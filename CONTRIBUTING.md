# Contributing

Thanks for contributing to `pq-ready-code-scanner`.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q
```

## Branch naming

Use simple branch names:

- `feat/...` for new features
- `fix/...` for bug fixes
- `docs/...` for documentation updates
- `chore/...` for maintenance

## Pull request checklist

- the code runs locally
- tests pass with `pytest -q`
- the README is updated when behavior changes
- new rules include at least one test
- sample output still makes sense

## Commit message examples

- `feat: add tls detection rule`
- `fix: avoid duplicate findings`
- `docs: explain scan severity levels`
