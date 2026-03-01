from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'velora-premium-shrikhand-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///velora.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
        'image': 'classic-mango.jpg',
        'price': '₹260 / kg'
    },
    {
        'name': 'Mix Fruit Delight',
        'description': 'A harmonious blend of tropical fruits in creamy tradition',
        'image': 'mix-fruit-delight.jpg',
        'price': '₹260 / kg'
    },
    {
        'name': 'Rajbhog Reserve',
        'description': 'Royal saffron, nuts and rose essence - our signature luxury',
        'image': 'rajbhog-reserve.jpg',
        'price': '₹280 / kg'
    },
    {
        'name': 'Kesar Royale',
        'description': 'Pure Kashmir saffron in every spoonful - the ultimate indulgence',
        'image': 'kesar-royale.jpg',
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
        inquiry = Inquiry(
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            flavor=request.form.get('flavor'),
            quantity=request.form.get('quantity'),
            event_date=request.form.get('event_date'),
            message=request.form.get('message')
        )
        
        try:
            db.session.add(inquiry)
            db.session.commit()
            flash('Thank you. We personally respond within 24 hours.', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('contact'))
    
    return render_template('contact.html', flavours=FLAVOURS)

@app.route('/admin')
def admin():
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template('admin.html', inquiries=inquiries)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
