"""
Main public routes for Velora website.
Handles homepage, legacy, flavors, bulk orders, contact form, and order tracking.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from urllib.parse import quote
from datetime import datetime, date
from app.models import db, Inquiry, FLAVOURS
from app.utils.receipt import generate_receipt_pdf

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
    Saves inquiry to database, generates receipt, and shows success page.
    """
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        phone = request.form.get('phone')
        flavor = request.form.get('flavor')
        quantity = request.form.get('quantity')
        event_date_str = request.form.get('event_date')
        message = request.form.get('message')
        
        # Validate event date (if provided) - must be future date
        if event_date_str:
            try:
                event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
                today = date.today()
                if event_date < today:
                    flash('Event date cannot be in the past. Please select a future date.', 'error')
                    return redirect(url_for('main.contact'))
            except ValueError:
                flash('Invalid date format. Please select a valid date.', 'error')
                return redirect(url_for('main.contact'))
        
        # Generate unique order number
        order_number = Inquiry.generate_order_number()
        
        # Create inquiry record
        inquiry = Inquiry(
            order_number=order_number,
            name=name,
            phone=phone,
            flavor=flavor,
            quantity=quantity,
            event_date=event_date_str,
            message=message,
            status='submitted'
        )
        
        try:
            # Save to database
            db.session.add(inquiry)
            db.session.commit()
            
            # Redirect to success page
            return redirect(url_for('main.order_success', order_number=order_number))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('main.contact'))
    
    return render_template('contact.html', flavours=FLAVOURS)


@main_bp.route('/order-success/<order_number>')
def order_success(order_number):
    """Display order success page with details."""
    order = Inquiry.query.filter_by(order_number=order_number).first()
    
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('order_success.html', order=order)


@main_bp.route('/download-receipt/<order_number>')
def download_receipt(order_number):
    """Generate and download PDF receipt for an order."""
    order = Inquiry.query.filter_by(order_number=order_number).first()
    
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('main.index'))
    
    try:
        # Generate PDF receipt
        pdf_buffer = generate_receipt_pdf(order)
        
        # Send as downloadable file
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'Velora_Receipt_{order_number}.pdf'
        )
    except Exception as e:
        flash('Error generating receipt. Please try again.', 'error')
        return redirect(url_for('main.track_order'))


@main_bp.route('/track')
def track_order():
    """Track order status by order number."""
    order_number = request.args.get('order')
    order = None
    searched = False
    
    if order_number:
        searched = True
        order = Inquiry.query.filter_by(order_number=order_number.strip().upper()).first()
    
    return render_template('track_order.html', 
                         order=order, 
                         searched=searched,
                         order_number_searched=order_number)
