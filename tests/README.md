# TaskFlow Application Tests

This directory contains the comprehensive test suite for the TaskFlow application.

## Test Organization

The tests are organized by functionality:

- `test_api_endpoints.py` - Tests for API endpoints and basic functionality
- `test_mcp_functions.py` - Tests for MCP (Model Context Protocol) functions
- `test_api_routes.py` - Tests for API routes and authentication
- `test_middleware.py` - Tests for application middleware (rate limiting)
- `test_auth.py` - Tests for authentication functionality
- `test_ai_agent.py` - Tests for AI agent functionality
- `test_task_handler.py` - Tests for task handling functionality
- `test_config.py` - Tests for configuration management
- `test_app.py` - Tests for the FastAPI application instance
- `test_environment.py` - Tests for the testing environment

## Running Tests

### Prerequisites

Make sure you have the required dependencies installed:

```bash
pip install -r tests/requirements.txt
```

### Running All Tests

To run all tests:

```bash
python -m pytest tests/
```

Or use the test runner:

```bash
python tests/run_tests.py
```

### Running Specific Tests

To run a specific test file:

```bash
python -m pytest tests/test_api_endpoints.py
```

### Running with Coverage

To run tests with coverage report:

```bash
python -m pytest tests/ --cov=backend --cov-report=html
```

### Running with Verbose Output

To run tests with detailed output:

```bash
python -m pytest tests/ -v
```

## Test Types

The test suite includes:

1. **Unit Tests** - Testing individual functions and methods
2. **Integration Tests** - Testing how components work together
3. **API Tests** - Testing API endpoints and responses
4. **Functional Tests** - Testing complete user workflows
5. **Environment Tests** - Testing the test environment itself

## Test Structure

Each test file follows the pytest conventions:

- Test functions start with `test_`
- Use pytest fixtures for setup/teardown
- Use descriptive names for test functions
- Include assertions to verify expected behavior

## Continuous Integration

The tests are designed to work with CI/CD pipelines and can be integrated with services like GitHub Actions, GitLab CI, or Jenkins.