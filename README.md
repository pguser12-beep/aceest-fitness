{% extends "base.html" %}

{% block title %}View Workouts - ACEest Fitness{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>
                <i class="fas fa-list me-2"></i>Your Workouts
            </h2>
            <a href="{{ url_for('main.add_workout') }}" class="btn btn-primary">
                <i class="fas fa-plus me-2"></i>Add Workout
            </a>
        </div>
        
        {% if workouts %}
            <!-- Summary Cards -->
            <div class="row mb-4">
                <div class="col-md-4">
                    <div class="card bg-primary text-white">
                        <div class="card-body text-center">
                            <i class="fas fa-dumbbell fa-2x mb-2"></i>
                            <h4>{{ workouts|length }}</h4>
                            <p class="mb-0">Total Workouts</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-success text-white">
                        <div class="card-body text-center">
                            <i class="fas fa-clock fa-2x mb-2"></i>
                            <h4>{{ workouts|sum(attribute='duration') }}</h4>
                            <p class="mb-0">Total Minutes</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-info text-white">
                        <div class="card-body text-center">
                            <i class="fas fa-chart-line fa-2x mb-2"></i>
                            <h4>{{ "%.1f"|format(workouts|sum(attribute='duration') / workouts|length) }}</h4>
                            <p class="mb-0">Avg Duration</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Workouts Table -->
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-table me-2"></i>Workout History
                    </h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover mb-0">
                            <thead class="table-dark">
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">
                                        <i class="fas fa-dumbbell me-1"></i>Workout
                                    </th>
                                    <th scope="col">
                                        <i class="fas fa-clock me-1"></i>Duration
                                    </th>
                                    <th scope="col">
                                        <i class="fas fa-calendar me-1"></i>Date Added
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for workout in workouts %}
                                <tr>
                                    <th scope="row">{{ loop.index }}</th>
                                    <td>
                                        <strong>{{ workout.name }}</strong>
                                    </td>
                                    <td>
                                        <span class="badge bg-primary">
                                            {{ workout.duration }} min
                                        </span>
                                    </td>
                                    <td>
                                        <small class="text-muted">
                                            {{ workout.date_created.strftime('%Y-%m-%d %H:%M') }}
                                        </small>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- Workout Categories (Sample Analysis) -->
            <div class="card mt-4">
                <div class="card-body">
                    <h6 class="card-title">
                        <i class="fas fa-chart-pie me-2"></i>Quick Analysis
                    </h6>
                    <div class="row">
                        <div class="col-md-6">
                            <p class="mb-1">
                                <strong>Most Common Duration:</strong> 
                                {% set duration_counts = {} %}
                                {% for workout in workouts %}
                                    {% if workout.duration in duration_counts %}
                                        {% set _ = duration_counts.update({workout.duration: duration_counts[workout.duration] + 1}) %}
                                    {% else %}
                                        {% set _ = duration_counts.update({workout.duration: 1}) %}
                                    {% endif %}
                                {% endfor %}
                                {% if duration_counts %}
                                    {{ duration_counts.keys()|list|sort|last }} minutes
                                {% endif %}
                            </p>
                            <p class="mb-0">
                                <strong>Longest Workout:</strong> 
                                {{ workouts|max(attribute='duration')|attr('duration') }} minutes
                                ({{ workouts|max(attribute='duration')|attr('name') }})
                            </p>
                        </div>
                        <div class="col-md-6">
                            <p class="mb-1">
                                <strong>Latest Workout:</strong> 
                                {{ workouts[-1].name }} - {{ workouts[-1].duration }} min
                            </p>
                            <p class="mb-0">
                                <strong>Total Hours:</strong> 
                                {{ "%.1f"|format(workouts|sum(attribute='duration') / 60) }} hours
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        {% else %}
            <!-- Empty State -->
            <div class="text-center py-5">
                <div class="card">
                    <div class="card-body py-5">
                        <i class="fas fa-dumbbell fa-4x text-muted mb-4"></i>
                        <h4 class="text-muted">No Workouts Yet</h4>
                        <p class="text-muted mb-4">
                            Start your fitness journey by adding your first workout!
                        </p>
                        <a href="{{ url_for('main.add_workout') }}" class="btn btn-primary btn-lg">
                            <i class="fas fa-plus me-2"></i>Add Your First Workout
                        </a>
                    </div>
                </div>
            </div>
        {% endif %}
    </div>
</div>

<!-- Back to Home Button -->
<div class="text-center mt-4">
    <a href="{{ url_for('main.index') }}" class="btn btn-secondary">
        <i class="fas fa-home me-2"></i>Back to Home
    </a>
</div>
{% endblock %}
# Trigger new run
