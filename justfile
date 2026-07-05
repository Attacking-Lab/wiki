unexport VIRTUAL_ENV

# List available recipes
default:
    @just --list

# Install dependencies
sync:
    uv sync

# Serve the docs locally with live reload (override port: just serve 9000)
serve port="8000":
    uv run mkdocs serve --dev-addr localhost:{{ port }}

# Build the static site into ./site
build:
    uv run mkdocs build

# Build with strict link/nav validation (fails on warnings)
build-strict:
    uv run mkdocs build --strict

# Regenerate the ATKLAB v2 scoring chart datasets from meta/atklabv2.py
data:
    uv run python meta/atklabv2.py jeopardy > docs/assets/data/atklabv2_jeopardy.json
    uv run python meta/atklabv2.py all      > docs/assets/data/atklabv2_all.json
    uv run python meta/atklabv2.py single   > docs/assets/data/atklabv2_single.json

# Format Python source files
format:
    uvx ruff format .

# Lint Python source files and apply safe fixes
lint:
    uvx ruff check --fix .

# Run all checks: format, lint, and a build
check: format lint build

# Remove build artifacts and caches
clean:
    rm -rf site .ruff_cache
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
