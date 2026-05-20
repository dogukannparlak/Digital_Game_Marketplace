# Testing

## Prerequisites

```bash
pip install -r requirements.txt
```

## Run tests

From the project root:

```bash
pytest
```

With coverage:

```bash
pytest --cov=backend --cov-report=term-missing
```

## Layout

| Path | Focus |
|------|--------|
| `tests/test_cart.py` | Cart add, checkout, totals |
| `tests/test_orders.py` | Orders, library, ownership |
| `tests/test_games_search_filter.py` | Store listing, search, filters |
| `tests/test_purchase_service.py` | Purchase flow via orders router |
| `tests/test_admin.py` | Admin moderation |
| `tests/conftest.py` | Shared fixtures and mocks |

## Conventions

- Unit tests mock the SQLAlchemy session; no live database required
- Use `@pytest.mark.unit` for fast router-level tests
- Docstrings describe behavior in plain language (no checklist emoji prefixes)

## CI

Add a workflow step that runs `pytest` on push/PR. Example:

```yaml
- run: pip install -r requirements.txt
- run: pytest
```
