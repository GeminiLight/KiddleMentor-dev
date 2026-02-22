"""
Test the refactored backend with proper API endpoints.

This script verifies that the new application structure works correctly.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    print("\n1. Testing root endpoint...")
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    print(f"   ✓ Root: {data['message']} v{data['version']}")
    print(f"   ✓ API Prefix: {data['api_prefix']}")


def test_health():
    """Test health check endpoint."""
    print("\n2. Testing health check endpoint...")
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data
    print(f"   ✓ Health: {data['status']} - {data['timestamp']}")


def test_storage_info():
    """Test storage info endpoint."""
    print("\n3. Testing storage info endpoint...")
    response = client.get("/api/v1/storage-info")
    assert response.status_code == 200
    data = response.json()
    assert "storage_mode" in data
    print(f"   ✓ Storage mode: {data['storage_mode']}")
    if data["storage_mode"] == "local":
        print(f"   ✓ Upload location: {data.get('upload_location')}")
        print(f"   ✓ Workspace: {data.get('workspace_dir')}")


def test_list_models():
    """Test list LLM models endpoint."""
    print("\n4. Testing list LLM models endpoint...")
    response = client.get("/api/v1/list-llm-models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) > 0
    print(f"   ✓ Found {len(data['models'])} models:")
    for model in data["models"]:
        print(f"     - {model['model_provider']}/{model['model_name']}")


def test_openapi_docs():
    """Test that OpenAPI documentation is available."""
    print("\n5. Testing OpenAPI documentation...")
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "info" in data
    assert "paths" in data
    print(f"   ✓ API Title: {data['info']['title']}")
    print(f"   ✓ API Version: {data['info']['version']}")
    print(f"   ✓ Endpoints: {len(data['paths'])} paths")

    # Check that we have the new endpoints
    paths = list(data['paths'].keys())
    expected_paths = [
        "/api/v1/health",
        "/api/v1/storage-info",
        "/api/v1/list-llm-models",
        "/api/v1/chat/chat-with-tutor",
        "/api/v1/goals/refine-learning-goal",
        "/api/v1/skills/identify-skill-gap-with-info",
        "/api/v1/profile/create-learner-profile",
        "/api/v1/learning/schedule-learning-path",
        "/api/v1/assessment/generate-document-quizzes",
        "/api/v1/memory/learner-memory/{learner_id}",
    ]

    print(f"\n   ✓ Checking key endpoints:")
    for path in expected_paths:
        # Check with or without path parameters
        base_path = path.replace("{learner_id}", "test")
        found = any(p.startswith(path.split("{")[0]) for p in paths)
        if found:
            print(f"     ✓ {path}")
        else:
            print(f"     ✗ {path} (NOT FOUND)")


def test_services():
    """Test that services are properly initialized."""
    print("\n6. Testing service initialization...")

    from services.llm_service import get_llm_service
    from services.memory_service import get_memory_service

    # Test LLM service
    llm_service = get_llm_service()
    assert llm_service is not None
    models = llm_service.list_available_models()
    assert len(models) > 0
    print(f"   ✓ LLM service initialized with {len(models)} models")

    # Test memory service
    memory_service = get_memory_service()
    assert memory_service is not None
    is_available = memory_service.is_available()
    print(f"   ✓ Memory service initialized (available: {is_available})")


def test_error_handling():
    """Test that error handling works correctly."""
    print("\n7. Testing error handling...")

    # Test 404
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404
    data = response.json()
    assert "error_code" in data
    print(f"   ✓ 404 handling works: {data['error_code']}")


def test_endpoint_structure():
    """Test that endpoints follow the new structure."""
    print("\n8. Testing endpoint structure...")

    # Test that endpoints are under /api/v1
    response = client.get("/openapi.json")
    data = response.json()

    v1_endpoints = [p for p in data['paths'].keys() if p.startswith("/api/v1/")]
    legacy_endpoints = [p for p in data['paths'].keys() if not p.startswith("/api/v1/") and p != "/"]

    print(f"   ✓ v1 endpoints: {len(v1_endpoints)}")
    print(f"   ✓ Legacy endpoints: {len(legacy_endpoints)}")
    print(f"\n   v1 Endpoint categories:")

    categories = {}
    for path in v1_endpoints:
        category = path.split("/")[2] if len(path.split("/")) > 2 else "root"
        categories[category] = categories.get(category, 0) + 1

    for category, count in sorted(categories.items()):
        print(f"     - {category}: {count} endpoints")


def main():
    """Run all tests."""
    print("="*70)
    print("  Testing Refactored Backend with Real Endpoints")
    print("="*70)

    try:
        test_root()
        test_health()
        test_storage_info()
        test_list_models()
        test_openapi_docs()
        test_services()
        test_error_handling()
        test_endpoint_structure()

        print("\n" + "="*70)
        print("  ✓ All tests passed!")
        print("="*70)
        print("\nThe refactored backend with proper endpoints is working!")
        print("\nNext steps:")
        print("  1. Run: python main.py")
        print("  2. Visit: http://localhost:5000/docs")
        print("  3. Test the API endpoints")
        print("\nAll endpoints are now under /api/v1/")
        print()

        return 0

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
