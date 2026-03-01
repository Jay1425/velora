# Quick Setup Guide - Velora

A streamlined guide to get Velora running locally in 5 minutes.

---

## Prerequisites

- Python 3.8+ installed
- Git installed
- Terminal/Command Prompt

---

## 🚀 Quick Start (5 Minutes)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/velora.git
cd velora
```

### 2️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Generate admin password hash
python generate_password_hash.py
# Enter your desired password when prompted
# Copy the generated hash

# Edit .env file and paste the hash
# On Windows: notepad .env
# On Mac/Linux: nano .env
```

**Your `.env` should look like:**
```env
ADMIN_USERNAME=velora_admin
ADMIN_PASSWORD_HASH=scrypt:32768:8:1$YourGeneratedHashHere
SECRET_KEY=your-generated-secret-key-here
```

**Generate SECRET_KEY:**
```bash
python -c "import os; print(os.urandom(24).hex())"
```

### 5️⃣ Run Application

```bash
python app.py
```

**Visit:** http://127.0.0.1:5000

---

## 🎉 You're Done!

**Test the site:**
- Homepage: http://127.0.0.1:5000
- Admin Login: http://127.0.0.1:5000/admin/login

**Admin Credentials:**
- Username: (what you set in .env)
- Password: (what you used to generate the hash)

---

## 📁 Expected File Structure

```
velora/
├── .env                    # Your local config (DO NOT COMMIT)
├── .env.example            # Template (safe to commit)
├── .gitignore              # Protects sensitive files
├── app.py                  # Main Flask application
├── generate_password_hash.py  # Password hash generator
├── requirements.txt        # Python dependencies
├── README.md               # Full documentation
├── SECURITY_IMPLEMENTATION.md  # Security details
├── CONTRIBUTING.md         # Contribution guidelines
├── instance/
│   └── velora.db          # Database (auto-created)
├── static/
│   └── img/
│       └── flavours/      # Product images
├── templates/             # HTML templates
└── .venv/                 # Virtual environment (auto-created)
```

---

## 🔒 Security Checklist

Before starting development:

- [x] `.env` file created (not committed)
- [x] Password hash generated (not plain text)
- [x] SECRET_KEY generated (random 48+ characters)
- [x] `.gitignore` protecting sensitive files
- [x] Virtual environment activated

---

## 🐛 Troubleshooting

### "Admin credentials not configured"
- Check `.env` file exists in project root
- Verify `ADMIN_PASSWORD_HASH` (not `ADMIN_PASSWORD`)
- Restart Flask app after editing `.env`

### "Import error: flask_wtf"
```bash
pip install Flask-WTF
```

### "Database is locked"
- Close any other instances of the app
- Delete `instance/velora.db` and restart

### "Port 5000 already in use"
- Stop other Flask apps
- Or change port in `app.py`: `app.run(port=5001)`

---

## 📚 Next Steps

1. **Read Full Documentation:** [README.md](README.md)
2. **Understand Security:** [SECURITY_IMPLEMENTATION.md](SECURITY_IMPLEMENTATION.md)
3. **Contributing Guidelines:** [CONTRIBUTING.md](CONTRIBUTING.md)
4. **Add Product Images:** Place in `static/img/flavours/`
5. **Test Admin Panel:** Login and create test inquiries

---

## 🆘 Need Help?

- Open an issue on GitHub
- Check [README.md](README.md) for detailed documentation
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines

---

**Setup Time:** ~5 minutes  
**Difficulty:** Beginner-friendly  
**Status:** Production-ready 🚀
