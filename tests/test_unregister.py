"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
Follows AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_unregister_student_success(client, fresh_activities, test_student_email):
    """
    Test successful unregistration of a student from an activity.
    
    AAA Pattern:
    - Arrange: Sign up student first, then prepare unregister request
    - Act: Send DELETE request to unregister endpoint
    - Assert: Verify 200 status, participant removed, and correct message
    """
    # Arrange
    activity_name = "Chess Club"
    email = test_student_email
    
    # First, sign up the student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Unregistered {email} from {activity_name}"
    
    # Verify participant was removed from activity
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_activity_not_found(client, fresh_activities, test_student_email):
    """
    Test unregister from non-existent activity returns 404.
    
    AAA Pattern:
    - Arrange: Prepare non-existent activity name
    - Act: Send DELETE request with invalid activity
    - Assert: Verify 404 status code and error detail
    """
    # Arrange
    activity_name = "Non-Existent Activity"
    email = test_student_email
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_student_not_signed_up(client, fresh_activities, test_student_email):
    """
    Test unregister when student is not signed up returns 400.
    
    AAA Pattern:
    - Arrange: Use student email not signed up for activity
    - Act: Send DELETE request with non-participant
    - Assert: Verify 400 status code and error detail
    """
    # Arrange
    activity_name = "Chess Club"
    email = test_student_email  # Not in default participants
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student is not signed up for this activity"


def test_unregister_existing_student(client, fresh_activities, existing_student_email):
    """
    Test unregister of a student already in participants list.
    
    AAA Pattern:
    - Arrange: Use email already in Chess Club participants
    - Act: Send DELETE request to unregister
    - Assert: Verify 200 status and participant removed
    """
    # Arrange
    activity_name = "Chess Club"
    email = existing_student_email  # michael@mergington.edu
    
    # Verify student is initially signed up
    activities_response = client.get("/activities")
    initial_participants = activities_response.json()[activity_name]["participants"]
    assert email in initial_participants
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    final_participants = activities_response.json()[activity_name]["participants"]
    assert email not in final_participants
    assert len(final_participants) == len(initial_participants) - 1


def test_unregister_multiple_times_fails(client, fresh_activities, test_student_email):
    """
    Test that unregistering twice fails on the second attempt.
    
    AAA Pattern:
    - Arrange: Sign up student, then unregister once (successful)
    - Act: Send DELETE request again (should fail)
    - Assert: Verify 400 status on second unregister attempt
    """
    # Arrange
    activity_name = "Programming Class"
    email = test_student_email
    
    # Sign up
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Unregister first time (should succeed)
    response_first = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert response_first.status_code == 200
    
    # Act: Try to unregister second time
    response_second = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response_second.status_code == 400
    data = response_second.json()
    assert data["detail"] == "Student is not signed up for this activity"
