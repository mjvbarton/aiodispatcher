# Contributing to aiodispatcher

Thank you for considering contributing to **aiodispatcher**! Your help is welcome.

## How to Contribute

### 1. Fork the repository

Click the **Fork** button at the top right of the [GitHub page](https://github.com/mjvbarton/aiodispatcher).

### 2. Clone your fork

```bash
git clone https://github.com/<your-username>/aiodispatcher.git
cd aiodispatcher
```

### 3. Create a new branch

```bash
git checkout -b my-feature
```

### 4. Install dependencies

We recommend using [uv](https://github.com/astral-sh/uv):

```bash
uv venv
uv sync
```

Or with pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 5. Make your changes

- Follow [PEP 8](https://peps.python.org/pep-0008/) and use type annotations.
- Run `ruff` to lint and format your code.
- Add or update unit tests in `tests/unit/` and integration tests in `tests/integration/`.
- Update documentation and the `CHANGELOG.md` if needed.

### 6. Run the tests

```bash
uv run pytest
```

### 7. Commit and push

```bash
git add .
git commit -m "Describe your change"
git push origin my-feature
```

### 8. Open a Pull Request

Go to your fork on GitHub and click **Compare & pull request**.

---

## Code Style

- Use [ruff](https://docs.astral.sh/ruff/) for linting and formatting.
- Use type annotations everywhere.
- Write docstrings for all public classes, functions, and type aliases.

## Tests

- All new features and bugfixes **must** include tests.
- Run `pytest` before submitting your PR.
- Place unit tests in `tests/unit/` and integration tests in `tests/integration/`.

## Reporting Issues

If you find a bug or have a feature request, please [open an issue](https://github.com/mjvbarton/aiodispatcher/issues) and provide as much detail as possible.

---

Thank you for helping make **aiodispatcher** better!
