# Test Structure Visualization

```
tests/
├── __init__.py                           # Test package init
├── conftest.py                           # Shared fixtures (14 fixtures)
├── README.md                             # Test documentation
│
├── unit/                                 # Unit tests (61+ tests)
│   ├── __init__.py
│   ├── test_config.py                    # Configuration tests (2 classes, 10 tests)
│   ├── test_schemas.py                   # Schema validation (4 classes, 15 tests)
│   ├── test_base_agent.py                # BaseAgent tests (1 class, 10 tests)
│   ├── test_llm_factory.py               # LLM factory tests (1 class, 8 tests)
│   └── test_utils.py                     # Utility tests (2 classes, 8 tests)
│
└── integration/                          # Integration tests (13+ tests)
    ├── __init__.py
    ├── test_content_agents.py            # Content agents (1 class, 3 tests)
    ├── test_learning_agents.py           # Learning agents (1 class, 3 tests)
    ├── test_assessment_agents.py         # Assessment agents (1 class, 4 tests)
    └── test_tutoring_agents.py           # Tutoring agents (1 class, 3 tests)

Root Level Files:
├── pyproject.toml                        # Pytest configuration
├── Makefile                              # Test commands
├── TESTING.md                            # Complete testing guide
├── TEST_SUITE_SUMMARY.md                 # Test suite overview
├── requirements.txt                      # Dependencies (with test deps)
├── requirements-dev.txt                  # Development dependencies
└── .github/workflows/tests.yml           # CI/CD configuration
```

## Test Coverage by Module

### Configuration (test_config.py)
- TestConfigLoader (7 tests)
- TestAppConfig (4 tests)

### Schemas (test_schemas.py)
- TestContentSchemas (4 tests)
- TestLearningSchemas (4 tests)
- TestTutoringSchemas (3 tests)
- TestAssessmentSchemas (3 tests)
- TestSchemaValidation (3 tests)

### BaseAgent (test_base_agent.py)
- TestBaseAgent (10 tests)

### LLM Factory (test_llm_factory.py)
- TestLLMFactory (8 tests)

### Utilities (test_utils.py)
- TestLLMOutput (4 tests)
- TestPreprocess (4 tests)

### Content Agents (test_content_agents.py)
- TestContentAgents (3 tests)

### Learning Agents (test_learning_agents.py)
- TestLearningAgents (3 tests)

### Assessment Agents (test_assessment_agents.py)
- TestAssessmentAgents (4 tests)

### Tutoring Agents (test_tutoring_agents.py)
- TestTutoringAgents (3 tests)

## Total Statistics

- **Test Files**: 9
- **Test Classes**: 16
- **Total Tests**: 74+
- **Fixtures**: 14
- **Documentation Files**: 4

## Commands Quick Reference

```bash
# Run all tests
make test
pytest

# Run unit tests
make test-unit
pytest tests/unit/

# Run integration tests
make test-integration
pytest tests/integration/

# Run with coverage
make test-cov
pytest --cov=gen_mentor --cov-report=html

# Run specific file
pytest tests/unit/test_config.py -v

# Run by marker
pytest -m unit
pytest -m integration
```
