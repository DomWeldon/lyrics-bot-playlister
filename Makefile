help:
	@echo "Usage:"
	@echo "    make help             prints this help."
	@echo "    make fix              fix formatting and import sort ordering."
	@echo "    make format           run the format checker (black)."
	@echo "    make lint             run the linter (flake8)."
	@echo "    make setup            set up/update the local dev env."
	@echo "    make sort             run the sort checker (isort)."
	@echo "    make test             run the test suite."


.PHONY: fix
fix:
	poetry run black lyrics_bot_playlister tests
	poetry run isort .

.PHONY: format
format:
	@echo "Running black" && poetry run black --check lyrics_bot_playlister tests || exit 1

.PHONY: lint
lint:
	@echo "Running flake8" && poetry run flake8 lyrics_bot_playlister tests || exit 1

.PHONY: setup
setup:
	poetry install
	poetry run pre-commit install

.PHONY: sort
sort:
	@echo "Running Isort" && poetry run isort . --check-only --diff || exit 1

.PHONY: check
check:
	@echo "Running MyPy" && poetry run mypy lyrics_bot_playlister || exit 1

.PHONY: test
test:
	poetry run py.test tests

.PHONY: repl
repl:
	poetry run bpython
