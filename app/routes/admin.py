"""
Admin routes for Velora dashboard.
Handles authentication, inquiry management, and analytics.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import check_password_hash
from datetime import datetime
from app.models import db, Inquiry
from app.utils.security import admin_required, check_lockout, log_admin_access

# Create Blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """
    Admin login with rate limiting and account lockout protection.
    """
    # Get admin credentials from config
    ADMIN_USERNAME = current_app.config.get('ADMIN_USERNAME')
    ADMIN_PASSWORD_HASH = current_app.config.get('ADMIN_PASSWORD_HASH')
    MAX_LOGIN_ATTEMPTS = current_app.config.get('MAX_LOGIN_ATTEMPTS')
    LOCKOUT_DURATION = current_app.config.get('LOCKOUT_DURATION')
    
    # Check if credentials are configured
    if not ADMIN_USERNAME or not ADMIN_PASSWORD_HASH:
        log_admin_access('Login attempt - Credentials not configured', ip_address=request.remote_addr)
        return render_template('admin_login.html', 
                             error="Admin credentials not configured. Please contact system administrator.")
    
    # Check if user is locked out
    is_locked, remaining_minutes = check_lockout()
    if is_locked:
        log_admin_access('Login attempt - Account locked', ip_address=request.remote_addr)
        return render_template('admin_login.html', 
                             lockout=True, 
                             remaining_minutes=remaining_minutes)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Initialize failed attempts counter
        if 'failed_attempts' not in session:
            session['failed_attempts'] = 0
        
        # Verify credentials using secure password hash
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            # Successful login
            session.clear()  # Clear any previous session data
            session.permanent = True  # Enable session timeout from config
            session['admin_logged_in'] = True
            session['admin_username'] = username
            session['admin_login_time'] = datetime.utcnow().isoformat()
            session['admin_ip'] = request.remote_addr
            
            log_admin_access('Successful login', username, request.remote_addr)
            flash('Welcome to Velora Admin Dashboard', 'success')
            return redirect(url_for('admin.admin'))
        else:
            # Failed login
            session['failed_attempts'] = session.get('failed_attempts', 0) + 1
            attempts = session['failed_attempts']
            remaining = MAX_LOGIN_ATTEMPTS - attempts
            
            log_admin_access(f'Failed login attempt ({attempts}/{MAX_LOGIN_ATTEMPTS})', 
                           username, request.remote_addr)
            
            if attempts >= MAX_LOGIN_ATTEMPTS:
                # Lock account
                lockout_until = datetime.utcnow() + LOCKOUT_DURATION
                session['lockout_until'] = lockout_until.isoformat()
                log_admin_access(f'Account locked until {lockout_until}', username, request.remote_addr)
                return render_template('admin_login.html', 
                                     lockout=True, 
                                     remaining_minutes=15)
            else:
                flash(f'Invalid credentials. {remaining} attempt{"s" if remaining != 1 else ""} remaining.', 'error')
                return render_template('admin_login.html', remaining_attempts=remaining)
    
    return render_template('admin_login.html')


@admin_bp.route('/logout')
def admin_logout():
    """Admin logout - clears session and redirects to login."""
    username = session.get('admin_username')
    ip_address = request.remote_addr
    
    # Log logout
    log_admin_access('User logged out', username, ip_address)
    
    # Clear session
    session.clear()
    
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('admin.admin_login'))


@admin_bp.route('/')
@admin_required
def admin():
    """
    Admin dashboard with inquiry management and analytics.
    Supports filtering by date range (all, today, month).
    """
    # Get filter parameter
    filter_by = request.args.get('filter', 'all')
    
    # Query based on filter
    query = Inquiry.query
    
    if filter_by == 'today':
        today = datetime.utcnow().date()
        query = query.filter(db.func.date(Inquiry.created_at) == today)
    elif filter_by == 'month':
        this_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(Inquiry.created_at >= this_month_start)
    
    inquiries = query.order_by(Inquiry.created_at.desc()).all()
    
    # Calculate analytics
    all_inquiries = Inquiry.query.all()
    total_count = len(all_inquiries)
    
    # Most requested flavor
    flavor_counts = {}
    total_quantity = 0
    for inq in all_inquiries:
        flavor_counts[inq.flavor] = flavor_counts.get(inq.flavor, 0) + 1
        # Try to extract quantity number for average
        try:
            qty = int(''.join(filter(str.isdigit, inq.quantity)))
            total_quantity += qty
        except:
            pass
    
    most_requested_flavor = max(flavor_counts.items(), key=lambda x: x[1])[0] if flavor_counts else "N/A"
    avg_quantity = round(total_quantity / total_count, 1) if total_count > 0 else 0
    
    # Inquiries this month
    this_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    inquiries_this_month = Inquiry.query.filter(Inquiry.created_at >= this_month_start).count()
    
    analytics = {
        'total_count': total_count,
        'most_requested_flavor': most_requested_flavor,
        'avg_quantity': avg_quantity,
        'inquiries_this_month': inquiries_this_month
    }
    
    return render_template('admin.html', inquiries=inquiries, analytics=analytics, current_filter=filter_by)


@admin_bp.route('/update-status/<int:order_id>', methods=['POST'])
@admin_required
def update_status(order_id):
    """Update order status."""
    order = Inquiry.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['submitted', 'accepted', 'rejected', 'fulfilled', 'dispatched', 'delivered']:
        order.status = new_status
        db.session.commit()
        flash(f'Order {order.order_number} status updated to {new_status}', 'success')
    else:
        flash('Invalid status', 'error')
    
    return redirect(url_for('admin.admin'))
