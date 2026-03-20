import pytest
from copy import deepcopy
from src.app import app, activities
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore in-memory activities state before each test."""
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


@pytest.fixture
def client():
    return TestClient(app)
