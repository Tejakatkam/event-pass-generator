from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email.mime.image import MIMEImage
import os
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import qrcode
import io
import base64
import json
import uuid
from .models import Event, Registration, AttendanceLog
from .serializers import (
    EventSerializer, RegistrationSerializer, RegistrationCreateSerializer,
    AttendanceLogSerializer, EventStatisticsSerializer
)
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from io import BytesIO

from django.contrib.auth.models import User
from .models import Event, Registration

from django.contrib.auth.decorators import login_required

@login_required
def download_event_registrations_pdf(request, event_id):
    event = Event.objects.get(id=event_id)
    registrations = event.registrations.all()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Event: {event.name}", styles['Title']))
    elements.append(Spacer(1, 0.3 * inch))

    data = [["Name", "Student ID", "Email", "Registered At", "Attended"]]

    for reg in registrations:
        data.append([
            reg.name,
            reg.student_id,
            reg.email,
            reg.registered_at.strftime("%d-%m-%Y %H:%M"),
            "Yes" if reg.has_attended else "No"
        ])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return HttpResponse(
        buffer,
        content_type='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename="{event.name}_registrations.pdf"'
        }
    )


def download_admin_report_pdf(request):
    buffer = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admin_report.pdf"'

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Admin & Events Report", styles['Title']))
    elements.append(Spacer(1, 0.5 * inch))

    admins = User.objects.filter(is_staff=True)

    data = [["Admin Username", "Admin Email", "Created Events"]]

    for admin in admins:
        events = Event.objects.filter(created_by=admin)
        event_names = ", ".join([event.name for event in events])
        data.append([admin.username, admin.email, event_names or "No Events"])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(table)
    doc.build(elements)

    response.write(buffer.getvalue())
    buffer.close()
    return response

@login_required
def download_event_registrations_pdf(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = event.registrations.all()

    buffer = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{event.name}_registrations.pdf"'

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # =========================
    # 🔷 COLLEGE HEADER
    # =========================

    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'cmrtc.png')

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=1.2*inch, height=1.2*inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)

    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(
        "<b>CMR TECHNICAL CAMPUS</b>",
        styles['Heading1']
    ))

    elements.append(Paragraph(
        "Autonomous | ESTD: 2009 | Hyderabad",
        styles['Normal']
    ))

    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(
        f"<b>Event Registration Report</b>",
        styles['Heading2']
    ))

    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(
        f"Event Name: <b>{event.name}</b>",
        styles['Normal']
    ))

    elements.append(Spacer(1, 0.5 * inch))

    # =========================
    # 🔷 TABLE SECTION
    # =========================

    data = [
        ["S.No", "Student ID", "Student Name", "Student Email", "Register ID"]
    ]

    for index, reg in enumerate(registrations, start=1):
        data.append([
            index,
            reg.student_id,
            reg.name,
            reg.email,
            str(reg.id)[:8].upper()
        ])

    table = Table(data, repeatRows=1, colWidths=[0.7*inch, 1.2*inch, 1.5*inch, 2*inch, 1.2*inch])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))

    elements.append(table)

    # =========================
    # 🔷 SIGNATURE SECTION
    # =========================

    elements.append(Spacer(1, 1 * inch))

    signature_data = [
        ["", ""],
        ["Coordinator Signature", "HoD Signature"]
    ]

    signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])

    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('LINEABOVE', (0, 1), (0, 1), 1, colors.black),
        ('LINEABOVE', (1, 1), (1, 1), 1, colors.black),
    ]))

    elements.append(signature_table)

    doc.build(elements)

    response.write(buffer.getvalue())
    buffer.close()

    return response



def send_registration_email(registration, qr_code_image_base64):
    """Send registration confirmation email with QR code"""
    try:
        event = registration.event
        
        # Prepare email context
        context = {
            'name': registration.name,
            'event_name': event.name,
            'event_venue': event.venue,
            'event_date': event.start_date.strftime('%B %d, %Y at %I:%M %p'),
            'student_id': registration.student_id,
            'registration_id': str(registration.id)[:8].upper(),
        }
        
        # Render HTML email
        html_content = render_to_string('emails/registration_email.html', context)
        
        # Create email message
        subject = f'Event Registration Confirmation - {event.name}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [registration.email]
        
        # Create message
        msg = EmailMultiAlternatives(subject, '', from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        
        # Attach college logo
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'cmrtc.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                logo_img = MIMEImage(f.read())
                logo_img.add_header('Content-ID', '<college_logo>')
                logo_img.add_header('Content-Disposition', 'inline', filename='logo.png')
                msg.attach(logo_img)
        
        # Attach QR code
        # Convert base64 to bytes
        qr_code_data = qr_code_image_base64.split(',')[1]  # Remove data:image/png;base64, prefix
        qr_code_bytes = base64.b64decode(qr_code_data)
        qr_img = MIMEImage(qr_code_bytes)
        qr_img.add_header('Content-ID', '<qr_code>')
        qr_img.add_header('Content-Disposition', 'inline', filename='qr_code.png')
        msg.attach(qr_img)
        
        # Send email
        msg.send()
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for managing events"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def active_events(self, request):
        """Get all currently active/ongoing events"""
        now = timezone.now()
        active = Event.objects.filter(
            start_date__lte=now,
            end_date__gte=now,
            status='ongoing'
        )
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get statistics for a specific event"""
        event = self.get_object()
        data = {
            'event_name': event.name,
            'registered': event.registered_count,
            'present': event.present_count,
            'absent': event.absent_count,
            'attendance_rate': (event.present_count / event.registered_count * 100) if event.registered_count > 0 else 0
        }
        return Response(data)


class RegistrationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing registrations"""
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RegistrationCreateSerializer
        return RegistrationSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        """Create a new registration and generate QR code"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Generate unique QR code data
        qr_uuid = str(uuid.uuid4())
        qr_data_dict = {
            'registration_id': qr_uuid,
            'event_id': str(serializer.validated_data['event'].id),
            'name': serializer.validated_data['name'],
            'student_id': serializer.validated_data['student_id'],
            'email': serializer.validated_data['email'],
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
        
        # Save registration
        registration = serializer.save(
            qr_code_data=qr_data,
            qr_code_image=qr_code_image
        )
        
        # Send confirmation email
        email_sent = send_registration_email(registration, qr_code_image)
        
        # Return registration data with QR code
        response_serializer = RegistrationSerializer(registration)
        return Response({
            **response_serializer.data,
            'qr_code_image': qr_code_image,
            'email_sent': email_sent
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def verify_qr(self, request):
        """Verify and mark QR code as scanned"""
        qr_data = request.data.get('qr_data')
        if not qr_data:
            return Response({'error': 'QR data is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Parse QR data
            qr_dict = json.loads(qr_data)
            
            # Find registration by QR code data
            registration = Registration.objects.filter(qr_code_data=qr_data).first()
            
            if not registration:
                return Response({
                    'valid': False,
                    'message': 'Invalid QR code',
                    'scan_result': 'invalid'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Get client IP
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or \
                        request.META.get('REMOTE_ADDR')
            
            # Check if already scanned
            if not registration.is_valid:
                # Log failed attempt
                AttendanceLog.objects.create(
                    registration=registration,
                    scan_result='already_used',
                    ip_address=ip_address
                )
                return Response({
                    'valid': False,
                    'message': 'QR code already used',
                    'scan_result': 'already_used',
                    'registration': RegistrationSerializer(registration).data
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Mark as scanned
            registration.mark_as_scanned()
            
            # Log successful scan
            AttendanceLog.objects.create(
                registration=registration,
                scan_result='success',
                ip_address=ip_address
            )
            
            return Response({
                'valid': True,
                'message': 'Attendance marked successfully',
                'scan_result': 'success',
                'registration': RegistrationSerializer(registration).data
            }, status=status.HTTP_200_OK)
            
        except json.JSONDecodeError:
            return Response({
                'valid': False,
                'message': 'Invalid QR code format',
                'scan_result': 'invalid'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required
def dashboard_statistics(request):
    """Get overall dashboard statistics"""
    total_events = Event.objects.count()
    now = timezone.now()
    active_events = Event.objects.filter(
        start_date__lte=now,
        end_date__gte=now,
        status='ongoing'
    ).count()
    
    total_registrations = Registration.objects.count()
    total_present = Registration.objects.filter(has_attended=True).count()
    total_absent = total_registrations - total_present
    attendance_rate = (total_present / total_registrations * 100) if total_registrations > 0 else 0
    
    data = {
        'total_events': total_events,
        'active_events': active_events,
        'total_registrations': total_registrations,
        'total_present': total_present,
        'total_absent': total_absent,
        'attendance_rate': round(attendance_rate, 2)
    }
    
    serializer = EventStatisticsSerializer(data)
    return Response(serializer.data)


@api_view(['POST'])
def admin_login_view(request):
    """Admin login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None and user.is_staff:
        login(request, user)
        return Response({
            'success': True,
            'message': 'Login successful',
            'user': {
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff
            }
        })
    else:
        return Response({
            'success': False,
            'message': 'Invalid credentials or insufficient permissions'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@login_required
def admin_logout_view(request):
    """Admin logout endpoint"""
    logout(request)
    return Response({
        'success': True,
        'message': 'Logout successful'
    })


# Template views
def index_view(request):
    """Home page view"""
    return render(request, 'index.html')


def events_view(request):
    """All events page view"""
    return render(request, 'events.html')


def scan_view(request):
    """QR scan page view"""
    return render(request, 'scan.html')


@login_required
def dashboard_view(request):
    """Admin dashboard view"""
    return render(request, 'dashboard.html')


def admin_login_page(request):
    """Admin login page"""
    # Handle POST request for login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin-panel')
        else:
            context = {'error': 'Invalid credentials or you do not have admin permissions'}
            return render(request, 'admin_login.html', context)
    
    # If already logged in, redirect to admin panel
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin-panel')
    
    return render(request, 'admin_login.html')


def admin_register_page(request):
    """Admin registration page"""
    # Handle POST request for registration
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if password1 != password2:
            context = {'error': 'Passwords do not match'}
            return render(request, 'admin_register.html', context)
        
        # Check if username already exists
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            context = {'error': 'Username already exists'}
            return render(request, 'admin_register.html', context)
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            context = {'error': 'Email already exists'}
            return render(request, 'admin_register.html', context)
        
        # Create user with staff permissions
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.is_staff = True
        user.save()
        
        context = {'success': 'Admin account created successfully! You can now login.'}
        return render(request, 'admin_register.html', context)
    
    # If already logged in, redirect to admin panel
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin-panel')
    
    return render(request, 'admin_register.html')


@login_required
def admin_panel_view(request):
    """Custom admin panel home"""
    if not request.user.is_staff:
        return redirect('admin-login-page')
    
    # Get summary statistics
    total_events = Event.objects.count()
    total_registrations = Registration.objects.count()
    total_present = Registration.objects.filter(has_attended=True).count()
    recent_events = Event.objects.all()[:5]
    
    context = {
        'total_events': total_events,
        'total_registrations': total_registrations,
        'total_present': total_present,
        'recent_events': recent_events,
    }
    return render(request, 'admin_panel.html', context)


@login_required
def admin_events_view(request):
    """List all events in custom admin"""
    if not request.user.is_staff:
        return redirect('admin-login-page')
    
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'admin_events.html', context)


@login_required
def admin_create_event(request):
    """Create new event"""
    if not request.user.is_staff:
        return redirect('admin-login-page')
    
    if request.method == 'POST':
        try:
            event = Event.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                venue=request.POST.get('venue'),
                max_capacity=request.POST.get('max_capacity'),
                status=request.POST.get('status'),
                created_by=request.user
            )
            return redirect('admin-events')
        except Exception as e:
            context = {'error': str(e)}
            return render(request, 'admin_create_event.html', context)
    
    return render(request, 'admin_create_event.html')


@login_required
def admin_edit_event(request, event_id):
    """Edit existing event"""
    if not request.user.is_staff:
        return redirect('admin-login-page')
    
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        try:
            event.name = request.POST.get('name')
            event.description = request.POST.get('description')
            event.start_date = request.POST.get('start_date')
            event.end_date = request.POST.get('end_date')
            event.venue = request.POST.get('venue')
            event.max_capacity = request.POST.get('max_capacity')
            event.status = request.POST.get('status')
            event.save()
            return redirect('admin-events')
        except Exception as e:
            context = {'event': event, 'error': str(e)}
            return render(request, 'admin_edit_event.html', context)
    
    context = {'event': event}
    return render(request, 'admin_edit_event.html', context)


@login_required
def admin_delete_event(request, event_id):
    """Delete event"""
    if not request.user.is_staff:
        return redirect('admin-login-page')
    
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event.delete()
        return redirect('admin-events')
    
    context = {'event': event}
    return render(request, 'admin_delete_event.html', context)


@login_required
def admin_registrations_view(request):
    """View all registrations"""
    if not request.user.is_staff:
        return redirect('admin-login-page')
    
    registrations = Registration.objects.select_related('event').all()
    context = {'registrations': registrations}
    return render(request, 'admin_registrations.html', context)


@login_required
def admin_logs_view(request):
    """View attendance logs"""
    if not request.user.is_staff:
        return redirect('admin-login-page')
    
    logs = AttendanceLog.objects.select_related('registration', 'registration__event').all()[:100]
    context = {'logs': logs}
    return render(request, 'admin_logs.html', context)
