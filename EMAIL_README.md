# 📧 Email Setup - Quick Start

## Automatic Email Sending is Now Configured! ✅

When users register for events, they will automatically receive a confirmation email with:
- ✅ Event details (name, venue, date, time)
- ✅ QR code for event entry (embedded in email)
- ✅ Registration ID and student information
- ✅ Professional branded email with college logo

---

## 🚀 Quick Setup (2 minutes)

### Step 1: Get Gmail App Password

1. Go to: https://myaccount.google.com/apppasswords
2. (If asked) Enable 2-Step Verification first
3. Generate App Password for "Mail"
4. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### Step 2: Configure Email

**Option A: Use the Setup Script** (Easiest)
```bash
python configure_email.py
```
Follow the prompts and enter your Gmail and App Password.

**Option B: Manual Configuration**

Edit `eventpass_backend/settings.py` around line 150:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your Gmail
EMAIL_HOST_PASSWORD = 'abcd efgh ijkl mnop'  # Your App Password
DEFAULT_FROM_EMAIL = 'EventPass Pro <your-email@gmail.com>'
```

### Step 3: Test Email

```bash
python test_email.py
```

Enter your email to receive a test message.

### Step 4: Done! 🎉

Start the server and test event registration:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ and register for an event.
Check your email inbox!

---

## 📋 What Happens When User Registers?

1. **User fills registration form** on homepage
2. **System generates QR code** with unique ID
3. **Email automatically sent** to user's email address
4. **User receives beautiful HTML email** with:
   - College logo at top
   - Event details in organized table
   - QR code image (250x250px)
   - Instructions for event entry
   - Single-use QR code warning
5. **User can download/print** QR code from website too

---

## 🎨 Email Features

### Professional Design:
- Responsive HTML email template
- College branding with logo
- Color-coded sections
- Mobile-friendly layout

### Embedded Images:
- College logo (from `static/images/cmrtc.png`)
- QR code (generated dynamically)
- Both images embedded inline (no external links)

### Security:
- Single-use QR codes
- Unique registration IDs
- Timestamp verification

---

## 🔧 Troubleshooting

### Email Not Received?
1. Check spam/junk folder
2. Verify email address is correct
3. Run `python test_email.py` to test configuration
4. Check Django terminal for error messages

### "SMTPAuthenticationError"?
- You're using regular password instead of App Password
- Generate App Password at: https://myaccount.google.com/apppasswords

### "Connection refused"?
- Check internet connection
- Firewall might be blocking port 587
- Try disabling antivirus temporarily

### Images Not Showing?
- Make sure `static/images/cmrtc.png` exists
- Check that STATIC_ROOT is configured
- Verify BASE_DIR in settings.py

---

## 📁 Email Template Location

Edit the email design:
```
templates/emails/registration_email.html
```

You can customize:
- Colors and styling
- Content and wording
- Layout and structure
- College information

---

## 🔐 For Production Use

### Use Environment Variables:

1. Create `.env` file:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

2. Install python-dotenv:
```bash
pip install python-dotenv
```

3. Update settings.py:
```python
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

4. Add to .gitignore:
```
.env
```

### Never commit passwords to Git!

---

## 📚 Full Documentation

For detailed setup instructions and advanced configuration:
- **EMAIL_SETUP_GUIDE.md** - Complete guide with screenshots
- **configure_email.py** - Interactive setup script
- **test_email.py** - Email testing utility

---

## ✅ Verification Checklist

After setup, verify:
- [ ] App Password generated from Gmail
- [ ] EMAIL_HOST_USER configured in settings.py
- [ ] EMAIL_HOST_PASSWORD configured in settings.py
- [ ] Test email sent successfully (`python test_email.py`)
- [ ] Event registration sends email
- [ ] Email received in inbox (check spam too)
- [ ] QR code visible in email
- [ ] College logo visible in email
- [ ] Download QR button works on website
- [ ] Print button works on website

---

## 🎯 Current Status

✅ Email functionality implemented  
✅ HTML email template created  
✅ QR code embedded in email  
✅ College logo attached  
✅ Automatic sending on registration  
✅ Error handling implemented  
✅ Success/failure feedback to user  

**Ready to use!** Just configure your Gmail credentials.

---

## 🚀 Quick Commands

```bash
# Configure email settings
python configure_email.py

# Test email configuration
python test_email.py

# Start development server
python manage.py runserver

# Access the application
http://127.0.0.1:8000/
```

---

*Need help? Check EMAIL_SETUP_GUIDE.md for detailed instructions!*
