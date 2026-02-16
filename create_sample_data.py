"""
Sample data creation script for Event Pass Generator
Run this after creating a superuser to populate the database with sample data.

Usage:
    python manage.py shell < create_sample_data.py
"""

from django.contrib.auth.models import User
from events.models import Event, Registration
from django.utils import timezone
from datetime import timedelta
import json
import qrcode
import io
import base64
import uuid

print("Creating sample data...")

# Get or create admin user
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@eventpass.com',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print("✓ Admin user created (username: admin, password: admin123)")
else:
    print("✓ Admin user already exists")

# Create sample events
now = timezone.now()

events_data = [
    {
        'name': 'Tech Fest 2025',
        'description': 'Annual technical festival featuring coding competitions, robotics, and tech talks',
        'start_date': now - timedelta(hours=2),
        'end_date': now + timedelta(days=2),
        'venue': 'Main Auditorium',
        'max_capacity': 150,
        'status': 'ongoing'
    },
    {
        'name': 'Cultural Night',
        'description': 'Evening of music, dance, and cultural performances',
        'start_date': now + timedelta(days=3),
        'end_date': now + timedelta(days=3, hours=4),
        'venue': 'Open Air Theater',
        'max_capacity': 200,
        'status': 'upcoming'
    },
    {
        'name': 'Workshop: AI & Machine Learning',
        'description': 'Hands-on workshop on artificial intelligence and machine learning fundamentals',
        'start_date': now - timedelta(days=1),
        'end_date': now + timedelta(hours=3),
        'venue': 'Computer Lab',
        'max_capacity': 50,
        'status': 'ongoing'
    },
    {
        'name': 'Sports Day',
        'description': 'Annual sports competition with cricket, football, and athletics',
        'start_date': now + timedelta(days=7),
        'end_date': now + timedelta(days=7, hours=8),
        'venue': 'Sports Ground',
        'max_capacity': 300,
        'status': 'upcoming'
    },
]

created_events = []
for event_data in events_data:
    event, created = Event.objects.get_or_create(
        name=event_data['name'],
        defaults={**event_data, 'created_by': admin_user}
    )
    created_events.append(event)
    if created:
        print(f"✓ Created event: {event.name}")
    else:
        print(f"- Event already exists: {event.name}")

# Create sample registrations for the ongoing events
ongoing_events = [e for e in created_events if e.status == 'ongoing']

sample_students = [
    {'name': 'Rajesh Kumar', 'student_id': '22CS001', 'email': 'rajesh.kumar@example.com'},
    {'name': 'Priya Sharma', 'student_id': '22CS002', 'email': 'priya.sharma@example.com'},
    {'name': 'Amit Patel', 'student_id': '22CS003', 'email': 'amit.patel@example.com'},
    {'name': 'Sneha Reddy', 'student_id': '22CS004', 'email': 'sneha.reddy@example.com'},
    {'name': 'Vikram Singh', 'student_id': '22CS005', 'email': 'vikram.singh@example.com'},
    {'name': 'Ananya Iyer', 'student_id': '22CS006', 'email': 'ananya.iyer@example.com'},
    {'name': 'Rohan Gupta', 'student_id': '22CS007', 'email': 'rohan.gupta@example.com'},
    {'name': 'Kavya Nair', 'student_id': '22CS008', 'email': 'kavya.nair@example.com'},
    {'name': 'Arjun Verma', 'student_id': '22CS009', 'email': 'arjun.verma@example.com'},
    {'name': 'Divya Menon', 'student_id': '22CS010', 'email': 'divya.menon@example.com'},
]

registration_count = 0
for event in ongoing_events:
    for i, student in enumerate(sample_students):
        # Generate QR code
        qr_uuid = str(uuid.uuid4())
        qr_data_dict = {
            'registration_id': qr_uuid,
            'event_id': str(event.id),
            'name': student['name'],
            'student_id': student['student_id'],
            'email': student['email'],
            'timestamp': timezone.now().isoformat()
        }
        qr_data = json.dumps(qr_data_dict)
        
        # Generate QR code image
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        qr_code_image = f"data:image/png;base64,{img_str}"
        
        # Create registration
        reg, created = Registration.objects.get_or_create(
            event=event,
            email=student['email'],
            defaults={
                'name': student['name'],
                'student_id': student['student_id'],
                'qr_code_data': qr_data,
                'qr_code_image': qr_code_image,
                'is_valid': True,
                'has_attended': (i < 5)  # First 5 students have attended
            }
        )
        
        if created:
            # Mark some as attended
            if i < 5:
                reg.scanned_at = timezone.now() - timedelta(hours=i)
                reg.is_valid = False
                reg.save()
            registration_count += 1

print(f"✓ Created {registration_count} sample registrations")
print(f"✓ Marked first 5 registrations as attended for each ongoing event")

print("\n" + "="*60)
print("Sample data created successfully!")
print("="*60)
print("\nSummary:")
print(f"- Total Events: {len(created_events)}")
print(f"- Ongoing Events: {len(ongoing_events)}")
print(f"- Total Registrations: {registration_count}")
print(f"- Sample Attended: ~{5 * len(ongoing_events)}")
print("\nYou can now:")
print("1. Visit http://127.0.0.1:8000/ to see running events")
print("2. Visit http://127.0.0.1:8000/dashboard/ to see statistics")
print("3. Login to admin panel with: admin / admin123")
print("\nNote: If admin user already exists, password may be different.")
