# app/routes.py - Flask Routes and API Endpoints
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app.models import Workout, workouts_storage

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@main.route('/add-workout', methods=['GET', 'POST'])
def add_workout():
    """Add workout route - handles both GET and POST requests"""
    if request.method == 'POST':
        workout_name = request.form.get('workout_name', '').strip()
        duration = request.form.get('duration', '').strip()
        
        # Validation
        if not workout_name or not duration:
            flash('Please enter both workout name and duration.', 'error')
            return render_template('add_workout.html')
        
        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError("Duration must be positive")
            
            # Create and store workout
            workout = Workout(workout_name, duration)
            workouts_storage.append(workout)
            flash(f"'{workout_name}' added successfully!", 'success')
            return redirect(url_for('main.view_workouts'))
        
        except ValueError:
            flash('Duration must be a positive number.', 'error')
            return render_template('add_workout.html')
    
    return render_template('add_workout.html')

@main.route('/view-workouts')
def view_workouts():
    """View all workouts route"""
    return render_template('view_workouts.html', workouts=workouts_storage)

# API Endpoints
@main.route('/api/workouts', methods=['GET'])
def api_get_workouts():
    """API endpoint to get all workouts"""
    return jsonify([workout.to_dict() for workout in workouts_storage])

@main.route('/api/workouts', methods=['POST'])
def api_add_workout():
    """API endpoint to add a new workout"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'duration' not in data:
        return jsonify({'error': 'Missing required fields: name and duration'}), 400
    
    try:
        duration = int(data['duration'])
        if duration <= 0:
            raise ValueError("Duration must be positive")
        
        workout = Workout(data['name'], duration)
        workouts_storage.append(workout)
        return jsonify({
            'message': 'Workout added successfully', 
            'workout': workout.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@main.route('/api/workouts/count')
def api_workout_count():
    """API endpoint to get total workout count"""
    return jsonify({'count': len(workouts_storage)})

@main.route('/api/workouts/total-duration')
def api_total_duration():
    """API endpoint to get total workout duration"""
    total_duration = sum(workout.duration for workout in workouts_storage)
    return jsonify({'total_duration': total_duration})