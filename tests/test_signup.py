"""
Tests for the POST /activities/{activity_name}/signup endpoint.
Follows AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_signup_new_student_success(client, fresh_activities, test_student_email):
    """
    Test successful signup of a new student to an activity.
    
    AAA Pattern:
    - Arrange: Prepare test student email and valid activity name
    - Act: Send POST request to signup endpoint
    - Assert: Verify 200 status, response message, and participant added
    """
    # Arrange
    activity_name = "Chess Club"
    email = test_student_email
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for {activity_name}"
    
    # Verify participant was added to activity
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]


def test_signup_activity_not_found(client, fresh_activities, test_student_email):
    """
    Test signup to non-existent activity returns 404.
    
    AAA Pattern:
    - Arrange: Prepare non-existent activity name
    - Act: Send POST request to signup with invalid activity
    - Assert: Verify 404 status code and error detail
    """
    # Arrange
    activity_name = "Non-Existent Activity"
    email = test_student_email
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_student_already_signed_up(client, fresh_activities, existing_student_email):
    """
    Test signup when student is already signed up returns 400.
    
    AAA Pattern:
    - Arrange: Use email already signed up for Chess Club
    - Act: Send POST request to signup with existing participant
    - Assert: Verify 400 status code and error detail
    """
    # Arrange
    activity_name = "Chess Club"
    email = existing_student_email  # michael@mergington.edu
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


@pytest.mark.parametrize("activity_name", [
    "Chess Club",
    "Programming Class",
    "Basketball Team",
    "Tennis Club"
])
def test_signup_multiple_activities(client, fresh_activities, test_student_email, activity_name):
    """
    Test signup works for multiple different activities.
    
    AAA Pattern:
    - Arrange: Test student and parametrized activity name
    - Act: Send POST request to signup
    - Assert: Verify 200 status for all activities
    """
    # Arrange
    email = test_student_email
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert activity_name in data["message"]
    assert email in data["message"]
