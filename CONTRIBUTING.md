# Contributing to Velora

Thank you for your interest in contributing to Velora! This document provides guidelines for development and security practices.

---

## 🔐 Security First

**CRITICAL:** Never commit sensitive data to version control!

### Protected Files (Never Commit)

✅ Already protected by `.gitignore`:
- `.env` - Contains real credentials
- `*.db` - Database with customer data
- `instance/` - Flask instance folder
- `.venv/` - Virtual environment
- `__pycache__/` - Python cache

### Safe to Commit

✅ These files are safe and should be committed:
- `.env.example` - Template without credentials
- `app.py` - Application code
- `templates/` - HTML templates
- `static/` - Images and assets
- `requirements.txt` - Dependencies
- `README.md` - Documentation

---

## 🚀 Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/velora.git
cd velora
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Generate password hash
python generate_password_hash.py

# Generate SECRET_KEY
python -c "import os; print(os.urandom(24).hex())"

# Edit .env with your credentials
```

### 5. Run Application

```bash
python app.py
```

Visit: http://127.0.0.1:5000

---

## 🔒 Security Guidelines

### Password Management

**NEVER commit plain text passwords!**

1. Use `generate_password_hash.py` to create hashes
2. Store only hashes in `.env` (never on GitHub)
3. Use strong passwords (12+ characters)

### Environment Variables

```env
# .env (local only - never commit)
ADMIN_USERNAME=your_username
ADMIN_PASSWORD_HASH=scrypt:32768:8:1$...
SECRET_KEY=your-secret-key
```

### Production Deployment

1. Use server environment variables (not .env)
2. Enable HTTPS (automatic redirect configured)
3. Generate unique credentials per environment
4. Rotate secrets regularly
5. Monitor admin access logs

---

## 📝 Code Contribution Guidelines

### Before Submitting PR

- [ ] Test locally with clean database
- [ ] Verify no credentials in code
- [ ] Run security checks: `git diff` before commit
- [ ] Check `.gitignore` is protecting sensitive files
- [ ] Update documentation if needed
- [ ] Test admin authentication
- [ ] Verify CSRF protection works

### Commit Messages

Use clear, descriptive commit messages:

```bash
✅ Good:
git commit -m "Add rate limiting to admin login"
git commit -m "Fix CSRF token validation on contact form"

❌ Avoid:
git commit -m "fix stuff"
git commit -m "update"
```

### Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `security/` - Security improvements
- `docs/` - Documentation updates

Example: `feature/add-email-notifications`

---

## 🧪 Testing

### Test Admin Security

```bash
# Test lockout mechanism
# Try 5 wrong passwords - should lock for 15 minutes

# Test CSRF protection
# Disable CSRF in form - should fail

# Test session timeout
# Wait 30 minutes - should redirect to login
```

### Test Customer Flow

```bash
# Test inquiry form submission
# Test WhatsApp redirect
# Verify database entry created
```

---

## 🚨 Reporting Security Issues

**DO NOT open public issues for security vulnerabilities!**

If you discover a security issue:

1. Email: security@yourdomain.com (or DM maintainer)
2. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We'll respond within 48 hours.

---

## 📦 Dependency Management

### Adding New Dependencies

```bash
# Install package
pip install package-name

# Update requirements
pip freeze > requirements.txt
```

### Security Updates

```bash
# Check for vulnerabilities
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update requirements.txt
pip freeze > requirements.txt
```

---

## 🎨 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic
- Keep functions focused and small

---

## 📚 Documentation

When adding features, update:

- `README.md` - User-facing documentation
- `SECURITY_IMPLEMENTATION.md` - Security details
- Code comments - Inline documentation
- This file - Contributing guidelines

---

## ✅ Pre-Commit Checklist

Before every commit:

```bash
# 1. Check what you're committing
git status
git diff

# 2. Verify no sensitive files
git status | grep -E "\.env$|\.db$"  # Should be empty

# 3. Test locally
python app.py  # Verify it runs

# 4. Commit with clear message
git add .
git commit -m "Clear description of changes"
```

---

## 🙏 Thank You!

Your contributions help make Velora more secure and reliable.

For questions, open an issue or contact the maintainers.

---

**Last Updated:** March 1, 2026  
**Maintainer:** Velora Development Team
