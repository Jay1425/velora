# Velora - Premium Shrikhand D2C Website

A clean, elegant Flask website for **Velora**, a premium Indian shrikhand brand.  
Part of the legacy of **Rasik Pan & Cold Drinks**, established **04 April 1983** in Kutiyana, Gujarat.

---

## ⚠️ SECURITY NOTICE

**This repository contains production-grade security implementations:**

🔒 **Never commit these files to version control:**
- `.env` (contains real credentials)
- `*.db` (customer database)
- `instance/` (Flask instance folder)
- `.venv/` (virtual environment)

✅ **Safe to commit:**
- `.env.example` (template only)
- All code and templates
- Documentation files

📖 **Setup Guide:** See [Quick Start](#-quick-start) below  
🔐 **Security Details:** See [SECURITY_IMPLEMENTATION.md](SECURITY_IMPLEMENTATION.md)  
🤝 **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🌟 Overview

Velora is a minimal, production-ready D2C dessert brand website focused on:
- **Premium branding** for weddings and celebrations
- **Inquiry-based orders** (not e-commerce)
- **SQLite database** for storing customer inquiries
- **Admin dashboard** for managing orders
- **Clean, boutique aesthetic** without flashy animations
- **Production-grade security** with enterprise-level authentication

---

## 🎨 Design System

**Color Palette:**
- **Cream Background:** `#F5E6C8`
- **Deep Saffron Accent:** `#C96A00`
- **White Cards**
- **Gray-900 Footer**

**Typography:**
- **Headings:** Cormorant Garamond (serif)
- **Body:** Inter (sans-serif)

**Design Philosophy:**
- Minimal and elegant
- Clean spacing and breathing room
- Subtle shadows only
- No flashy gradients or heavy animations
- Luxury boutique feel

---

## 📁 Project Structure

```
velora/
│
├── app.py                  # Flask app with SQLAlchemy database
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── velora.db              # SQLite database (auto-created)
│
├── static/
│   └── img/
│       └── flavours/
│           ├── classic-mango.jpg
│           ├── mix-fruit-delight.jpg
│           ├── rajbhog-reserve.jpg
│           └── kesar-royale.jpg
│
└── templates/
    ├── index.html         # Home page
    ├── legacy.html        # Brand story page
    ├── flavors.html       # Product catalog (4 flavors only)
    ├── bulk.html          # Bulk & wedding orders info
    ├── contact.html       # Inquiry form
    └── admin.html         # Admin dashboard
```

---

## 🍨 Product Catalog

**EXACTLY 4 FLAVORS:**

1. **Classic Mango** – ₹260 / kg
2. **Mix Fruit Delight** – ₹260 / kg
3. **Rajbhog Reserve** – ₹280 / kg
4. **Kesar Royale** – ₹300 / kg

**Pack Sizes:**
- 1 kg (small gatherings)
- 2 kg (family functions)
- 5 kg+ (weddings & events)

---

## 🚀 Quick Start

### 1. Set Environment Variables

**Required for Admin Access:**

**IMPORTANT:** Admin passwords are now stored as hashed values for security.

**Step 1: Generate Password Hash**

```bash
# Run this Python command to generate a secure password hash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your_password_here'))"
```

This will output a hash like:
```
scrypt:32768:8:1$abc123...xyz789
```

**Step 2: Configure Environment Variables**

Create a `.env` file in your project root:

```env
# Velora Admin Configuration
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD_HASH=scrypt:32768:8:1$your_generated_hash_here
SECRET_KEY=your-random-secret-key-here
```

**OR use system environment variables:**

```bash
# Windows PowerShell
setx ADMIN_USERNAME "your_admin_username"
setx ADMIN_PASSWORD_HASH "scrypt:32768:8:1$your_generated_hash_here"
setx SECRET_KEY "your-random-secret-key-here"

# Windows CMD
set ADMIN_USERNAME=your_admin_username
set ADMIN_PASSWORD_HASH=scrypt:32768:8:1$your_generated_hash_here
set SECRET_KEY=your-random-secret-key-here

# Mac/Linux
export ADMIN_USERNAME="your_admin_username"
export ADMIN_PASSWORD_HASH="scrypt:32768:8:1$your_generated_hash_here"
export SECRET_KEY="your-random-secret-key-here"
```

**Generate a strong SECRET_KEY:**

```bash
python -c "import os; print(os.urandom(24).hex())"
```

**Optional:**

```bash
# Enable debug mode (default: False in production)
setx FLASK_DEBUG "true"  # Windows
export FLASK_DEBUG="true"  # Mac/Linux
```

**Note:** Using `.env` file (recommended for development) - no need to restart terminal. For `setx` method, restart your terminal or IDE.

### 2. Install Dependencies

```bash
# Activate virtual environment (if using one)
.venv\Scripts\Activate.ps1  # Windows PowerShell
# OR
source .venv/bin/activate   # Mac/Linux

# Install required packages
pip install -r requirements.txt
```

### 3. Add Product Images

Place these images in `static/img/flavours/`:
- `classic-mango.jpg`
- `mix-fruit-delight.jpg`
- `rajbhog-reserve.jpg`
- `kesar-royale.jpg`

**Image Guidelines:**
- Format: `.jpg` (recommended)
- Size: 800x800px (square, high quality)
- Clean, well-lit product photos

### 4. Run the Application

```bash
python app.py
```

Visit: **http://127.0.0.1:5000/**

The SQLite database (`velora.db`) will be created automatically on first run.

---

## 📄 Pages & Routes

| Route | Page | Purpose |
|-------|------|---------|
| `/` | Home | Hero, featured flavors, wedding banner |
| `/legacy` | Our Legacy | Brand storytelling since 1983 |
| `/flavors` | Flavors | 4 product catalog with pricing |
| `/bulk` | Bulk Orders | Wedding & corporate event info |
| `/contact` | Contact Form | Customer inquiry form (with WhatsApp redirect) |
| `/admin` | Admin Dashboard | Protected analytics & inquiry management |
| `/admin/login` | Admin Login | Secure authentication page |
| `/admin/logout` | Admin Logout | Secure session termination |

---

## 💾 Database Structure

**Inquiry Model:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String(100) | Customer name |
| `phone` | String(20) | Phone number |
| `flavor` | String(50) | Selected flavor |
| `quantity` | String(20) | Order quantity |
| `event_date` | String(20) | Optional event date |
| `message` | Text | Optional message |
| `created_at` | DateTime | Auto-generated timestamp (UTC) |

---

## 🔐 Admin Dashboard

**Access:** `/admin` (Protected - Login Required)

**Login:** `/admin/login`

### Production-Grade Security

The Velora admin panel implements **enterprise-level security** with multiple layers of protection.

### Setup

**1. Generate Password Hash:**

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YourSecurePassword123!'))"
```

**2. Configure Credentials in `.env` file:**

```env
ADMIN_USERNAME=velora_admin
ADMIN_PASSWORD_HASH=scrypt:32768:8:1$your_hash_here
SECRET_KEY=your-random-secret-key-here
```

### Security Features

**🔒 Password Security:**
- ✅ Werkzeug scrypt hashing (NOT plain text)
- ✅ Passwords never stored or compared in plain text
- ✅ Industry-standard password hashing

**🛡️ CSRF Protection:**
- ✅ Flask-WTF CSRF tokens on all forms
- ✅ Prevents cross-site request forgery attacks
- ✅ Automatic token validation

**⏱️ Rate Limiting & Lockout:**
- ✅ Maximum 5 failed login attempts
- ✅ 15-minute lockout after 5 failures
- ✅ Remaining attempts displayed in UI
- ✅ Lockout timer shown to user

**🍪 Secure Session Configuration:**
- ✅ HTTPOnly cookies (JavaScript cannot access)
- ✅ Secure flag in production (HTTPS only)
- ✅ SameSite=Lax prevents CSRF
- ✅ 30-minute session timeout

**📋 Security Logging:**
- ✅ All login attempts logged with IP address
- ✅ Failed attempts tracked with timestamps
- ✅ Admin actions logged for audit trail
- ✅ Lockout events recorded

**🔐 Security Headers:**
- ✅ X-Frame-Options: DENY (prevents clickjacking)
- ✅ X-Content-Type-Options: nosniff
- ✅ Referrer-Policy: no-referrer
- ✅ Content-Security-Policy configured
- ✅ No-cache headers on admin pages

**🌐 HTTPS Enforcement:**
- ✅ Automatic HTTP → HTTPS redirect in production
- ✅ Disabled in debug mode for local development

### Dashboard Features

- **Analytics Cards:**
  - Total inquiries
  - This month's inquiries
  - Most requested flavor
  - Average order quantity
  
- **Inquiry Filters:**
  - All Time
  - This Month
  - Today
  
- **Data Table:**
  - Customer details (name, phone)
  - Order information (flavor, quantity)
  - Event date
  - Custom messages
  - Timestamps

### Access Flow

1. Visit `/admin` → Redirects to `/admin/login` if not authenticated
2. Login with credentials
   - Failed attempts show remaining tries
   - After 5 failures: 15-minute lockout
3. Successful login grants 30-minute session
4. Click "Logout" to securely end session (clears all session data)

### Security Best Practices

**For Production:**

1. **Use Strong Passwords:**
   - Minimum 12 characters
   - Mix uppercase, lowercase, numbers, symbols
   - Never reuse passwords

2. **Secure Your `.env` File:**
   - Add `.env` to `.gitignore` (already done)
   - Never commit credentials to version control
   - Use different passwords for dev/production

3. **Enable HTTPS:**
   - Required for secure cookies
   - Use SSL certificate in production
   - Flask auto-redirects HTTP to HTTPS

4. **Monitor Logs:**
   - Check admin access logs regularly
   - Watch for suspicious login patterns
   - Track failed login attempts

5. **Regular Security Updates:**
   - Keep Flask and dependencies updated
   - Rotate SECRET_KEY periodically
   - Review security logs monthly

### Troubleshooting

**"Admin credentials not configured"**
- Check `.env` file exists in project root
- Verify `ADMIN_USERNAME` and `ADMIN_PASSWORD_HASH` are set
- Ensure password is **hashed**, not plain text

**"Account temporarily locked"**
- Wait 15 minutes after 5 failed attempts
- Clear browser cookies if needed
- Check you're using the correct password

**CSRF Token Error**
- Ensure Flask-WTF is installed: `pip install Flask-WTF`
- Clear browser cache and cookies
- Check CSRF is enabled in `app.py`

---

## 📝 Customization

### Update Brand Information

In `app.py`, edit the `FLAVOURS` list to modify products:

```python
FLAVOURS = [
    {
        'name': 'Classic Mango',
        'description': 'Premium Alphonso mangoes...',
        'image': 'classic-mango.jpg',
        'price': '₹260 / kg'
    },
    # Add more (but keep it minimal)
]
```

### Modify Footer Contact

Update footer in all template files:
- Replace placeholders with actual contact details
- Update location information

---

## 🌐 Deployment

### ⭐ Recommended: Render + Neon PostgreSQL (Production-Ready)

**Complete deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)

**Quick Setup:**

1. **Create Neon PostgreSQL Database** (free tier)
   - Sign up at [neon.tech](https://neon.tech)
   - Create project and get connection URL

2. **Deploy to Render** (free tier available)
   - Push code to GitHub
   - Connect repo to [render.com](https://render.com)
   - Create new "Web Service"
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   
3. **Set Environment Variables in Render:**
   ```env
   SECRET_KEY=your-generated-secret-key
   ADMIN_USERNAME=velora_admin
   ADMIN_PASSWORD_HASH=scrypt:32768:8:1$your_hash_here
   DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
   ```

4. **Deploy!** 
   - Automatic deployment on git push
   - HTTPS enabled automatically
   - Production-ready in 5 minutes

**Features:**
- ✅ PostgreSQL database (scalable, production-grade)
- ✅ SQLite fallback for local development
- ✅ Gunicorn WSGI server (production server)
- ✅ Auto-deploy from GitHub
- ✅ Free SSL certificate
- ✅ Zero-downtime deployments
- ✅ Connection pooling configured

---

### Alternative: PythonAnywhere (SQLite only)

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload project files
3. Set up Flask web app
4. Install dependencies via Bash console
5. Configure environment variables
6. **Note:** Uses SQLite (good for small projects)

---

### Alternative: Heroku

1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:mini
   git push heroku main
   ```

**Note:** Heroku sets `DATABASE_URL` automatically.

---

## � Security Features

The Velora admin panel includes enterprise-grade security:

**Authentication:**
- Session-based login system with `@admin_required` decorator
- Credentials stored in environment variables (never hardcoded)
- Secure session management with Flask server-side sessions

**Protection Measures:**
- Rate limiting: Maximum 5 failed login attempts per session
- No-cache headers on all admin pages
- Secure logout with complete session clearing
- Failed attempt counter resets on successful login

**Best Practices:**
- SECRET_KEY from environment or auto-generated
- Debug mode disabled by default in production
- Environment variable validation
- Graceful error handling for missing credentials

**Production Security Recommendations:**
- Use HTTPS/SSL in production
- Set strong SECRET_KEY (24+ random bytes)
- Use strong admin passwords (12+ characters, mixed case, numbers, symbols)
- Consider adding IP whitelisting for admin access
- Regularly backup the SQLite database
- Monitor `velora.db` file permissions

---

## 🔧 Technical Stack

**Backend:**
- **Framework:** Flask 3.0.0
- **Database:** Flask-SQLAlchemy 3.1.1
  - **Production:** PostgreSQL (Neon)
  - **Development:** SQLite (fallback)
- **Database Driver:** psycopg2-binary 2.9.9 (PostgreSQL)
- **WSGI Server:** Gunicorn 21.2.0 (production)
- **Security:** Flask-WTF 1.2.1 (CSRF Protection)
- **Password Hashing:** Werkzeug 3.0.1 (scrypt)
- **Environment:** python-dotenv 1.0.0

**Frontend:**
- **Templating:** Jinja2
- **CSS:** Tailwind CSS (via CDN)
- **Fonts:** Google Fonts (Cormorant Garamond, Inter)
- **Icons:** Emojis (universal support)

**Infrastructure:**
- **Hosting:** Render (recommended)
- **Database:** Neon PostgreSQL (recommended)
- **SSL:** Automatic (Render provides)
- **CI/CD:** Auto-deploy from GitHub

---

## ✅ Production Checklist

Before going live:

**Website Content:**
- [ ] Add real product images (4 flavors)
- [ ] Update contact information in footer
- [ ] Add `robots.txt` and `sitemap.xml` for SEO

**Security Configuration (CRITICAL):**
- [x] ✅ Production-grade authentication with password hashing
- [x] ✅ CSRF protection enabled (Flask-WTF)
- [x] ✅ Rate limiting with 15-minute lockout
- [x] ✅ Secure session configuration (HTTPOnly, Secure, SameSite)
- [x] ✅ Security headers implemented
- [x] ✅ HTTPS enforcement in production
- [x] ✅ Admin access logging with IP tracking
- [x] ✅ Debug mode disabled by default

**Production Environment Setup:**

- [ ] **Create Neon PostgreSQL database:**
  - Sign up at https://neon.tech
  - Create project and get DATABASE_URL
  
- [ ] **Deploy to Render:**
  - Connect GitHub repository
  - Set start command: `gunicorn app:app`
  
- [ ] **Set environment variables on Render:**
  - `DATABASE_URL` (from Neon PostgreSQL)
  - `ADMIN_USERNAME` (e.g., velora_admin)
  - `ADMIN_PASSWORD_HASH` (generate with: `python generate_password_hash.py`)
  - `SECRET_KEY` (generate: `python -c "import os; print(os.urandom(24).hex())"`)
  - `FLASK_DEBUG=false` (explicitly disable debug mode)
  
- [ ] **Verify deployment:**
  - Test HTTPS redirect (HTTP → HTTPS)
  - Test admin login and rate limiting
  - Submit test inquiry via contact form
  - Verify WhatsApp redirect works
  - Check admin analytics dashboard
  
- [ ] **Security verification:**
  - Confirm CSRF protection active
  - Test 15-minute lockout after 5 failed logins
  - Verify session timeout (30 minutes)
  - Check security headers in browser devtools

**Testing:**
- [ ] Test inquiry form submission with WhatsApp redirect
- [ ] Verify admin login with correct credentials
- [ ] Test failed login attempts (should lock after 5)
- [ ] Verify 15-minute lockout functionality
- [ ] Test admin logout and session clearing
- [ ] Test admin analytics dashboard with filters
- [ ] Verify CSRF protection on forms
- [ ] Test on mobile devices

**Deployment & Monitoring:**
- [ ] Set up proper database backups (daily recommended)
- [ ] Configure database file permissions (chmod 600 velora.db)
- [ ] Review admin access logs after deployment
- [ ] Monitor failed login attempts
- [ ] Document admin credentials securely (password manager)

---

## 📊 SEO Features

✅ Clean semantic HTML structure  
✅ Meta descriptions on all pages  
✅ Mobile-responsive design  
✅ Fast loading (CDN-based CSS)  
✅ Descriptive page titles  

**To Improve SEO Further:**
- Add Google Analytics
- Register with Google Search Console
- Create `robots.txt` file
- Generate `sitemap.xml`

---

## 🎯 Key Features

**Business & Customer Experience:**
- **Inquiry-Based Ordering:** No shopping cart — customers submit inquiries with WhatsApp auto-redirect
- **Personal Touch:** "We respond within 24 hours" messaging throughout
- **Wedding Focus:** Dedicated bulk order page emphasizing celebrations
- **Legacy Storytelling:** Strong brand narrative dating back to 1983
- **WhatsApp Integration:** Automatic redirect after form submission with pre-filled details
- **Mobile-First Design:** Fully responsive across all devices

**Production-Grade Security:**
- **Password Hashing:** Werkzeug scrypt hashing (passwords never stored in plain text)
- **CSRF Protection:** Flask-WTF tokens prevent cross-site attacks
- **Rate Limiting:** 5 login attempts max, 15-minute lockout protection
- **Secure Sessions:** HTTPOnly, Secure, SameSite cookies with 30-min timeout
- **Security Headers:** X-Frame-Options, CSP, nosniff, no-referrer
- **HTTPS Enforcement:** Automatic redirect in production
- **Audit Logging:** IP tracking, timestamps, failed attempt monitoring

**Admin Dashboard:**
- **Data-Driven Insights:** Most requested flavors, average quantities, monthly trends
- **Analytics Cards:** Total inquiries, monthly stats, flavor analysis
- **Inquiry Filters:** All time, this month, today
- **Secure Access:** Session-based authentication with automatic timeout

---

## 📞 Brand Details

**Brand Name:** Velora  
**Tagline:** Crafted with Legacy Since 1983  
**Parent Brand:** Rasik Pan & Cold Drinks  
**Established:** 04 April 1983  
**Location:** Kutiyana, Gujarat, India  
**Positioning:** Premium Shrikhand for Celebrations, Weddings & Special Moments

---

## 📄 License

Custom website built for Velora. All rights reserved.

---

**Velora — Handcrafted with Legacy Since 1983**
