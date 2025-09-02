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
            'duration': '30'
        })
        assert response.status_code == 200
        assert len(workouts_storage) == 0
        assert b'Please enter both workout name and duration' in response.data

    def test_add_workout_post_empty_duration(self, client, clean_storage):
        """Test adding workout with empty duration"""
        response = client.post('/add-workout', data={
            'workout_name': 'Squats',
            'duration': ''
        })
        assert response.status_code == 200
        assert len(workouts_storage) == 0

    def test_add_workout_post_invalid_duration(self, client, clean_storage):
        """Test adding workout with invalid duration"""
        response = client.post('/add-workout', data={
            'workout_name': 'Burpees',
            'duration': 'invalid'
        })
        assert response.status_code == 200
        assert len(workouts_storage) == 0
        assert b'Duration must be a positive number' in response.data

    def test_add_workout_post_negative_duration(self, client, clean_storage):
        """Test adding workout with negative duration"""
        response = client.post('/add-workout', data={
            'workout_name': 'Planks',
            'duration': '-10'
        })
        assert response.status_code == 200
        assert len(workouts_storage) == 0

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_api_get_workouts_empty(self, client, clean_storage):
        """Test API returns empty list when no workouts"""
        response = client.get('/api/workouts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    def test_api_get_workouts_with_data(self, client, clean_storage):
        """Test API returns workouts when data exists"""
        # Add a workout first
        client.post('/add-workout', data={
            'workout_name': 'Squats',
            'duration': '45'
        })
        
        response = client.get('/api/workouts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['name'] == 'Squats'
        assert data[0]['duration'] == 45
        assert 'date_created' in data[0]

    def test_api_add_workout_valid(self, client, clean_storage):
        """Test API add workout with valid data"""
        response = client.post('/api/workouts', 
                              json={'name': 'Burpees', 'duration': 25},
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'message' in data
        assert data['workout']['name'] == 'Burpees'
        assert len(workouts_storage) == 1

    def test_api_add_workout_missing_fields(self, client, clean_storage):
        """Test API add workout with missing fields"""
        response = client.post('/api/workouts', 
                              json={'name': 'Incomplete'},
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_api_add_workout_invalid_duration(self, client, clean_storage):
        """Test API add workout with invalid duration"""
        response = client.post('/api/workouts', 
                              json={'name': 'Test', 'duration': 'invalid'},
                              content_type='application/json')
        assert response.status_code == 400

    def test_api_workout_count(self, client, clean_storage):
        """Test API workout count endpoint"""
        response = client.get('/api/workouts/count')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 0
        
        # Add workout and test again
        client.post('/api/workouts', 
                   json={'name': 'Test', 'duration': 30},
                   content_type='application/json')
        
        response = client.get('/api/workouts/count')
        data = json.loads(response.data)
        assert data['count'] == 1

    def test_api_total_duration(self, client, clean_storage):
        """Test API total duration endpoint"""
        response = client.get('/api/workouts/total-duration')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_duration'] == 0
        
        # Add workouts and test again
        client.post('/api/workouts', 
                   json={'name': 'Test1', 'duration': 30},
                   content_type='application/json')
        client.post('/api/workouts', 
                   json={'name': 'Test2', 'duration': 20},
                   content_type='application/json')
        
        response = client.get('/api/workouts/total-duration')
        data = json.loads(response.data)
        assert data['total_duration'] == 50