"""
Integration tests for the GET /activities endpoint.

Tests follow the Arrange-Act-Assert (AAA) pattern:
- Arrange: Set up test data and fixtures
- Act: Make the API request
- Assert: Verify the response
"""

import pytest


class TestGetActivities:
    """Test cases for GET /activities endpoint"""
    
    def test_get_activities_success(self, client, reset_activities):
        """
        Test: Successful retrieval of all activities
        
        Arrange: Use the TestClient fixture with reset activities
        Act: Make GET request to /activities
        Assert: Verify 200 status and response contains all activities
        """
        # Arrange
        # (fixtures provide client and reset activities to initial state)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 3
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
    
    def test_get_activities_response_structure(self, client, reset_activities):
        """
        Test: Response has correct structure for each activity
        
        Arrange: Use the TestClient fixture with reset activities
        Act: Make GET request to /activities
        Assert: Verify each activity has required fields
        """
        # Arrange
        # (fixtures provide client and reset activities to initial state)
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data, dict)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
    
    def test_get_activities_contains_participants(self, client, reset_activities):
        """
        Test: Activities contain correct participant data
        
        Arrange: Use the TestClient fixture with reset activities
        Act: Make GET request to /activities
        Assert: Verify known participants are in their activities
        """
        # Arrange
        # (fixtures provide client and reset activities to initial state)
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
        assert "emma@mergington.edu" in data["Programming Class"]["participants"]
        assert "sophia@mergington.edu" in data["Programming Class"]["participants"]
        assert "john@mergington.edu" in data["Gym Class"]["participants"]
        assert "olivia@mergington.edu" in data["Gym Class"]["participants"]
    
    def test_get_activities_correct_descriptions(self, client, reset_activities):
        """
        Test: Activities have correct descriptions
        
        Arrange: Use the TestClient fixture with reset activities
        Act: Make GET request to /activities
        Assert: Verify descriptions match expected values
        """
        # Arrange
        # (fixtures provide client and reset activities to initial state)
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
        assert data["Programming Class"]["description"] == "Learn programming fundamentals and build software projects"
        assert data["Gym Class"]["description"] == "Physical education and sports activities"
