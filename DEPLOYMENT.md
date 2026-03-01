# Velora - Render Deployment Guide

Complete guide for deploying Velora to Render with Neon PostgreSQL.

---

## 📋 Prerequisites

1. **GitHub Account** with Velora repository pushed
2. **Render Account** (free tier available at https://render.com)
3. **Neon PostgreSQL** database (free tier at https://neon.tech)

---

## 🗄️ Step 1: Create Neon PostgreSQL Database

### 1. Sign up for Neon

Visit https://neon.tech and create an account (free tier available).

### 2. Create a New Project

1. Click "Create Project"
2. Project name: `velora-db`
3. Region: Choose closest to your users (e.g., US East, EU West)
4. Click "Create Project"

### 3. Get Database Connection String

After creating the project, you'll see a connection string like:

```
postgresql://username:password@ep-cool-darkness-123456.us-east-2.aws.neon.tech/velora?sslmode=require
```

**Save this URL** - you'll need it for Render!

---

## 🚀 Step 2: Deploy to Render

### 1. Sign up for Render

Visit https://render.com and sign up (GitHub login recommended).

### 2. Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub account
3. Select the `velora` repository
4. Click "Connect"

### 3. Configure Web Service

**Basic Settings:**
- **Name:** `velora` (or your preferred name)
- **Region:** Same as your Neon database region
- **Branch:** `main`
- **Root Directory:** (leave blank)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

**Instance Type:**
- Free tier is sufficient for testing
- Upgrade to paid for production traffic

### 4. Set Environment Variables

Click "Advanced" → "Add Environment Variable" and add:

**Required Variables:**

```env
SECRET_KEY=your-generated-secret-key-48-characters-minimum
ADMIN_USERNAME=velora_admin
ADMIN_PASSWORD_HASH=scrypt:32768:8:1$your_hash_here
DATABASE_URL=postgresql://username:password@ep-cool-darkness-123456.us-east-2.aws.neon.tech/velora?sslmode=require
```

**How to Generate Values:**

```bash
# SECRET_KEY (run locally)
python -c "import os; print(os.urandom(24).hex())"

# ADMIN_PASSWORD_HASH (run locally)
python generate_password_hash.py
```

**Optional Variables:**

```env
FLASK_DEBUG=false
PORT=10000
```

*(Note: Render sets PORT automatically, but you can override)*

### 5. Deploy!

1. Click "Create Web Service"
2. Render will:
   - Clone your repository
   - Install dependencies
   - Start gunicorn server
3. Wait 2-3 minutes for deployment

---

## ✅ Step 3: Verify Deployment

### 1. Check Deployment Status

Monitor the deployment logs in Render dashboard:
- ✅ "Build successful"
- ✅ "Deploy live"

### 2. Test Your Site

Visit your Render URL (e.g., `https://velora.onrender.com`):

**Test Pages:**
- Homepage: `https://velora.onrender.com/`
- Admin Login: `https://velora.onrender.com/admin/login`
- Legacy Page: `https://velora.onrender.com/legacy`

### 3. Test Admin Login

1. Go to `/admin/login`
2. Enter your credentials
3. Verify dashboard loads
4. Submit a test inquiry from contact form
5. Check if it appears in admin dashboard

---

## 🔧 Step 4: Database Migration (If Needed)

If you have existing SQLite data to migrate:

### Option 1: Manual Export/Import

**Export from SQLite:**
```bash
# Local machine
sqlite3 instance/velora.db .dump > velora_dump.sql
```

**Import to PostgreSQL:**
```bash
# Use Neon SQL Editor or psql
psql "postgresql://username:password@host/velora?sslmode=require" < velora_dump.sql
```

### Option 2: Fresh Start

Just deploy without migration - the app will create empty tables automatically.

---

## 🎯 Step 5: Custom Domain (Optional)

### 1. In Render Dashboard

1. Go to your web service
2. Click "Settings"
3. Scroll to "Custom Domain"
4. Click "Add Custom Domain"
5. Enter your domain: `velora.com`

### 2. Configure DNS

Add these records to your domain registrar:

**For Root Domain (velora.com):**
```
Type: A
Name: @
Value: [Render IP from dashboard]
```

**For www Subdomain:**
```
Type: CNAME
Name: www
Value: velora.onrender.com
```

### 3. SSL Certificate

Render provides free SSL automatically via Let's Encrypt.

---

## 🔐 Security Checklist

Before going live:

- [ ] **Environment Variables Set:**
  - ✅ `SECRET_KEY` (strong, 48+ characters)
  - ✅ `ADMIN_PASSWORD_HASH` (hashed, not plain text)
  - ✅ `DATABASE_URL` (Neon PostgreSQL URL)
  - ✅ `ADMIN_USERNAME` (not "admin")
  
- [ ] **Debug Mode Disabled:**
  - ✅ `FLASK_DEBUG=false` or not set
  
- [ ] **HTTPS Enabled:**
  - ✅ Render provides SSL automatically
  
- [ ] **Database Connection Secure:**
  - ✅ `?sslmode=require` in DATABASE_URL
  
- [ ] **Test Security Features:**
  - ✅ Rate limiting works (5 failed logins)
  - ✅ 15-minute lockout activates
  - ✅ CSRF protection enabled
  - ✅ Admin logout clears session

---

## 📊 Monitoring & Maintenance

### Render Dashboard

Monitor your app:
- **Metrics:** CPU, memory, request rate
- **Logs:** Real-time application logs
- **Events:** Deployment history

### Neon Dashboard

Monitor your database:
- **Connections:** Active connections, pool usage
- **Storage:** Database size
- **Queries:** Slow queries, performance

### Set Up Alerts

1. Render: Configure email alerts for:
   - Deploy failures
   - High error rates
   - Service downtime

2. Neon: Configure alerts for:
   - Storage limits
   - Connection limits
   - Database errors

---

## 🐛 Troubleshooting

### App Won't Start

**Error: "Application failed to respond"**

Check Render logs for:
```bash
# Missing environment variables
WARNING: ADMIN_USERNAME not set

# Database connection issues
ERROR: could not connect to server

# Port binding issues
ERROR: Failed to bind to 0.0.0.0:10000
```

**Solutions:**
1. Verify all environment variables are set
2. Check DATABASE_URL format
3. Ensure gunicorn is in requirements.txt

### Database Connection Errors

**Error: "could not connect to server"**

1. Verify DATABASE_URL is correct
2. Check Neon database is active (not suspended)
3. Ensure `?sslmode=require` is in URL
4. Confirm database exists in Neon

### Admin Login Not Working

**Error: "Admin credentials not configured"**

1. Verify environment variables in Render:
   - `ADMIN_USERNAME` is set
   - `ADMIN_PASSWORD_HASH` is set (not `ADMIN_PASSWORD`)
2. Restart the service after setting variables

### CSRF Token Errors

**Error: "The CSRF token is missing"**

1. Clear browser cookies
2. Verify SECRET_KEY is set in Render
3. Check HTTPS is enabled (Render does this automatically)

### 502 Bad Gateway

**Possible causes:**
1. App crashed during startup
2. Gunicorn not running
3. Port misconfiguration

**Solutions:**
1. Check Render logs for crash details
2. Verify start command: `gunicorn app:app`
3. Don't set PORT manually (Render sets it)

---

## 🔄 Updates & Redeploys

### Automatic Deploys

Render auto-deploys when you push to GitHub:

```bash
# Local machine
git add .
git commit -m "Update feature"
git push origin main

# Render automatically:
# 1. Detects push
# 2. Runs build command
# 3. Deploys new version
# 4. Zero-downtime deployment
```

### Manual Deploy

In Render dashboard:
1. Go to your web service
2. Click "Manual Deploy" → "Deploy latest commit"

### Rollback

If deployment fails:
1. Go to "Events" tab
2. Find previous successful deploy
3. Click "Rollback to this version"

---

## 💰 Cost Breakdown

### Free Tier (Sufficient for Testing)

**Render Free:**
- 750 hours/month
- Auto-sleeps after 15 minutes inactivity
- Wakes up on request (cold start ~30s)

**Neon Free:**
- 10 GB storage
- Unlimited compute hours
- Auto-scales to zero when inactive

**Total: $0/month**

### Production Tier (Recommended)

**Render Starter: $7/month**
- Always on (no sleep)
- 512 MB RAM
- Custom domain
- SSL included

**Neon Pro: $19/month**
- 50 GB storage
- Higher connection limits
- Point-in-time restore
- Better performance

**Total: ~$26/month**

---

## 📚 Additional Resources

**Render Docs:**
- Web Services: https://render.com/docs/web-services
- Environment Variables: https://render.com/docs/environment-variables
- Deploy Hooks: https://render.com/docs/deploy-hooks

**Neon Docs:**
- Getting Started: https://neon.tech/docs/get-started-with-neon
- Connection Strings: https://neon.tech/docs/connect/connection-string
- Branching: https://neon.tech/docs/introduction/branching

**Flask Production:**
- Deployment: https://flask.palletsprojects.com/en/3.0.x/deploying/
- Gunicorn: https://docs.gunicorn.org/

---

## ✅ Deployment Complete!

Your Velora website is now:
- ✅ Running on Render (production server)
- ✅ Using Neon PostgreSQL (scalable database)
- ✅ HTTPS enabled (secure)
- ✅ Auto-deploying from GitHub (CI/CD)
- ✅ Production-grade security (authentication, CSRF, rate limiting)

**Your Production URL:** `https://your-app-name.onrender.com`

---

## 🎉 What's Next?

1. **Test thoroughly** - Try all features
2. **Monitor logs** - Watch for errors
3. **Set up custom domain** - Professional URL
4. **Configure backups** - Protect your data
5. **Add analytics** - Track user behavior

**Need Help?**
- Render Support: https://render.com/docs/support
- Neon Support: https://neon.tech/docs/introduction/support
- GitHub Issues: https://github.com/Jay1425/velora/issues

---

**Deployed:** March 1, 2026  
**Stack:** Flask + Gunicorn + PostgreSQL (Neon) + Render  
**Status:** Production-Ready 🚀
