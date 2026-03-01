from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, timedelta
from urllib.parse import quote
from functools import wraps
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# ============================================
# Security Configuration (Production-Grade)
# ============================================

# Determine if running in debug mode
DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Secret key for session signing
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())

# Secure session configuration
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = not DEBUG_MODE  # True in production (HTTPS)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# ============================================
# Database Configuration (PostgreSQL/SQLite)
# ============================================

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    DATABASE_URL = "sqlite:///velora.db"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# PostgreSQL connection pool configuration (production optimization)
if DATABASE_URL.startswith("postgresql://"):
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,        # Verify connections before using
        "pool_recycle": 300,           # Recycle connections after 5 minutes
        "pool_size": 10,               # Max connections in pool
        "max_overflow": 20             # Max overflow connections
    }

# CSRF Protection
csrf = CSRFProtect(app)

# Get admin credentials from environment
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH')

# Rate limiting constants
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=15)

db = SQLAlchemy(app)

# ============================================
# Security Utility Functions
# ============================================

def check_lockout():
    """Check if user is currently locked out from login attempts"""
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
    """Log admin actions for security auditing"""
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

# ============================================
# Security Headers Middleware
# ============================================

@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.tailwindcss.com;"
    return response

@app.before_request
def enforce_https():
    """Redirect HTTP to HTTPS in production"""
    if not DEBUG_MODE and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
        return redirect(url, code=301)

# ============================================
# Admin Authentication Decorator
# ============================================

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('admin_login'))
        
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

# Database Model
class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    flavor = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(20), nullable=False)
    event_date = db.Column(db.String(20))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Inquiry {self.name}>'

# ONLY 4 Flavors - Premium Collection
FLAVOURS = [
    {
        'name': 'Classic Mango',
        'description': 'Premium Alphonso mangoes create our most beloved flavor',
        'image': 'classic-mango.png',
        'price': '₹260 / kg'
    },
    {
        'name': 'Mix Fruit Delight',
        'description': 'A harmonious blend of tropical fruits in creamy tradition',
        'image': 'mix-fruit-delight.png',
        'price': '₹260 / kg'
    },
    {
        'name': 'Rajbhog Reserve',
        'description': 'Royal saffron, nuts and rose essence - our signature luxury',
        'image': 'rajbhog-reserve.png',
        'price': '₹280 / kg'
    },
    {
        'name': 'Kesar Royale',
        'description': 'Pure Kashmir saffron in every spoonful - the ultimate indulgence',
        'image': 'kesar-royale.png',
        'price': '₹300 / kg'
    }
]

# Routes
@app.route('/')
def index():
    return render_template('index.html', flavours=FLAVOURS)

@app.route('/legacy')
def legacy():
    return render_template('legacy.html')

@app.route('/flavors')
def flavors():
    return render_template('flavors.html', flavours=FLAVOURS)

@app.route('/bulk')
def bulk():
    return render_template('bulk.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        flavor = request.form.get('flavor')
        quantity = request.form.get('quantity')
        event_date = request.form.get('event_date')
        message = request.form.get('message')
        
        inquiry = Inquiry(
            name=name,
            phone=phone,
            flavor=flavor,
            quantity=quantity,
            event_date=event_date,
            message=message
        )
        
        try:
            db.session.add(inquiry)
            db.session.commit()
            
            # Build WhatsApp message
            whatsapp_message = f"Hello Velora! I submitted an order request.\n\n"
            whatsapp_message += f"Name: {name}\n"
            whatsapp_message += f"Flavor: {flavor}\n"
            whatsapp_message += f"Quantity: {quantity}\n"
            if event_date:
                whatsapp_message += f"Event Date: {event_date}\n"
            if message:
                whatsapp_message += f"\nMessage: {message}"
            
            # Redirect to WhatsApp
            whatsapp_url = f"https://wa.me/919428638301?text={quote(whatsapp_message)}"
            return redirect(whatsapp_url)
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('contact'))
    
    return render_template('contact.html', flavours=FLAVOURS)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
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
            session.permanent = True  # Enable 30-minute session timeout
            session['admin_logged_in'] = True
            session['admin_username'] = username
            session['admin_login_time'] = datetime.utcnow().isoformat()
            session['admin_ip'] = request.remote_addr
            
            log_admin_access('Successful login', username, request.remote_addr)
            flash('Welcome to Velora Admin Dashboard', 'success')
            return redirect(url_for('admin'))
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

@app.route('/admin/logout')
def admin_logout():
    username = session.get('admin_username')
    ip_address = request.remote_addr
    
    # Log logout
    log_admin_access('User logged out', username, ip_address)
    
    # Clear session and regenerate
    session.clear()
    
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin():
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

# ============================================
# Database Initialization
# ============================================

# Create database tables
with app.app_context():
    db.create_all()

# ============================================
# Production Server Configuration
# ============================================

if __name__ == '__main__':
    # Production-ready configuration for Render deployment
    # - host="0.0.0.0" allows external connections
    # - port from environment variable (Render assigns dynamically)
    # - debug disabled in production
    
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    app.run(
        host=host,
        port=port,
        debug=DEBUG_MODE
    )
