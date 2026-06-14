"""
Integration tests for the POST /activities/{activity_name}/signup endpoint.

Tests follow the Arrange-Act-Assert (AAA) pattern:
- Arrange: Set up test data and fixtures
- Act: Make the API request
- Assert: Verify the response
"""

import pytest


class TestSignupForActivity:
    """Test cases for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_user_success(self, client, reset_activities):
        """
        Test: Successful signup for a new user to an existing activity
        
        Arrange: Use the TestClient fixture with reset activities
        Act: POST signup request with valid activity name and new email
        Assert: Verify 200 status, confirmation message, and participant added
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
        
        # Verify participant was added to the activity
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]
    
    def test_signup_duplicate_email_allowed(self, client, reset_activities):
        """
        Test: Current implementation allows duplicate email signups (idempotent behavior)
        
        Arrange: Use the TestClient fixture with reset activities
        Act: POST signup with same email twice
        Assert: Verify both requests succeed and email appears multiple times
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act - Second signup with same email
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert - Both requests succeed
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify email appears in activity (may appear twice)
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        participants = activities_data[activity_name]["participants"]
        assert email in participants
    
    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        Test: Signup to non-existent activity returns 404
        
        Arrange: Use the TestClient fixture with reset activities
        Act: POST signup to activity that doesn't exist
        Assert: Verify 404 status and error detail
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "alice@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_signup_all_activities_success(self, client, reset_activities):
        """
        Test: User can successfully signup for all available activities
        
        Arrange: Use the TestClient fixture with reset activities
        Act: POST signup for each activity with same email
        Assert: Verify all signups succeed
        """
        # Arrange
        activities_list = ["Chess Club", "Programming Class", "Gym Class"]
        email = "alice@mergington.edu"
        
        # Act & Assert
        for activity_name in activities_list:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            
            # Assert each signup succeeds
            assert response.status_code == 200
            assert email in response.json()["message"]
    
    def test_signup_response_format(self, client, reset_activities):
        """
        Test: Signup response has correct structure
        
        Arrange: Use the TestClient fixture with reset activities
        Act: POST signup request
        Assert: Verify response JSON structure
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)
    
    def test_signup_with_existing_participant(self, client, reset_activities):
        """
        Test: Signup with email that already exists in the activity
        
        Arrange: Use the TestClient fixture with reset activities, 
                 knowing michael@mergington.edu is already in Chess Club
        Act: POST signup with existing participant email
        Assert: Verify request succeeds (no duplicate prevention)
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert - Current implementation allows this
        assert response.status_code == 200
        assert existing_email in response.json()["message"]
