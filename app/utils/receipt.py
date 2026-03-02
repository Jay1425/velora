"""
PDF Receipt Generator for Velora Orders.
Generates professional order receipts with Velora branding.
"""
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas


def generate_receipt_pdf(inquiry):
    """
    Generate a professional PDF receipt for an order.
    
    Args:
        inquiry: Inquiry model instance
    
    Returns:
        BytesIO: PDF file as bytes buffer
    """
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#C96A00'),  # Saffron color
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#C96A00'),
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    # Company Header
    story.append(Paragraph("VELORA", title_style))
    story.append(Paragraph("Premium Shrikhand Since 1983", subtitle_style))
    story.append(Paragraph("Kutiyana, Gujarat | +91 94286 38301", subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Receipt Title
    story.append(Paragraph("ORDER RECEIPT", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Order Information Table
    order_data = [
        ['Order Number:', inquiry.order_number],
        ['Order Date:', inquiry.created_at.strftime('%d %B %Y, %I:%M %p')],
        ['Status:', inquiry.status.upper()],
    ]
    
    order_table = Table(order_data, colWidths=[2*inch, 4*inch])
    order_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5E6C8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    story.append(order_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Customer Details
    story.append(Paragraph("CUSTOMER DETAILS", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    customer_data = [
        ['Name:', inquiry.name],
        ['Phone:', inquiry.phone],
    ]
    
    customer_table = Table(customer_data, colWidths=[2*inch, 4*inch])
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5E6C8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    story.append(customer_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Order Details
    story.append(Paragraph("ORDER DETAILS", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    order_details_data = [
        ['Flavor:', inquiry.flavor],
        ['Quantity:', inquiry.quantity],
    ]
    
    if inquiry.event_date:
        order_details_data.append(['Event Date:', inquiry.event_date])
    
    if inquiry.message:
        order_details_data.append(['Message:', inquiry.message])
    
    order_details_table = Table(order_details_data, colWidths=[2*inch, 4*inch])
    order_details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5E6C8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(order_details_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Order Status Timeline
    story.append(Paragraph("ORDER STATUS", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Status definitions
    statuses = ['submitted', 'accepted', 'fulfilled', 'dispatched', 'delivered']
    status_labels = ['Submitted', 'Accepted', 'Fulfilled', 'Dispatched', 'Delivered']
    current_status_index = statuses.index(inquiry.status) if inquiry.status in statuses else 0
    
    status_data = []
    for i, (status, label) in enumerate(zip(statuses, status_labels)):
        if i <= current_status_index:
            status_data.append([f'✓ {label}', ''])
        else:
            status_data.append([f'○ {label}', 'Pending'])
    
    status_table = Table(status_data, colWidths=[3*inch, 3*inch])
    status_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, current_status_index), colors.HexColor('#C96A00')),
        ('TEXTCOLOR', (0, current_status_index + 1), (-1, -1), colors.grey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(status_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Thank you for choosing Velora Premium Shrikhand!", footer_style))
    story.append(Paragraph(f"Track your order at: www.velora.com/track?order={inquiry.order_number}", footer_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("For inquiries, WhatsApp us at +91 94286 38301", footer_style))
    
    # Build PDF
    doc.build(story)
    
    # Reset buffer position
    buffer.seek(0)
    
    return buffer


def get_status_display(status):
    """Get user-friendly status label."""
    status_map = {
        'submitted': 'Order Submitted',
        'accepted': 'Order Accepted',
        'fulfilled': 'Order Fulfilled',
        'dispatched': 'Order Dispatched',
        'delivered': 'Order Delivered'
    }
    return status_map.get(status, status.title())


def get_status_progress(status):
    """Get status progress percentage."""
    statuses = ['submitted', 'accepted', 'fulfilled', 'dispatched', 'delivered']
    if status in statuses:
        index = statuses.index(status)
        return int((index + 1) / len(statuses) * 100)
    return 0
