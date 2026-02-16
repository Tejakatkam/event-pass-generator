"""
Test Email Configuration
Run this to verify your email settings are working
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventpass_backend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    print("=" * 60)
    print("EventPass Pro - Email Configuration Test")
    print("=" * 60)
    print()
    
    # Check if email is configured
    if not settings.EMAIL_HOST_USER or settings.EMAIL_HOST_USER == 'your-email@gmail.com':
        print("❌ Email not configured!")
        print()
        print("Please run: python configure_email.py")
        print("Or manually edit eventpass_backend/settings.py")
        return
    
    print(f"📧 Configured Email: {settings.EMAIL_HOST_USER}")
    print(f"📤 SMTP Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
    print()
    
    recipient = input("Enter test recipient email address: ").strip()
    
    if not recipient:
        recipient = settings.EMAIL_HOST_USER
        print(f"Using sender email as recipient: {recipient}")
    
    print()
    print("📨 Sending test email...")
    
    try:
        send_mail(
            subject='Test Email - EventPass Pro',
            message='This is a test email from EventPass Pro. If you receive this, your email configuration is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        print()
        print("✅ Email sent successfully!")
        print()
        print(f"📬 Check your inbox: {recipient}")
        print("   (Also check spam/junk folder)")
        print()
        print("🎉 Email configuration is working!")
        print()
        print("Next steps:")
        print("1. Start server: python manage.py runserver")
        print("2. Register for an event")
        print("3. Check email for registration confirmation")
        print()
        
    except Exception as e:
        print()
        print("❌ Failed to send email!")
        print()
        print(f"Error: {str(e)}")
        print()
        print("Common issues:")
        print("1. Wrong App Password - Generate a new one")
        print("2. 2-Step Verification not enabled")
        print("3. Internet connection issues")
        print("4. Firewall blocking SMTP port 587")
        print()
        print("📖 Check EMAIL_SETUP_GUIDE.md for troubleshooting")
        print()

if __name__ == '__main__':
    test_email()
