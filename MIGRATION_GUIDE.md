# Flask-Migrate Migration Guide

This project now uses **Flask-Migrate** (Alembic) for managing database schema changes in production.

---

## 🎯 Why Flask-Migrate?

- **Safe schema changes** - No more dropping tables and losing data
- **Version control** - Track all database changes in migration files
- **Rollback capability** - Undo migrations if needed
- **Production-ready** - Industry standard for Flask apps

---

## 📋 Local Development Workflow

### 1. After Changing Models (app/models.py)

```bash
# Generate a new migration
flask db migrate -m "Add new column to Inquiry table"

# Review the generated migration file in migrations/versions/

# Apply the migration to your local database
flask db upgrade
```

### 2. Common Commands

```bash
# Show current migration status
flask db current

# Show migration history
flask db history

# Rollback last migration
flask db downgrade

# Upgrade to specific revision
flask db upgrade <revision_id>

# Show SQL that will be executed (dry run)
flask db upgrade --sql
```

---

## 🚀 Production Deployment (Render)

### First Time Setup (One-time)

**If your production database already has the tables**, you need to tell Flask-Migrate to start tracking:

```bash
# SSH or use Render Shell
flask db stamp head
```

This marks your existing database as "up-to-date" without running any migrations.

### Regular Deployment Workflow

1. **Develop locally** - Make model changes, create and test migrations
2. **Commit migrations** - Git add the `migrations/versions/` files
3. **Push to GitHub** - Your changes deploy to Render automatically
4. **Run migrations on Render** - Use one of these methods:

#### Option A: Render Shell (Recommended)
1. Go to Render Dashboard → Your service → Shell tab
2. Run:
   ```bash
   flask db upgrade
   ```

#### Option B: Build Command
Update your Render build command to:
```bash
pip install -r requirements.txt && flask db upgrade
```

#### Option C: Release Phase Command
In Render settings, add a "Release Command":
```bash
flask db upgrade
```
This runs automatically after each deployment.

---

## 📁 Migration Files

- **Location**: `migrations/versions/`
- **Format**: `<hash>_<description>.py`
- **Git**: Always commit migration files
- **Never**: Manually edit old migrations that have been deployed

---

## ⚠️ CRITICAL: Production Database Recovery

Your current production database has the schema already. Here's how to bring it under Flask-Migrate control:

### Step 1: Deploy Code with Flask-Migrate
✅ Already done - code is pushed to GitHub

### Step 2: Mark Existing Schema
In Render Shell, run:
```bash
flask db stamp head
```

This tells Flask-Migrate "the database is already at the latest version" without actually running any migrations.

### Step 3: Future Changes
From now on, any model changes will:
1. Generate a migration locally (`flask db migrate`)
2. Be committed to Git
3. Deploy to Render
4. Be applied with `flask db upgrade`

---

## 🔄 Migration from Old System

### Before (Manual Reset - DEPRECATED)
```python
# Old method in app/__init__.py
if os.environ.get('RESET_DB') == 'true':
    db.drop_all()  # ⚠️ LOSES ALL DATA
    db.create_all()
```

### After (Flask-Migrate - CURRENT)
```bash
# Safe schema changes
flask db migrate -m "Add new field"
flask db upgrade  # Preserves existing data
```

---

## 📝 Example: Adding a New Field

### 1. Update Model
```python
# app/models.py
class Inquiry(db.Model):
    # ... existing fields ...
    delivery_address = db.Column(db.String(200))  # NEW FIELD
```

### 2. Generate Migration
```bash
flask db migrate -m "Add delivery_address to Inquiry"
```

### 3. Review Generated File
Check `migrations/versions/xxxxx_add_delivery_address_to_inquiry.py`

### 4. Test Locally
```bash
flask db upgrade
# Test your app
```

### 5. Deploy
```bash
git add migrations/versions/
git commit -m "feat: Add delivery address field"
git push
```

### 6. Apply in Production
```bash
# In Render Shell
flask db upgrade
```

---

## 🛠️ Troubleshooting

### Migration Conflict
If you get "Multiple heads detected":
```bash
flask db merge heads -m "Merge migrations"
```

### Reset Migrations (Development Only)
```bash
flask db downgrade base  # Remove all migrations
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Check Migration Status
```bash
flask db current  # What version is the database at?
flask db history  # Show all migrations
```

### Stuck Migration
```bash
flask db downgrade -1  # Go back one migration
# Fix the issue
flask db upgrade  # Try again
```

---

## 📚 Documentation

- Flask-Migrate: https://flask-migrate.readthedocs.io/
- Alembic: https://alembic.sqlalchemy.org/

---

## ✅ Current Status

- ✅ Flask-Migrate installed
- ✅ Migrations folder initialized
- ✅ Code updated in `app/__init__.py`
- ✅ `requirements.txt` updated
- ⏳ **TODO**: Run `flask db stamp head` in production (Render Shell)

---

**Note**: The old `RESET_DB` environment variable is no longer used. Remove it from Render if it exists.
