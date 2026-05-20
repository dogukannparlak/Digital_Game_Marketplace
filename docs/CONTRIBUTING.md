# Contributing

Thanks for your interest in Digital Game Marketplace.

## Getting started

1. Fork the repository
2. Clone your fork and create a branch: `git checkout -b feature/your-change`
3. Follow [INSTALLATION.md](INSTALLATION.md) for local setup
4. Run tests before opening a PR: `pytest`

## Code style

- **Python**: PEP 8, type hints where helpful, docstrings on public endpoints
- **JavaScript/React**: functional components, hooks for shared state
- Keep router logic in `backend/routers/`; avoid duplicating business rules in tests

## Pull requests

- One logical change per PR
- Update docs if you change API behavior or setup steps
- Link related issues when applicable

## Reporting issues

Open a [GitHub issue](https://github.com/dogukannparlak/Digital_Game_Marketplace/issues) with:

- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python/Node versions)
