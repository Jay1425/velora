"""
Database models for Velora application.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy (will be configured in app factory)
db = SQLAlchemy()


class Inquiry(db.Model):
    """Customer inquiry model for orders and questions."""
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    flavor = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(20), nullable=False)
    event_date = db.Column(db.String(20))
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='submitted', nullable=False)  # submitted, accepted, fulfilled, dispatched, delivered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Inquiry {self.order_number} - {self.name}>'
    
    @staticmethod
    def generate_order_number():
        """Generate unique order number with format VEL-YYYYMMDD-XXXX"""
        from datetime import datetime
        date_str = datetime.now().strftime('%Y%m%d')
        # Count today's orders
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = Inquiry.query.filter(Inquiry.created_at >= today_start).count() + 1
        return f"VEL-{date_str}-{today_count:04d}"


# Premium Flavors Collection (4 flavors)
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
