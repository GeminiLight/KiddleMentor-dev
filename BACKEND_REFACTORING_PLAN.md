# Backend Refactoring Plan

## Current Issues

1. **Monolithic Structure**: All code (815 lines) in single `main.py` file
2. **Missing Type Safety**: Schema definitions not properly imported
3. **No Separation of Concerns**: API routes, business logic, and configuration mixed together
4. **No Dependency Injection**: Direct instantiation of services throughout
5. **Limited Error Handling**: Basic try-catch blocks without structured error responses
6. **No Request Validation**: Missing input validation and sanitization
7. **No API Versioning**: All endpoints at root level

## Proposed Structure

```
apps/backend/
├── README.md
├── main.py                          # Application entry point (minimal)
├── config.py                        # Configuration management
├── dependencies.py                  # Dependency injection
├── exceptions.py                    # Custom exceptions
├── middleware/                      # Middleware components
│   ├── __init__.py
│   ├── error_handler.py            # Global error handling
│   ├── logging.py                  # Request/response logging
│   └── cors.py                     # CORS configuration
├── models/                          # Request/response models
│   ├── __init__.py
│   ├── requests.py                 # Request schemas
│   ├── responses.py                # Response schemas
│   └── common.py                   # Common/shared models
├── api/                            # API routes
│   ├── __init__.py
│   ├── v1/                         # Version 1 API
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py             # Chat endpoints
│   │   │   ├── profile.py          # Profile management
│   │   │   ├── goals.py            # Goal refinement
│   │   │   ├── skills.py           # Skill gap identification
│   │   │   ├── learning_path.py    # Learning path management
│   │   │   ├── content.py          # Content generation
│   │   │   ├── assessment.py       # Quiz generation
│   │   │   ├── memory.py           # Memory/context endpoints
│   │   │   └── system.py           # System info endpoints
│   │   └── router.py               # v1 router aggregation
│   └── deps.py                     # API dependencies
├── services/                       # Business logic layer
│   ├── __init__.py
│   ├── llm_service.py              # LLM operations
│   ├── profile_service.py          # Profile management
│   ├── learning_service.py         # Learning path operations
│   ├── content_service.py          # Content generation
│   ├── memory_service.py           # Memory operations
│   └── storage_service.py          # File storage operations
├── core/                           # Core utilities
│   ├── __init__.py
│   ├── security.py                 # Security utilities
│   ├── validators.py               # Input validation
│   └── formatters.py               # Data formatting
└── tests/                          # Tests
    ├── __init__.py
    ├── conftest.py                 # Pytest configuration
    ├── test_api/
    │   ├── test_chat.py
    │   ├── test_profile.py
    │   └── test_memory.py
    └── test_services/
        ├── test_llm_service.py
        └── test_memory_service.py
```

## Key Improvements

### 1. Layered Architecture
- **API Layer**: Request handling, validation, HTTP concerns
- **Service Layer**: Business logic, orchestration
- **Core Layer**: Shared utilities, helpers

### 2. Dependency Injection
- Services injected via FastAPI dependencies
- Easy testing with mock dependencies
- Clear dependency graph

### 3. Proper Error Handling
- Custom exception hierarchy
- Structured error responses
- Automatic HTTP status code mapping

### 4. API Versioning
- `/api/v1/` prefix for all endpoints
- Easy to add v2 without breaking v1

### 5. Type Safety
- Proper Pydantic models for all requests/responses
- Type hints throughout
- Runtime validation

### 6. Testability
- Service layer can be unit tested
- API layer can be integration tested
- Clear separation makes mocking easy

### 7. Configuration Management
- Environment-based configuration
- Validation of required settings
- Easy to switch between dev/staging/prod

## Migration Strategy

### Phase 1: Create New Structure (No Breaking Changes)
1. Create new directory structure
2. Move schemas to `models/`
3. Extract services from `main.py`
4. Create new API route modules
5. Keep old `main.py` as reference

### Phase 2: Implement Core Services
1. Implement `llm_service.py`
2. Implement `memory_service.py`
3. Implement `storage_service.py`
4. Implement `profile_service.py`
5. Implement `learning_service.py`
6. Implement `content_service.py`

### Phase 3: Create API Endpoints
1. Implement endpoints in new structure
2. Add proper validation
3. Add error handling
4. Add tests

### Phase 4: Switch to New Structure
1. Update `main.py` to use new routes
2. Run tests to verify functionality
3. Update documentation
4. Remove old code

### Phase 5: Enhancements
1. Add authentication/authorization
2. Add rate limiting
3. Add caching
4. Add monitoring/metrics
5. Add API documentation (Swagger)

## Benefits

1. **Maintainability**: Easy to find and modify code
2. **Testability**: Each component can be tested independently
3. **Scalability**: Easy to add new features without bloating existing files
4. **Team Collaboration**: Multiple developers can work on different modules
5. **Code Quality**: Clear separation of concerns and single responsibility
6. **Documentation**: Self-documenting structure with clear module purposes

## Implementation Priority

1. ✅ **High Priority**: Core structure, services, error handling
2. ⬜ **Medium Priority**: API endpoints, validation, tests
3. ⬜ **Low Priority**: Advanced features, monitoring, optimization

## Backward Compatibility

- Maintain existing API endpoints during migration
- Add deprecation warnings to old endpoints
- Provide migration guide for clients
- Keep old endpoints for 1-2 versions before removal
