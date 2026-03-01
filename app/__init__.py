"""
Velora Flask Application Factory.
Creates and configures the Flask application with all extensions and blueprints.
"""
import os
from pathlib import Path
from flask import Flask, redirect, request
from flask_wtf.csrf import CSRFProtect


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app instances.
    
    Args:
        config_name (str): Configuration name ('development', 'production', or None for auto-detect)
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Get the parent directory (velora/) for templates and static folders
    parent_dir = Path(__file__).parent.parent
    
    # Create Flask app with correct template and static folders
    app = Flask(__name__,
                template_folder=str(parent_dir / 'templates'),
                static_folder=str(parent_dir / 'static'))
    
    # Load configuration
    if config_name is None:
        # Auto-detect: production if DATABASE_URL exists, else development
        config_name = 'production' if os.environ.get('DATABASE_URL') else 'development'
    
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    from app.models import db
    db.init_app(app)
    
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Security headers middleware
    @app.after_request
    def set_security_headers(response):
        """Add security headers to all responses."""
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self' 'unsafe-inline' https:; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://fonts.gstatic.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.tailwindcss.com;"
        )
        return response
    
    # HTTPS enforcement in production
    @app.before_request
    def enforce_https():
        """Redirect HTTP to HTTPS in production."""
        if not app.config.get('DEBUG') and request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
