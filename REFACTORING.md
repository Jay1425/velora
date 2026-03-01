# Velora Application Structure Refactoring

## Overview
The Velora Flask application has been refactored from a single-file monolith into a clean, modular application factory structure following Flask best practices.

## New Architecture

### Directory Structure
```
velora/
├── app/                          # Main application package
│   ├── __init__.py               # Application factory (create_app)
│   ├── models.py                 # Database models (Inquiry, FLAVOURS)
│   ├── routes/                   # Route blueprints
│   │   ├── __init__.py
│   │   ├── main.py               # Public routes (/, /legacy, /flavors, /bulk, /contact)
│   │   └── admin.py              # Admin routes (/admin/*, authentication)
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       └── security.py           # Auth decorators, rate limiting, logging
├── config.py                     # Configuration classes
├── run.py                        # Application entry point
├── templates/                    # Jinja2 templates (unchanged)
├── static/                       # Static assets (unchanged)
├── requirements.txt              # Python dependencies
├── Procfile                      # Render deployment config (updated)
├── runtime.txt                   # Python version specification
└── .env                          # Environment variables (local)
```

## Key Components

### 1. Application Factory (`app/__init__.py`)
- **Function**: `create_app(config_name=None)`
- **Purpose**: Creates and configures Flask app instances
- **Features**:
  - Auto-detects config (production if DATABASE_URL exists, else development)
  - Initializes extensions (SQLAlchemy, CSRF)
  - Registers blueprints (main, admin)
  - Sets up security headers middleware
  - Enforces HTTPS in production
  - Creates database tables

### 2. Configuration (`config.py`)
- **Classes**:
  - `Config`: Base configuration with common settings
  - `DevelopmentConfig`: SQLite database, debug mode enabled
  - `ProductionConfig`: PostgreSQL via DATABASE_URL, HTTPS enforced

- **Features**:
  - Environment-based configuration
  - Neon PostgreSQL URL conversion (postgres:// → postgresql://)
  - Connection pooling for PostgreSQL
  - Secure session settings
  - Rate limiting configuration

### 3. Models (`app/models.py`)
- **Database Model**: `Inquiry`
  - Customer inquiry/order information
  - Fields: name, phone, flavor, quantity, event_date, message, created_at
- **Constants**: `FLAVOURS`
  - Premium 4-flavor collection data

### 4. Routes

#### Main Blueprint (`app/routes/main.py`)
- **Prefix**: `/` (root)
- **Routes**:
  - `GET /` - Homepage
  - `GET /legacy` - Company history
  - `GET /flavors` - Flavor catalog
  - `GET /bulk` - Bulk orders info
  - `GET|POST /contact` - Contact form (saves to DB, redirects to WhatsApp)

#### Admin Blueprint (`app/routes/admin.py`)
- **Prefix**: `/admin`
- **Routes**:
  - `GET|POST /admin/login` - Admin authentication
  - `GET /admin/logout` - Session termination
  - `GET /admin/` - Dashboard with analytics (protected)
- **Features**:
  - Rate limiting (5 attempts, 15-minute lockout)
  - Password hash verification
  - Session security
  - Access logging

### 5. Security Utilities (`app/utils/security.py`)
- **Functions**:
  - `check_lockout()`: Validates login attempt limits
  - `log_admin_access()`: Security audit logging
- **Decorators**:
  - `@admin_required`: Protects admin routes, adds no-cache headers

### 6. Entry Point (`run.py`)
- Imports `create_app()` factory
- Creates app instance: `app = create_app()`
- Development server configuration
- Gunicorn-compatible for production

## Migration from Old Structure

### What Changed
| Before | After |
|--------|-------|
| Single `app.py` (402 lines) | Modular package structure |
| Global `app` instance | Application factory pattern |
| All routes in one file | Blueprints (main, admin) |
| Inline configuration | `config.py` classes |
| No separation of concerns | Organized by responsibility |

### What Stayed the Same
- All routes and functionality preserved
- Templates and static files unchanged
- Database schema identical
- Security features maintained (CSRF, rate limiting, session security)
- WhatsApp integration intact
- Admin analytics unchanged

## Benefits of New Structure

### 1. **Modularity**
- Separate concerns (routes, models, config, security)
- Easier to navigate and understand
- Clear responsibility boundaries

### 2. **Scalability**
- Easy to add new blueprints
- Can split large blueprints into smaller ones
- Testing is simpler (can test blueprints independently)

### 3. **Configuration Management**
- Environment-specific configs (dev vs prod)
- Easier to add new environments (staging, testing)
- No hardcoded configuration

### 4. **Maintainability**
- Easier to find and fix bugs
- Clear file organization
- Follows Flask best practices
- Better for team collaboration

### 5. **Deployment Flexibility**
- Application factory allows multiple instances
- Compatible with Gunicorn, uWSGI, etc.
- Easy to integrate with testing frameworks
- Supports Flask extensions better

## Running the Application

### Development
```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac

# Run development server
python run.py

# Or with Flask CLI
export FLASK_APP=run.py
flask run
```

### Production (Render)
```bash
# Procfile automatically uses:
gunicorn run:app
```

## Environment Variables
Required in `.env` (development) or Render (production):
- `SECRET_KEY`: Flask session encryption key
- `DATABASE_URL`: PostgreSQL connection string (optional in dev)
- `ADMIN_USERNAME`: Admin login username
- `ADMIN_PASSWORD_HASH`: Bcrypt password hash
- `FLASK_DEBUG`: Set to 'true' for development

## Testing the Refactored App
```bash
# Quick structure test
python test_structure.py

# Expected output:
# ✓ Models imported successfully
# ✓ Database tables exist
# ✓ Public routes (5): /, /legacy, /flavors, /bulk, /contact
# ✓ Admin routes (3): /admin/login, /admin/logout, /admin/
# ✓ Application structure is working correctly!
```

## Deployment Compatibility
✅ **Gunicorn**: `gunicorn run:app`  
✅ **Render**: Procfile updated (`web: gunicorn run:app`)  
✅ **Neon PostgreSQL**: Connection pooling configured  
✅ **SQLite Fallback**: Works in development  
✅ **Environment-based Config**: Auto-detects dev vs prod  

## Security Features Maintained
- Password hashing (Werkzeug)
- CSRF protection (Flask-WTF)
- Rate limiting (5 attempts, 15-min lockout)
- Session security (30-min timeout, HttpOnly, Secure, SameSite)
- Security headers (X-Frame-Options, CSP, etc.)
- HTTPS enforcement in production
- Admin action logging
- No-cache headers for admin pages

## Next Steps
1. ✅ Refactoring complete
2. ⏳ Commit changes to Git
3. ⏳ Push to GitHub
4. ⏳ Deploy to Render
5. ⏳ Verify production deployment

## Backup
The original single-file application is backed up as `app_old.py` for reference.

---

**Refactoring Date**: March 1, 2026  
**Status**: ✅ Complete and Tested  
**Compatibility**: Maintained 100% functionality
