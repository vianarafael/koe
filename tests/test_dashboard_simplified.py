import pytest
from app.routes.dashboard import dashboard_page
from app.models import User, TweetEngagement
from datetime import datetime
import inspect

def test_dashboard_route_no_goals_import():
    """Test that dashboard route doesn't import goal-related functions"""
    # Verify that the dashboard route doesn't import goal functions
    import app.routes.dashboard as dashboard_module
    
    # Check that goal-related functions are not imported
    assert not hasattr(dashboard_module, 'get_user_goals')
    
    # Check that the route function doesn't call goal functions
    source = inspect.getsource(dashboard_page)
    assert 'get_user_goals' not in source

def test_dashboard_template_variables():
    """Test that dashboard template doesn't receive goal-related variables"""
    # Verify that the route function signature doesn't include goal parameters
    sig = inspect.signature(dashboard_page)
    assert 'user_goals' not in sig.parameters
    
    # Check that the function doesn't pass user_goals to template
    source = inspect.getsource(dashboard_page)
    assert 'user_goals=user_goals' not in source

def test_dashboard_route_imports():
    """Test that dashboard route has correct imports"""
    import app.routes.dashboard as dashboard_module
    
    # Verify that goal-related imports are not present
    source = inspect.getsource(dashboard_module)
    assert 'get_user_goals' not in source
    
    # Verify that core imports are present
    assert 'get_user_engagements' in source
    assert 'get_user_total_score' in source
    assert 'get_top_engagements' in source

def test_dashboard_functionality_remains():
    """Test that dashboard core functionality is intact"""
    # Verify that the dashboard route function exists and is callable
    assert callable(dashboard_page)
    
    # Verify that the function has the expected parameters
    sig = inspect.signature(dashboard_page)
    expected_params = {'request', 'current_user', 'db'}
    actual_params = set(sig.parameters.keys())
    assert expected_params.issubset(actual_params)

def test_goals_route_removed():
    """Test that goals route is completely removed from the app"""
    from app.main import app
    
    # Check that goals route is not in the app routes
    route_paths = [route.path for route in app.routes]
    assert '/goals' not in route_paths
    assert '/goals/' not in route_paths

def test_goals_template_removed():
    """Test that goals template file is removed"""
    import os
    
    # Check that goals.html template is not present
    goals_template_path = 'app/templates/goals.html'
    assert not os.path.exists(goals_template_path)

def test_goals_models_removed():
    """Test that goal-related models are removed"""
    from app.models import User, TweetEngagement, CSVUpload
    
    # Verify that goal models are not imported
    import app.models as models_module
    
    # Check that goal-related classes are not defined
    assert not hasattr(models_module, 'UserGoal')
    assert not hasattr(models_module, 'GoalProgress')
    assert not hasattr(models_module, 'GoalTemplate')
    assert not hasattr(models_module, 'CreateGoalRequest')
    assert not hasattr(models_module, 'GoalResponse')

def test_goals_db_functions_removed():
    """Test that goal-related database functions are removed"""
    from app.db import get_user_engagements, get_user_total_score
    
    # Verify that goal functions are not imported
    import app.db as db_module
    
    # Check that goal-related functions are not defined
    assert not hasattr(db_module, 'create_user_goal')
    assert not hasattr(db_module, 'get_user_goals')
    assert not hasattr(db_module, 'get_user_goal')
    assert not hasattr(db_module, 'update_goal_progress')
    assert not hasattr(db_module, 'delete_user_goal')

if __name__ == "__main__":
    pytest.main([__file__])
