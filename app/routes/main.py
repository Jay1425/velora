"""
Main public routes for Velora website.
Handles homepage, legacy, flavors, bulk orders, and contact form.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from urllib.parse import quote
from app.models import db, Inquiry, FLAVOURS

# Create Blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage with featured flavors."""
    return render_template('index.html', flavours=FLAVOURS)


@main_bp.route('/legacy')
def legacy():
    """Our legacy and history page."""
    return render_template('legacy.html')


@main_bp.route('/flavors')
def flavors():
    """Full flavors catalog page."""
    return render_template('flavors.html', flavours=FLAVOURS)


@main_bp.route('/bulk')
def bulk():
    """Bulk orders information page."""
    return render_template('bulk.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Contact form for customer inquiries.
    Saves inquiry to database and redirects to WhatsApp.
    """
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        phone = request.form.get('phone')
        flavor = request.form.get('flavor')
        quantity = request.form.get('quantity')
        event_date = request.form.get('event_date')
        message = request.form.get('message')
        
        # Create inquiry record
        inquiry = Inquiry(
            name=name,
            phone=phone,
            flavor=flavor,
            quantity=quantity,
            event_date=event_date,
            message=message
        )
        
        try:
            # Save to database
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
            return redirect(url_for('main.contact'))
    
    return render_template('contact.html', flavours=FLAVOURS)
