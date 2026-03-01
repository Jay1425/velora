"""
Velora Application Entry Point.
Run this file to start the development server.
For production deployment, use Gunicorn: gunicorn run:app
"""
import os
from app import create_app

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # Development server configuration
    # For production, use Gunicorn instead
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )
