# Email Configuration Guide

## Setting Up Gmail SMTP for Event Pass Generator

To enable automatic email sending when users register for events, you need to configure Gmail SMTP in your Django settings.

---

## 📧 Step 1: Create Gmail App Password

### Why App Password?
Gmail requires an "App Password" for third-party applications to send emails securely (regular password won't work).

### Steps to Generate App Password:

1. **Go to Google Account Settings**
   - Visit: https://myaccount.google.com/
   - Sign in with your Gmail account

2. **Enable 2-Step Verification** (Required)
   - Go to: Security → 2-Step Verification
   - Click "Get Started" and follow the steps
   - This is mandatory for App Passwords

3. **Generate App Password**
   - Go to: Security → 2-Step Verification → App passwords
   - Or direct link: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Windows Computer" or "Other (Custom name)"
   - Name it: "EventPass Pro"
   - Click "Generate"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)
   - **Save it securely** - you won't see it again!

---

## ⚙️ Step 2: Configure Django Settings

### Edit `settings.py`:

Open: `eventpass_backend/settings.py`

Find the email configuration section (around line 150) and update:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # ← Replace with YOUR Gmail
EMAIL_HOST_PASSWORD = 'abcd efgh ijkl mnop'  # ← Replace with YOUR App Password
DEFAULT_FROM_EMAIL = 'EventPass Pro <your-email@gmail.com>'  # ← Replace
EMAIL_TIMEOUT = 30
```

### Example Configuration:
```python
EMAIL_HOST_USER = 'college.events@gmail.com'
EMAIL_HOST_PASSWORD = 'xyzw abcd 1234 5678'
DEFAULT_FROM_EMAIL = 'EventPass Pro <college.events@gmail.com>'
```

---

## 🧪 Step 3: Test Email Configuration

### Option A: Using Django Shell

```bash
python manage.py shell
```

Then run:
```python
from django.core.mail import send_mail

send_mail(
    'Test Email - EventPass Pro',
    'This is a test email from EventPass Pro.',
    'your-email@gmail.com',  # From
    ['recipient@gmail.com'],  # To
    fail_silently=False,
)
```

If successful, you'll see no errors and receive the email!

### Option B: Using Console Backend (Testing)

For testing without actually sending emails, use console backend:

```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This will print emails to the console instead of sending them.

---

## 🎯 Step 4: Test Event Registration

1. **Start Django Server**:
   ```bash
   python manage.py runserver
   ```

2. **Register for an Event**:
   - Visit: http://127.0.0.1:8000/
   - Fill in registration form with YOUR email
   - Submit registration

3. **Check Your Email**:
   - Look in your inbox (and spam folder)
   - You should receive:
     - Subject: "Event Registration Confirmation - [Event Name]"
     - Beautiful HTML email with college logo
     - QR code embedded in the email
     - Event details

---

## 🔧 Troubleshooting

### Problem: "SMTPAuthenticationError"
**Solution**: 
- Make sure you're using App Password, not regular password
- Verify 2-Step Verification is enabled
- Check that EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct

### Problem: "SMTPServerDisconnected"
**Solution**:
- Check your internet connection
- Verify EMAIL_PORT is 587
- Ensure EMAIL_USE_TLS is True

### Problem: Email not received
**Solution**:
- Check spam/junk folder
- Verify recipient email is correct
- Test with a different email address
- Check Gmail's "Sent" folder

### Problem: "gmail.com refused connection"
**Solution**:
- Check if your firewall is blocking port 587
- Try port 465 with EMAIL_USE_SSL = True instead of TLS

### Problem: Email sent but no images
**Solution**:
- Make sure college logo exists at: `static/images/cmrtc.png`
- Check that STATIC_ROOT is configured correctly
- Verify BASE_DIR path in settings.py

---

## 🔐 Security Best Practices

### For Production:

1. **Use Environment Variables** (Recommended):

Create `.env` file:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

In `settings.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

Install python-dotenv:
```bash
pip install python-dotenv
```

2. **Never commit passwords to Git**:
Add to `.gitignore`:
```
.env
*.pyc
__pycache__/
db.sqlite3
```

3. **Use different email for production**:
- Don't use personal Gmail
- Create dedicated account like `eventpass@yourdomain.com`

---

## 📨 Email Template Customization

### Edit Email Template:
File: `templates/emails/registration_email.html`

You can customize:
- Colors and styling
- College name and branding
- Email content and instructions
- Footer information

### Variables Available:
- `{{ name }}` - Student name
- `{{ event_name }}` - Event name
- `{{ event_venue }}` - Event venue
- `{{ event_date }}` - Event date and time
- `{{ student_id }}` - Student ID
- `{{ registration_id }}` - Registration ID

---

## 🚀 Alternative Email Services

### Using Other Email Providers:

#### **Outlook/Hotmail**:
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

#### **Yahoo Mail**:
```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@yahoo.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

#### **SendGrid** (Professional):
```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

#### **Mailgun** (Professional):
```python
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'postmaster@yourdomain.com'
EMAIL_HOST_PASSWORD = 'your-mailgun-password'
```

---

## ✅ Quick Start Checklist

- [ ] Enable 2-Step Verification on Gmail
- [ ] Generate App Password
- [ ] Update EMAIL_HOST_USER in settings.py
- [ ] Update EMAIL_HOST_PASSWORD in settings.py
- [ ] Update DEFAULT_FROM_EMAIL in settings.py
- [ ] Test email sending from Django shell
- [ ] Register for test event
- [ ] Check email inbox (and spam)
- [ ] Verify QR code and logo display correctly
- [ ] Save App Password securely for future reference

---

## 📞 Support

If you encounter issues:
1. Check Django logs in terminal
2. Review error messages carefully
3. Test with console backend first
4. Verify Gmail account settings
5. Check firewall/antivirus settings

---

## 🎉 Success!

Once configured, users will automatically receive:
- ✅ Confirmation email immediately after registration
- ✅ QR code embedded in email
- ✅ Event details and instructions
- ✅ Professional branded email with college logo

**No manual email sending required!** 🚀

---

*Last Updated: October 28, 2025*
