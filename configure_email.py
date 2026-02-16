"""
Quick Email Configuration Script
Run this to configure email settings for EventPass Pro
"""

import os
import re

def configure_email():
    print("=" * 60)
    print("EventPass Pro - Email Configuration Setup")
    print("=" * 60)
    print()
    
    print("📧 This script will help you configure email settings.")
    print()
    print("⚠️  IMPORTANT: You need a Gmail App Password!")
    print("   If you don't have one, follow these steps:")
    print("   1. Enable 2-Step Verification on your Gmail account")
    print("   2. Go to: https://myaccount.google.com/apppasswords")
    print("   3. Generate an App Password for 'Mail'")
    print()
    
    # Get email configuration
    email = input("Enter your Gmail address: ").strip()
    
    # Validate email
    if not re.match(r'^[\w\.-]+@gmail\.com$', email):
        print("❌ Invalid Gmail address. Please use a Gmail account.")
        return
    
    print()
    print("🔑 Now enter your Gmail App Password (16 characters)")
    print("   Format: xxxx xxxx xxxx xxxx")
    password = input("Enter App Password: ").strip()
    
    if len(password.replace(' ', '')) != 16:
        print("⚠️  Warning: App Password should be 16 characters.")
        print("   It might still work, but double-check if emails fail.")
    
    # Read settings.py
    settings_path = os.path.join(os.path.dirname(__file__), 'eventpass_backend', 'settings.py')
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update email settings
        content = re.sub(
            r"EMAIL_HOST_USER = '[^']*'",
            f"EMAIL_HOST_USER = '{email}'",
            content
        )
        content = re.sub(
            r'EMAIL_HOST_PASSWORD = \'[^\']*\'',
            f"EMAIL_HOST_PASSWORD = '{password}'",
            content
        )
        content = re.sub(
            r"DEFAULT_FROM_EMAIL = '[^']*'",
            f"DEFAULT_FROM_EMAIL = 'EventPass Pro <{email}>'",
            content
        )
        
        # Write back
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print()
        print("✅ Email configuration updated successfully!")
        print()
        print("📝 Configuration saved:")
        print(f"   Email: {email}")
        print(f"   From: EventPass Pro <{email}>")
        print()
        print("🧪 To test the configuration, run:")
        print("   python test_email.py")
        print()
        print("🚀 Start the server and register for an event to test!")
        print()
        
    except FileNotFoundError:
        print("❌ Error: settings.py not found!")
        print("   Make sure you're running this from the project root directory.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    configure_email()
