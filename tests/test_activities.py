"""
Tests for the GET /activities endpoint.
Follows AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_get_activities_returns_all_activities(client, fresh_activities):
    """
    Test that GET /activities returns all available activities.
    
    AAA Pattern:
    - Arrange: No setup needed, activities are pre-populated
    - Act: Send GET request to /activities
    - Assert: Verify response status is 200 and all activities are returned
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify all activities are returned
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Basketball Team" in data
    assert "Tennis Club" in data
    assert "Drama Club" in data
    assert "Art Studio" in data
    assert "Debate Team" in data
    assert "Science Club" in data


def test_get_activities_response_structure(client, fresh_activities):
    """
    Test that GET /activities returns activities with correct structure.
    
    AAA Pattern:
    - Arrange: Define expected activity structure keys
    - Act: Send GET request to /activities
    - Assert: Verify each activity has required fields
    """
    # Arrange
    required_keys = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    for activity_name, activity in data.items():
        assert activity_name, "Activity name should not be empty"
        assert isinstance(activity, dict), f"Activity {activity_name} should be a dict"
        assert set(activity.keys()) == required_keys, \
            f"Activity {activity_name} is missing required keys"
        
        # Validate field types
        assert isinstance(activity["description"], str), \
            f"{activity_name} description should be string"
        assert isinstance(activity["schedule"], str), \
            f"{activity_name} schedule should be string"
        assert isinstance(activity["max_participants"], int), \
            f"{activity_name} max_participants should be int"
        assert isinstance(activity["participants"], list), \
            f"{activity_name} participants should be list"


def test_get_activities_participants_list_validity(client, fresh_activities):
    """
    Test that activities have valid participants data.
    
    AAA Pattern:
    - Arrange: Define validation rules for participants
    - Act: Send GET request to /activities
    - Assert: Verify participants are valid
    """
    # Arrange
    valid_emails = {
        "michael@mergington.edu", "daniel@mergington.edu",
        "emma@mergington.edu", "sophia@mergington.edu",
        "john@mergington.edu", "olivia@mergington.edu",
        "alex@mergington.edu", "lucas@mergington.edu",
        "noah@mergington.edu", "isabella@mergington.edu",
        "ava@mergington.edu", "mia@mergington.edu",
        "james@mergington.edu", "charlotte@mergington.edu",
        "benjamin@mergington.edu"
    }
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    for activity_name, activity in data.items():
        participants = activity.get("participants", [])
        
        # Verify participants is a list of strings
        assert isinstance(participants, list), \
            f"{activity_name} participants should be a list"
        for participant in participants:
            assert isinstance(participant, str), \
                f"{activity_name} participants should all be strings"
            assert participant in valid_emails, \
                f"{activity_name} has invalid participant email: {participant}"
        
        # Verify participants count does not exceed max
        assert len(participants) <= activity.get("max_participants", 0), \
            f"{activity_name} has more participants than max_participants"
