# Velora - Premium Shrikhand D2C Website

A clean, elegant Flask website for **Velora**, a premium Indian shrikhand brand.  
Part of the legacy of **Rasik Pan & Cold Drinks**, established **04 April 1983** in Kutiyana, Gujarat.

---

## 🌟 Overview

Velora is a minimal, production-ready D2C dessert brand website focused on:
- **Premium branding** for weddings and celebrations
- **Inquiry-based orders** (not e-commerce)
- **SQLite database** for storing customer inquiries
- **Admin dashboard** for managing orders
- **Clean, boutique aesthetic** without flashy animations

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

### 1. Install Dependencies

```bash
# Activate virtual environment (if using one)
.venv\Scripts\Activate.ps1  # Windows PowerShell
# OR
source .venv/bin/activate   # Mac/Linux

# Install required packages
pip install -r requirements.txt
```

### 2. Add Product Images

Place these images in `static/img/flavours/`:
- `classic-mango.jpg`
- `mix-fruit-delight.jpg`
- `rajbhog-reserve.jpg`
- `kesar-royale.jpg`

**Image Guidelines:**
- Format: `.jpg` (recommended)
- Size: 800x800px (square, high quality)
- Clean, well-lit product photos

### 3. Run the Application

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
| `/contact` | Contact Form | Customer inquiry form (with database) |
| `/admin` | Admin Dashboard | View all inquiries |

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

**Access:** `/admin`

**Features:**
- View all customer inquiries
- Sort by latest first
- Display total inquiry count
- Clean table layout with:
  - Customer name & phone (clickable)
  - Flavor & quantity
  - Event date
  - Custom message
  - Submission timestamp

**Note:** No authentication required (add authentication for production use).

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

### Option 1: PythonAnywhere (Free)

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload project files
3. Set up Flask web app
4. Install dependencies via Bash console
5. Set working directory to project folder

### Option 2: Render (Recommended)

1. Push code to GitHub
2. Connect repo to [render.com](https://render.com)
3. Create new "Web Service"
4. Select Python environment
5. Build command: `pip install -r requirements.txt`
6. Start command: `python app.py`

### Option 3: Heroku

1. Update `app.py` for production:
   ```python
   if __name__ == '__main__':
       import os
       port = int(os.environ.get("PORT", 5000))
       app.run(host='0.0.0.0', port=port)
   ```

2. Create `Procfile`:
   ```
   web: python app.py
   ```

3. Deploy:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku create your-app-name
   git push heroku main
   ```

---

## 🔧 Technical Stack

- **Framework:** Flask 3.0.0
- **Database:** Flask-SQLAlchemy 3.1.1 with SQLite
- **Templating:** Jinja2
- **CSS:** Tailwind CSS (via CDN)
- **Fonts:** Google Fonts (Cormorant Garamond, Inter)
- **Icons:** Emojis (universal support)

---

## ✅ Production Checklist

Before going live:

- [ ] Add real product images (4 flavors)
- [ ] Update contact information in footer
- [ ] Add authentication to `/admin` route
- [ ] Set `app.config['SECRET_KEY']` to a secure random string
- [ ] Change `debug=True` to `debug=False` in production
- [ ] Set up proper database backups
- [ ] Add `robots.txt` and `sitemap.xml` for SEO
- [ ] Configure environment variables for sensitive data
- [ ] Test inquiry form submission
- [ ] Verify admin dashboard displays inquiries correctly

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

- **Inquiry-Based Ordering:** No shopping cart — customers submit inquiries
- **Personal Touch:** "We respond within 24 hours" messaging throughout
- **Wedding Focus:** Dedicated bulk order page emphasizing celebrations
- **Legacy Storytelling:** Strong brand narrative dating back to 1983
- **Clean Admin Panel:** Simple dashboard to manage customer inquiries
- **Mobile-First Design:** Fully responsive across all devices

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
