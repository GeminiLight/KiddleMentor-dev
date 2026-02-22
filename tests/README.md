# GenMentor Test Suite

Comprehensive test suite for the GenMentor AI-powered learning platform.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and pytest configuration
├── unit/                    # Unit tests for individual components
│   ├── test_config.py       # Configuration management tests
│   ├── test_schemas.py      # Schema validation tests
│   ├── test_base_agent.py   # BaseAgent tests
│   ├── test_llm_factory.py  # LLM factory tests
│   └── test_utils.py        # Utility function tests
├── integration/             # Integration tests for agents
│   ├── test_content_agents.py     # Content generation agents
│   ├── test_learning_agents.py    # Learning assessment agents
│   ├── test_assessment_agents.py  # Assessment agents
│   └── test_tutoring_agents.py    # Tutoring chatbot agents
└── fixtures/                # Test data and fixtures
```

## Running Tests

### Install Test Dependencies

```bash
# Install production + test dependencies
pip install -r requirements.txt

# Or install development dependencies
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=gen_mentor --cov-report=html
```

### Run Specific Test Categories

```bash
# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run specific test file
pytest tests/unit/test_config.py

# Run specific test class
pytest tests/unit/test_config.py::TestConfigLoader

# Run specific test function
pytest tests/unit/test_config.py::TestConfigLoader::test_load_config_from_dict
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run slow tests
pytest -m slow

# Run everything except slow tests
pytest -m "not slow"
```

## Test Configuration

Test configuration is in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow-running tests",
    "api: Tests requiring API access",
]
```

## Coverage Reports

After running tests with coverage:

```bash
pytest --cov=gen_mentor --cov-report=html
```

Open the coverage report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Writing Tests

### Unit Test Example

```python
# tests/unit/test_my_module.py
import pytest
from gen_mentor.my_module import my_function

class TestMyFunction:
    """Tests for my_function."""

    def test_basic_functionality(self):
        """Test basic functionality."""
        result = my_function("input")
        assert result == "expected_output"

    def test_edge_case(self):
        """Test edge case."""
        with pytest.raises(ValueError):
            my_function(None)
```

### Integration Test Example

```python
# tests/integration/test_my_agent.py
import pytest
from unittest.mock import MagicMock, patch

class TestMyAgent:
    """Integration tests for MyAgent."""

    @pytest.mark.integration
    def test_agent_workflow(self, mock_llm):
        """Test complete agent workflow."""
        # Your test here
        pass
```

## Fixtures

Common fixtures are defined in `conftest.py`:

- `temp_dir` - Temporary directory for tests
- `sample_config` - Sample configuration
- `sample_learner_profile` - Sample learner profile
- `sample_learning_path` - Sample learning path
- `mock_llm` - Mock LLM for testing
- `mock_llm_json` - Mock LLM with JSON responses

### Using Fixtures

```python
def test_with_fixtures(sample_config, temp_dir):
    """Test using fixtures."""
    assert sample_config.agent_defaults.model is not None
    assert temp_dir.exists()
```

## Mocking

### Mocking LLMs

```python
from unittest.mock import MagicMock, patch

def test_with_mock_llm(mock_llm):
    """Test with mocked LLM."""
    with patch('gen_mentor.agents.base_agent.BaseAgent') as mock_agent:
        mock_agent.invoke.return_value = {"result": "test"}
        # Your test here
```

### Mocking API Calls

```python
@patch('requests.get')
def test_api_call(mock_get):
    """Test with mocked API call."""
    mock_get.return_value.json.return_value = {"data": "test"}
    # Your test here
```

## Test Coverage Goals

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Key workflows covered
- **Critical Paths**: 100% coverage

## Current Test Statistics

Run to see current stats:

```bash
pytest --cov=gen_mentor --cov-report=term-missing
```

## Continuous Integration

Tests are run automatically on:
- Pull requests
- Commits to main branch
- Scheduled daily runs

## Troubleshooting

### Import Errors

If you get import errors:

```bash
# Ensure gen_mentor is importable
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or install in development mode
pip install -e .
```

### Slow Tests

Mark slow tests:

```python
@pytest.mark.slow
def test_slow_operation():
    """This test is slow."""
    pass
```

Skip slow tests:

```bash
pytest -m "not slow"
```

### API Tests

Tests requiring API access should be marked:

```python
@pytest.mark.api
def test_api_call():
    """Test requiring API access."""
    pass
```

Skip API tests:

```bash
pytest -m "not api"
```

## Best Practices

1. **Descriptive Names**: Use clear, descriptive test names
2. **Single Assertion**: Each test should test one thing
3. **Fixtures**: Use fixtures for common setup
4. **Mocking**: Mock external dependencies
5. **Documentation**: Add docstrings to test classes and methods
6. **Markers**: Use markers to categorize tests
7. **Isolation**: Tests should be independent

## Contributing

When adding new features:

1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain coverage above 80%
4. Add integration tests for new agents
5. Update this README if adding new test categories

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
