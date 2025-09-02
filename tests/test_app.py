# tests/test_app.py - Unit Tests for Flask Application
import pytest
import json
from app import create_app
from app.models import workouts_storage

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def clean_storage():
    """Clean workouts storage before and after tests"""
    workouts_storage.clear()
    yield
    workouts_storage.clear()

class TestBasicRoutes:
    """Test basic route functionality"""
    
    def test_index_route(self, client):
        """Test home page loads correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'ACEest Fitness' in response.data

    def test_add_workout_get(self, client):
        """Test add workout page loads"""
        response = client.get('/add-workout')
        assert response.status_code == 200
        assert b'Add Workout' in response.data

    def test_view_workouts_get(self, client):
        """Test view workouts page loads"""
        response = client.get('/view-workouts')
        assert response.status_code == 200

class TestWorkoutFunctionality:
    """Test workout add/view functionality"""
    
    def test_add_workout_post_valid(self, client, clean_storage):
        """Test adding valid workout"""
        response = client.post('/add-workout', data={
            'workout_name': 'Push-ups',
            'duration': '30'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert len(workouts_storage) == 1
        assert workouts_storage[0].name == 'Push-ups'
        assert workouts_storage[0].duration == 30

    def test_add_workout_post_empty_name(self, client, clean_storage):
        """Test adding workout with empty name"""
        response = client.post('/add-workout', data={
            'workout_name': '',
            'dura
