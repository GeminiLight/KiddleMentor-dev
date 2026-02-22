.PHONY: help test test-unit test-integration test-cov clean lint format install install-dev

help:
	@echo "GenMentor Development Commands"
	@echo "=============================="
	@echo "make install       - Install production dependencies"
	@echo "make install-dev   - Install development dependencies"
	@echo "make test          - Run all tests"
	@echo "make test-unit     - Run unit tests only"
	@echo "make test-integration - Run integration tests only"
	@echo "make test-cov      - Run tests with coverage report"
	@echo "make test-fast     - Run tests excluding slow tests"
	@echo "make lint          - Run code linting"
	@echo "make format        - Format code with black and isort"
	@echo "make clean         - Clean up generated files"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-cov:
	pytest --cov=gen_mentor --cov-report=html --cov-report=term-missing -v

test-fast:
	pytest -v -m "not slow"

test-watch:
	pytest-watch

lint:
	flake8 gen_mentor tests
	mypy gen_mentor

format:
	black gen_mentor tests
	isort gen_mentor tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

# Convenience aliases
t: test
tu: test-unit
ti: test-integration
tc: test-cov
