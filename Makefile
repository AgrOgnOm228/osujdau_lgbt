SHELL := /bin/bash

.PHONY: requirements
requirements: pyproject.toml
	uv lock
	uv sync
	uv sync --group dev


.PHONY: requirements_without_dev
requirements_without_dev: pyproject.toml
	uv sync


# --- QA ---

.PHONY: ruff
ruff: requirements
	uv run ruff check . $(ARGS)

.PHONY: mypy
mypy: requirements
	uv run mypy . $(ARGS)
