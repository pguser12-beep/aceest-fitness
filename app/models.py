# app/models.py - Data Models
from datetime import datetime

class Workout:
    """Workout model to represent a gym workout session"""
    
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.date_created = datetime.now()
    
    def to_dict(self):
        """Convert workout object to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'duration': self.duration,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f"<Workout(name='{self.name}', duration={self.duration})>"

# In-memory storage for workouts (for simplicity)
# In a real application, this would be replaced with a database
workouts_storage = []
