"""
Pytest configuration and shared fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient instance for testing.
    Creates a fresh client for each test to ensure isolation.
    """
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """
    Reset activities to initial state before each test.
    This ensures test isolation by providing a clean state.
    """
    # Store original state
    original_state = {
        activity_name: {
            "description": activity.get("description"),
            "schedule": activity.get("schedule"),
            "max_participants": activity.get("max_participants"),
            "participants": activity.get("participants", []).copy()
        }
        for activity_name, activity in activities.items()
    }
    
    yield
    
    # Restore original state after test
    for activity_name, activity_data in original_state.items():
        if activity_name in activities:
            activities[activity_name]["participants"] = activity_data["participants"].copy()


@pytest.fixture
def test_student_email():
    """Provide a test student email that is not in default activities."""
    return "test.student@mergington.edu"


@pytest.fixture
def existing_student_email():
    """Provide an email of a student already signed up for Chess Club."""
    return "michael@mergington.edu"
