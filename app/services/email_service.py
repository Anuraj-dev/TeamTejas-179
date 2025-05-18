from flask import current_app
from flask_mail import Message, Mail
from threading import Thread

# This is a placeholder - you'll need to add Flask-Mail to your extensions if you want to use this service
mail = Mail()

def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        mail.send(msg)

def send_email(recipient, subject, template, **kwargs):
    """
    Send an email to a recipient.
    
    Args:
        recipient: Email address of the recipient
        subject: Subject of the email
        template: HTML template to use for the email
        **kwargs: Additional arguments to pass to the template
        
    Returns:
        True if email sending was successful, False otherwise
    """
    try:
        app = current_app._get_current_object()
        msg = Message(
            subject=subject,
            recipients=[recipient],
            html=template,
            sender=app.config.get('MAIL_DEFAULT_SENDER', 'noreply@ecofinds.com')
        )
        
        # Send email asynchronously
        Thread(target=send_async_email, args=(app, msg)).start()
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {str(e)}")
        return False

def send_welcome_email(user):
    """Send welcome email to a new user."""
    subject = "Welcome to EcoFinds!"
    template = f"""
    <h1>Welcome to EcoFinds, {user.username}!</h1>
    <p>Thank you for joining our community for sustainable second-hand shopping.</p>
    <p>Start exploring items or list your own products today!</p>
    <p>Best regards,<br>The EcoFinds Team</p>
    """
    return send_email(user.email, subject, template)

def send_purchase_confirmation(user, purchase):
    """Send purchase confirmation email."""
    subject = "Your EcoFinds Purchase Confirmation"
    # In a real application, you would use a template with purchase details
    template = f"""
    <h1>Purchase Confirmation</h1>
    <p>Thank you for your purchase, {user.username}!</p>
    <p>Your order has been confirmed and the seller will be notified.</p>
    <p>Best regards,<br>The EcoFinds Team</p>
    """
    return send_email(user.email, subject, template)

# Note: To use this service, you'll need to:
# 1. Add Flask-Mail to your requirements.txt
# 2. Initialize mail in extensions.py
# 3. Add mail configuration to config.py
