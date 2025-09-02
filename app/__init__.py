# app/__init__.py - Application Factory
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aceest-fitness-secret-key-2025'
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app
