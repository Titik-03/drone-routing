PYTHON = python3
MAIN_SCRIPT = main.py
MAP ?= maps/easy/01_linear_path.txt 

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN_SCRIPT) $(MAP)

debug:
	$(PYTHON) -m pdb $(MAIN_SCRIPT) $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .mypy_cache
	rm -rf .pytest_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict