"""
Security utilities for admin authentication and access control.
"""
from flask import session, redirect, url_for, flash, request, make_response
from functools import wraps
from datetime import datetime


def check_lockout():
    """
    Check if user is currently locked out from failed login attempts.
    
    Returns:
        tuple: (is_locked: bool, remaining_minutes: int)
    """
    lockout_until = session.get('lockout_until')
    if lockout_until:
        lockout_time = datetime.fromisoformat(lockout_until)
        if datetime.utcnow() < lockout_time:
            remaining = (lockout_time - datetime.utcnow()).total_seconds() / 60
            return True, int(remaining)
        else:
            # Lockout expired, clear it
            session.pop('lockout_until', None)
            session.pop('failed_attempts', None)
    return False, 0


def log_admin_access(action, username=None, ip_address=None):
    """
    Log admin actions for security auditing.
    
    Args:
        action (str): Description of the action performed
        username (str): Admin username (optional)
        ip_address (str): IP address of the request (optional)
    """
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    log_entry = f"[{timestamp}] {action}"
    if username:
        log_entry += f" | User: {username}"
    if ip_address:
        log_entry += f" | IP: {ip_address}"
    
    # Log to console (in production, use proper logging)
    print(log_entry)
    
    # Could also log to file or database here
    # with open('admin_access.log', 'a') as f:
    #     f.write(log_entry + '\n')


def admin_required(f):
    """
    Decorator to require admin authentication for protected routes.
    Adds no-cache headers to prevent caching of admin pages.
    
    Usage:
        @app.route('/admin/dashboard')
        @admin_required
        def admin_dashboard():
            return render_template('dashboard.html')
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('admin.admin_login'))
        
        # Log access
        log_admin_access('Admin page accessed', 
                        session.get('admin_username'), 
                        request.remote_addr)
        
        # Add no-cache headers for admin pages
        response = make_response(f(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return decorated_function
