import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from app.routes.settings import router
from app.models import User, SetPointValuesRequest
from datetime import datetime

# Test client
client = TestClient(app)

@pytest.fixture
def mock_user():
    """Mock user for testing"""
    return User(
        id="user123",
        email="test@example.com",
        username="testuser",
        hashed_password="hashed",
        point_values={"like": 1, "retweet": 2, "reply": 3, "mention": 1},
        created_at=datetime.utcnow(),
        is_active=True
    )

@pytest.fixture
def sample_point_values():
    """Sample point values for testing"""
    return {
        "like": 2,
        "retweet": 4,
        "reply": 6,
        "mention": 2
    }

class TestSettingsRoutes:
    """Test settings route functionality"""
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    def test_settings_page_authenticated(self, mock_db, mock_auth, mock_user):
        """Test settings page access with authenticated user"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        
        response = client.get("/settings/")
        assert response.status_code == 200
        assert "Engagement Strategy Settings" in response.text
        assert "Current Engagement Strategy" in response.text
        assert "Optimize Your Engagement Strategy" in response.text
    
    def test_settings_page_unauthenticated(self):
        """Test settings page access without authentication"""
        response = client.get("/settings/")
        
        # Should redirect to login
        assert response.status_code == 302
        assert "/auth/login" in response.headers["location"]

class TestPointValueUpdates:
    """Test point value update functionality"""
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    @patch('app.routes.settings.scoring_engine')
    @patch('app.routes.settings.update_user_point_values')
    @patch('app.routes.settings.recalculate_user_scores')
    @patch('app.routes.settings.get_user_by_id')
    def test_update_point_values_success(self, mock_get_user, mock_recalc, mock_update, mock_scoring, mock_db, mock_auth, mock_user, sample_point_values):
        """Test successful point value update"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        mock_scoring.validate_point_values.return_value = True
        mock_update.return_value = None
        mock_recalc.return_value = 25  # 25 scores recalculated
        mock_get_user.return_value = mock_user
        
        response = client.post("/settings/update-points", data=sample_point_values)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert "Point values updated successfully" in data["message"]
        assert data["recalculated_count"] == 25
        assert data["updated_point_values"] == sample_point_values
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    @patch('app.routes.settings.scoring_engine')
    def test_update_point_values_invalid(self, mock_scoring, mock_db, mock_auth, mock_user):
        """Test point value update with invalid values"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        mock_scoring.validate_point_values.return_value = False
        
        invalid_values = {"like": -1, "retweet": 2, "reply": 3, "mention": 1}
        response = client.post("/settings/update-points", data=invalid_values)
        assert response.status_code == 400
        assert "Invalid point values" in response.json()["detail"]
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    @patch('app.routes.settings.scoring_engine')
    @patch('app.routes.settings.update_user_point_values')
    @patch('app.routes.settings.recalculate_user_scores')
    def test_update_point_values_htmx_success(self, mock_recalc, mock_update, mock_scoring, mock_db, mock_auth, mock_user, sample_point_values):
        """Test successful HTMX point value update"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        mock_scoring.validate_point_values.return_value = True
        mock_update.return_value = None
        mock_recalc.return_value = 30  # 30 scores recalculated
        
        response = client.post("/settings/update-points-htmx", data=sample_point_values)
        assert response.status_code == 200
        
        # Check HTML response contains success message
        html_content = response.text
        assert "Point values updated successfully" in html_content
        assert "30 engagement scores recalculated" in html_content
        assert "2" in html_content  # New like value
        assert "4" in html_content  # New retweet value
        assert "6" in html_content  # New reply value
        assert "2" in html_content  # New mention value
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    @patch('app.routes.settings.scoring_engine')
    def test_update_point_values_htmx_invalid(self, mock_scoring, mock_db, mock_auth, mock_user):
        """Test HTMX point value update with invalid values"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        mock_scoring.validate_point_values.return_value = False
        
        invalid_values = {"like": -1, "retweet": 2, "reply": 3, "mention": 1}
        response = client.post("/settings/update-points-htmx", data=invalid_values)
        assert response.status_code == 400
        assert "Invalid point values" in response.text

class TestSettingsAPIs:
    """Test settings API endpoints"""
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    @patch('app.routes.settings.get_user_by_id')
    def test_get_current_point_values(self, mock_get_user, mock_db, mock_auth, mock_user):
        """Test getting current user point values"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        mock_get_user.return_value = mock_user
        
        response = client.get("/settings/api/current-points")
        assert response.status_code == 200
        
        data = response.json()
        assert data["point_values"] == mock_user.point_values
        assert data["user_id"] == mock_user.id
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    def test_get_point_impact_analysis(self, mock_db, mock_auth, mock_user):
        """Test point impact analysis API"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        
        response = client.get("/settings/api/point-impact")
        assert response.status_code == 200
        
        data = response.json()
        assert "current_values" in data
        assert "scoring_formula" in data
        assert "example_scenarios" in data
        assert "recommendations" in data
        
        # Check scoring formula
        assert f"likes × {mock_user.point_values['like']}" in data["scoring_formula"]
        assert f"retweets × {mock_user.point_values['retweet']}" in data["scoring_formula"]
        assert f"replies × {mock_user.point_values['reply']}" in data["scoring_formula"]
        assert f"mentions × {mock_user.point_values['mention']}" in data["scoring_formula"]
        
        # Check example scenarios
        scenarios = data["example_scenarios"]
        assert "high_engagement" in scenarios
        assert "medium_engagement" in scenarios
        assert "low_engagement" in scenarios
        
        # Check recommendations
        recommendations = data["recommendations"]
        assert "high_value_actions" in recommendations
        assert "optimization_tips" in recommendations

class TestSettingsValidation:
    """Test settings validation functionality"""
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    @patch('app.routes.settings.scoring_engine')
    def test_point_values_validation_success(self, mock_scoring, mock_db, mock_auth, mock_user, sample_point_values):
        """Test successful point values validation"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        mock_scoring.validate_point_values.return_value = True
        
        response = client.post("/settings/update-points", data=sample_point_values)
        assert response.status_code == 200
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    @patch('app.routes.settings.scoring_engine')
    def test_point_values_validation_failure(self, mock_scoring, mock_db, mock_auth, mock_user):
        """Test point values validation failure"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        mock_scoring.validate_point_values.return_value = False
        
        # Test with negative values
        invalid_values = {"like": -1, "retweet": 2, "reply": 3, "mention": 1}
        response = client.post("/settings/update-points", data=invalid_values)
        assert response.status_code == 400
        
        # Test with missing values
        incomplete_values = {"like": 1, "retweet": 2, "reply": 3}  # Missing mention
        response = client.post("/settings/update-points", data=incomplete_values)
        assert response.status_code == 422  # Validation error

class TestSettingsIntegration:
    """Test settings integration with other components"""
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    @patch('app.routes.settings.scoring_engine')
    @patch('app.routes.settings.update_user_point_values')
    @patch('app.routes.settings.recalculate_user_scores')
    def test_score_recalculation_integration(self, mock_recalc, mock_update, mock_scoring, mock_db, mock_auth, mock_user, sample_point_values):
        """Test that score recalculation is triggered when point values change"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        mock_scoring.validate_point_values.return_value = True
        mock_update.return_value = None
        mock_recalc.return_value = 15  # 15 scores recalculated
        
        response = client.post("/settings/update-points", data=sample_point_values)
        assert response.status_code == 200
        
        # Verify that recalculation was called
        mock_recalc.assert_called_once_with(
            mock_user.id,
            sample_point_values,
            mock_db.return_value
        )
        
        # Verify that user point values were updated
        mock_update.assert_called_once_with(
            mock_db.return_value,
            mock_user.id,
            sample_point_values
        )
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    @patch('app.routes.settings.scoring_engine')
    @patch('app.routes.settings.update_user_point_values')
    @patch('app.routes.settings.recalculate_user_scores')
    def test_immediate_score_impact(self, mock_recalc, mock_update, mock_scoring, mock_db, mock_auth, mock_user, sample_point_values):
        """Test that updated point values immediately affect score calculations"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        mock_scoring.validate_point_values.return_value = True
        mock_update.return_value = None
        mock_recalc.return_value = 20
        
        # Update point values
        response = client.post("/settings/update-points", data=sample_point_values)
        assert response.status_code == 200
        
        # Verify that the scoring engine validation was called with new values
        mock_scoring.validate_point_values.assert_called_once_with(sample_point_values)
        
        # Verify that recalculation was triggered
        assert mock_recalc.called

class TestSettingsErrorHandling:
    """Test settings error handling"""
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    @patch('app.routes.settings.scoring_engine')
    def test_database_error_handling(self, mock_scoring, mock_db, mock_auth, mock_user, sample_point_values):
        """Test handling of database errors during point value update"""
        mock_auth.return_value = mock_user
        mock_db.return_value = AsyncMock()
        mock_scoring.validate_point_values.return_value = True
        
        # Simulate database error
        from app.routes.settings import update_user_point_values
        with patch('app.routes.settings.update_user_point_values', side_effect=Exception("Database error")):
            response = client.post("/settings/update-points", data=sample_point_values)
            assert response.status_code == 500
            assert "Error updating point values" in response.json()["detail"]
    
    @patch('app.routes.settings.get_current_user')
    @patch('app.routes.settings.get_db')
    def test_authentication_error_handling(self, mock_db, mock_auth):
        """Test handling of authentication errors"""
        mock_auth.return_value = None  # No authenticated user
        mock_db.return_value = AsyncMock()
        
        response = client.post("/settings/update-points", data={"like": 1, "retweet": 2, "reply": 3, "mention": 1})
        assert response.status_code == 401
        assert "Authentication required" in response.json()["detail"]

if __name__ == "__main__":
    pytest.main([__file__])
