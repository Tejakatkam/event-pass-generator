# 🚀 Quick Start Guide - Event Pass Generator

## ⚡ 5-Minute Setup

### Step 1: Create Admin User (REQUIRED)
```bash
python manage.py createsuperuser
```
When prompted, enter:
- **Username**: `admin`
- **Email**: `admin@eventpass.com`
- **Password**: Choose a secure password (e.g., `admin123`)

### Step 2: Start Server
```bash
python manage.py runserver
```

### Step 3: Access the Application
Open your browser and visit:
- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Dashboard**: http://127.0.0.1:8000/dashboard/

---

## 📝 First Time Usage

### Create Your First Event (Admin)

1. **Login to Admin**
   - Go to: http://127.0.0.1:8000/admin/
   - Username: `admin`
   - Password: (the one you created)

2. **Add Event**
   - Click on "**Events**" under EVENTS section
   - Click "**ADD EVENT**" button (top right)
   - Fill in the form:
     ```
     Name: Tech Fest 2025
     Description: Annual technical festival
     Start date: [Choose a date/time]
     End date: [Choose a date/time after start]
     Venue: Main Auditorium
     Max capacity: 100
     Status: ongoing
     Created by: admin (your username)
     ```
   - Click "**SAVE**"

3. **View Your Event**
   - Go to homepage: http://127.0.0.1:8000/
   - You should see your event in the "Running Events" section!

---

## 🎟️ Register for Event (Student View)

1. **Go to Homepage**
   - Visit: http://127.0.0.1:8000/

2. **Fill Registration Form**
   - Select the event from dropdown
   - Enter your details:
     ```
     Name: John Doe
     Student ID: 22CS001
     Email: john@example.com
     ```

3. **Get QR Code**
   - Click "Generate Gate Pass"
   - Your QR code will appear instantly!
   - (Note: Email sending requires SMTP configuration)

---

## 📊 View Dashboard

1. **Access Dashboard**
   - Go to: http://127.0.0.1:8000/dashboard/
   - (You may need to login first at `/admin-login/`)

2. **See Statistics**
   - Total Events: Shows count of all events
   - Total Registrations: All registered participants
   - Present: Participants who have been scanned in
   - Absent: Registered but not attended
   - **Pie Chart**: Visual representation of attendance

---

## 📱 Scan QR Codes

1. **Go to Scanner Page**
   - Visit: http://127.0.0.1:8000/scan/

2. **Allow Camera Access**
   - Browser will ask for camera permission
   - Click "Allow"

3. **Scan QR Code**
   - Point camera at QR code
   - System automatically validates
   - Shows participant info if valid
   - Shows "Already Used" if scanned before

4. **Alternative: Upload QR Image**
   - If camera doesn't work
   - Use the file upload option
   - Select QR code image from your device

---

## 🎯 Key URLs to Remember

| Page | URL | Purpose |
|------|-----|---------|
| **Home** | http://127.0.0.1:8000/ | Register for events |
| **Admin** | http://127.0.0.1:8000/admin/ | Manage everything |
| **Dashboard** | http://127.0.0.1:8000/dashboard/ | View statistics |
| **Scanner** | http://127.0.0.1:8000/scan/ | Scan QR codes |
| **Admin Login** | http://127.0.0.1:8000/admin-login/ | Admin auth page |

---

## 🧪 Test the Single-Use Feature

1. **Register for an event** (creates a QR code)
2. **Go to scanner page**
3. **Scan the QR code** → Should show "✅ Attendance marked successfully"
4. **Scan the same QR code again** → Should show "❌ QR code already used"

**This proves the single-use feature is working!**

---

## 📈 Check Statistics

After scanning QR codes:
1. Go to **Dashboard**: http://127.0.0.1:8000/dashboard/
2. Numbers update automatically:
   - **Present**: Increases when QR is scanned
   - **Absent**: Registered but not scanned
   - **Pie Chart**: Visual breakdown

---

## 🔧 Common Commands

```bash
# Start server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Run migrations (if you change models)
python manage.py makemigrations
python manage.py migrate

# Reset database (careful - deletes all data!)
# Delete db.sqlite3 file, then:
python manage.py migrate
python manage.py createsuperuser
```

---

## ✅ Checklist - Is Everything Working?

- [ ] Server starts without errors
- [ ] Can access homepage (http://127.0.0.1:8000/)
- [ ] Can login to admin panel
- [ ] Created at least one event
- [ ] Event appears on homepage
- [ ] Can register for event
- [ ] QR code generates successfully
- [ ] Can access dashboard
- [ ] Scanner page opens
- [ ] Camera works (or file upload)
- [ ] QR code scans successfully
- [ ] Second scan shows "already used"
- [ ] Dashboard shows updated statistics

---

## 🐛 Quick Troubleshooting

### Problem: Can't login to admin
**Solution**: Make sure you created a superuser:
```bash
python manage.py createsuperuser
```

### Problem: No events showing on homepage
**Solution**: 
1. Login to admin panel
2. Create an event with status "ongoing"
3. Make sure start_date is before current time

### Problem: QR scanner not working
**Solution**:
- Use Chrome/Firefox (best compatibility)
- Allow camera permissions
- Use file upload as alternative

### Problem: Can't access dashboard
**Solution**: Login first at `/admin-login/` or `/admin/`

---

## 🎓 Next Steps

1. **Explore Admin Panel**
   - Check "Registrations" to see all sign-ups
   - View "Attendance Logs" to see all scan attempts

2. **Create More Events**
   - Try different event types
   - Set capacity limits
   - Use different venues

3. **Test All Features**
   - Register multiple participants
   - Scan different QR codes
   - Watch statistics update

4. **Customize**
   - Replace college logo in `static/images/`
   - Modify colors in `static/css/style.css`
   - Add your college name

---

## 📞 Need Help?

- Check **README.md** for detailed documentation
- See **UML_DIAGRAMS.md** for system architecture
- Review Django errors in terminal
- Check browser console (F12) for JavaScript errors

---

**🎉 You're all set! Start managing events like a pro!**
