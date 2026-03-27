"""
Tests for the GET / root endpoint.
Follows AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_root_redirect_to_static_index(client):
    """
    Test GET / redirects to /static/index.html.
    
    AAA Pattern:
    - Arrange: No setup needed
    - Act: Send GET request to / endpoint
    - Assert: Verify 307 redirect status and Location header
    """
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_with_follow_redirects(client):
    """
    Test GET / can be followed to static index page.
    
    AAA Pattern:
    - Arrange: No setup needed
    - Act: Send GET request to / with follow_redirects=True
    - Assert: Verify final response is accessible
    """
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
    # The response should be HTML content from index.html


def test_root_redirect_location_header_exact(client):
    """
    Test GET / redirect location header is exactly /static/index.html.
    
    AAA Pattern:
    - Arrange: Define expected redirect location
    - Act: Send GET request to / endpoint
    - Assert: Verify exact location match
    """
    # Arrange
    expected_location = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert "location" in response.headers
    assert response.headers["location"] == expected_location
