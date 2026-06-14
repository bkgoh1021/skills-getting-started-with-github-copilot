"""
Pytest configuration and shared fixtures for all tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for making requests to the FastAPI app.
    Each test gets a fresh client, but the app's in-memory database is shared.
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture that resets activities to a known state before each test.
    This ensures test isolation by providing a clean slate.
    """
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Reset the app's activities to original state
    from src.app import activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup after test (reset again to known state)
    activities.clear()
    activities.update(original_activities)
