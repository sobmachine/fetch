# === Variables ===
PACKAGE_NAME=fetch
SRC_DIR=src
PYTHON=python3
VENV_DIR=.venv

# === Targets ===

# Install dependencies in a virtual environment
.PHONY: install
install:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r requirements.txt

# Run the script
.PHONY: run
run:
	$(VENV_DIR)/bin/python $(SRC_DIR)/main.py $(ARGS)

# Build distribution (wheel + sdist)
.PHONY: build
build:
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build

# Install package locally (editable)
.PHONY: develop
develop:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .

# Clean build artifacts
.PHONY: clean
clean:
	rm -rf build dist *.egg-info __pycache__ $(VENV_DIR)

# Test if script runs
.PHONY: test
test:
	$(MAKE) install
	$(MAKE) run ARGS="tests/test_image.png"
