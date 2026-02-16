# Event Pass Generator - UML Diagrams

## 1. Entity-Relationship (ER) Diagram

```
┌─────────────────────┐
│       User          │
│  (Django Auth)      │
├─────────────────────┤
│ id (PK)            │
│ username           │
│ email              │
│ password           │
│ is_staff           │
│ is_superuser       │
└─────────────────────┘
         │
         │ creates
         ▼
┌─────────────────────┐
│       Event         │
├─────────────────────┤
│ id (PK, UUID)      │
│ name               │
│ description        │
│ start_date         │
│ end_date           │
│ venue              │
│ max_capacity       │
│ status             │
│ created_at         │
│ updated_at         │
│ created_by (FK)    │───┐
└─────────────────────┘   │
         │                │
         │ has many       │ references
         ▼                │
┌─────────────────────┐   │
│   Registration      │   │
├─────────────────────┤   │
│ id (PK, UUID)      │   │
│ event (FK)         │◄──┘
│ name               │
│ student_id         │
│ email              │
│ qr_code_data       │
│ qr_code_image      │
│ is_valid           │◄─── Single-use validation
│ has_attended       │
│ registered_at      │
│ scanned_at         │
└─────────────────────┘
         │
         │ has many
         ▼
┌─────────────────────┐
│  AttendanceLog      │
├─────────────────────┤
│ id (PK, UUID)      │
│ registration (FK)  │◄── Tracks all scan attempts
│ scan_time          │
│ scan_result        │
│ ip_address         │
└─────────────────────┘
```

## 2. Class Diagram

```
┌────────────────────────────────────────────┐
│              Event                         │
├────────────────────────────────────────────┤
│ - id: UUID                                 │
│ - name: CharField                          │
│ - description: TextField                   │
│ - start_date: DateTimeField               │
│ - end_date: DateTimeField                 │
│ - venue: CharField                         │
│ - max_capacity: IntegerField              │
│ - status: CharField                        │
│ - created_at: DateTimeField               │
│ - updated_at: DateTimeField               │
│ - created_by: ForeignKey(User)            │
├────────────────────────────────────────────┤
│ + __str__(): str                           │
│ + is_active(): bool                        │
│ + registered_count(): int                  │
│ + present_count(): int                     │
│ + absent_count(): int                      │
└────────────────────────────────────────────┘
                  │
                  │ 1:N
                  ▼
┌────────────────────────────────────────────┐
│           Registration                      │
├────────────────────────────────────────────┤
│ - id: UUID                                 │
│ - event: ForeignKey(Event)                │
│ - name: CharField                          │
│ - student_id: CharField                    │
│ - email: EmailField                        │
│ - qr_code_data: TextField                 │
│ - qr_code_image: TextField                │
│ - is_valid: BooleanField                  │
│ - has_attended: BooleanField              │
│ - registered_at: DateTimeField            │
│ - scanned_at: DateTimeField               │
├────────────────────────────────────────────┤
│ + __str__(): str                           │
│ + mark_as_scanned(): bool                  │
└────────────────────────────────────────────┘
                  │
                  │ 1:N
                  ▼
┌────────────────────────────────────────────┐
│          AttendanceLog                      │
├────────────────────────────────────────────┤
│ - id: UUID                                 │
│ - registration: ForeignKey(Registration)  │
│ - scan_time: DateTimeField                │
│ - scan_result: CharField                   │
│ - ip_address: GenericIPAddressField       │
├────────────────────────────────────────────┤
│ + __str__(): str                           │
└────────────────────────────────────────────┘
```

## 3. Sequence Diagram - Registration Process

```
User          Frontend        Backend API        Database        Email Service
 │                │                 │                │                 │
 │   Fill Form    │                 │                │                 │
 ├───────────────>│                 │                │                 │
 │                │                 │                │                 │
 │                │  POST /api/     │                │                 │
 │                │  registrations/ │                │                 │
 │                ├────────────────>│                │                 │
 │                │                 │                │                 │
 │                │                 │  Create        │                 │
 │                │                 │  Registration  │                 │
 │                │                 ├───────────────>│                 │
 │                │                 │                │                 │
 │                │                 │  Generate      │                 │
 │                │                 │  QR Code       │                 │
 │                │                 │<───────────────│                 │
 │                │                 │                │                 │
 │                │                 │  Save QR Data  │                 │
 │                │                 ├───────────────>│                 │
 │                │                 │                │                 │
 │                │                 │                │  Send Email    │
 │                │                 ├────────────────┼────────────────>│
 │                │                 │                │                 │
 │                │  Return QR      │                │                 │
 │                │  Code Image     │                │                 │
 │                │<────────────────│                │                 │
 │                │                 │                │                 │
 │  Display QR    │                 │                │                 │
 │<───────────────│                 │                │                 │
 │                │                 │                │                 │
```

## 4. Sequence Diagram - QR Code Scanning (Single-Use)

```
Scanner      Frontend        Backend API        Database        AttendanceLog
 │              │                 │                │                 │
 │ Scan QR      │                 │                │                 │
 ├─────────────>│                 │                │                 │
 │              │                 │                │                 │
 │              │  POST /api/     │                │                 │
 │              │  registrations/ │                │                 │
 │              │  verify_qr/     │                │                 │
 │              ├────────────────>│                │                 │
 │              │                 │                │                 │
 │              │                 │  Find          │                 │
 │              │                 │  Registration  │                 │
 │              │                 ├───────────────>│                 │
 │              │                 │                │                 │
 │              │                 │  Check         │                 │
 │              │                 │  is_valid      │                 │
 │              │                 │<───────────────│                 │
 │              │                 │                │                 │
 │              │                 │  IF Valid:     │                 │
 │              │                 │  - Set valid=F │                 │
 │              │                 │  - Set attend=T│                 │
 │              │                 │  - Set scan_at │                 │
 │              │                 ├───────────────>│                 │
 │              │                 │                │                 │
 │              │                 │                │  Log Success   │
 │              │                 ├────────────────┼────────────────>│
 │              │                 │                │                 │
 │              │                 │  IF Invalid:   │                 │
 │              │                 │                │  Log Failure   │
 │              │                 ├────────────────┼────────────────>│
 │              │                 │                │                 │
 │              │  Return Result  │                │                 │
 │              │  (valid/invalid)│                │                 │
 │              │<────────────────│                │                 │
 │              │                 │                │                 │
 │  Show Result │                 │                │                 │
 │<─────────────│                 │                │                 │
 │              │                 │                │                 │
```

## 5. Use Case Diagram

```
                    ┌──────────────────────────────┐
                    │   Event Pass Generator       │
                    │        System                │
                    └──────────────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
    ┌────▼────┐            ┌────▼────┐            ┌────▼────┐
    │ Student │            │  Admin  │            │ Scanner │
    └────┬────┘            └────┬────┘            └────┬────┘
         │                      │                      │
         │                      │                      │
    ┌────▼──────────────┐  ┌───▼──────────────┐  ┌───▼──────────────┐
    │ - View Events     │  │ - Create Events  │  │ - Scan QR Code   │
    │ - Register Event  │  │ - Edit Events    │  │ - Validate Pass  │
    │ - Receive QR Pass│  │ - View Dashboard │  │ - Mark Attendance│
    └───────────────────┘  │ - View Statistics│  └──────────────────┘
                           │ - Manage Users   │
                           │ - View Logs      │
                           └──────────────────┘
```

## 6. Activity Diagram - Student Registration

```
        START
          │
          ▼
    ┌─────────────┐
    │ Browse      │
    │ Events      │
    └─────┬───────┘
          │
          ▼
    ┌─────────────┐
    │ Select      │
    │ Event       │
    └─────┬───────┘
          │
          ▼
    ┌─────────────┐
    │ Fill        │
    │ Registration│
    │ Form        │
    └─────┬───────┘
          │
          ▼
    ┌─────────────┐       NO
    │ Already     ├──────────┐
    │ Registered? │          │
    └─────┬───────┘          │
          │ YES              │
          ▼                  │
    ┌─────────────┐          │
    │ Show Error  │          │
    └─────────────┘          │
                             │
                             ▼
                       ┌─────────────┐
                       │ Create      │
                       │ Registration│
                       └─────┬───────┘
                             │
                             ▼
                       ┌─────────────┐
                       │ Generate    │
                       │ QR Code     │
                       └─────┬───────┘
                             │
                             ▼
                       ┌─────────────┐
                       │ Send Email  │
                       │ with QR     │
                       └─────┬───────┘
                             │
                             ▼
                       ┌─────────────┐
                       │ Display     │
                       │ Success     │
                       └─────────────┘
                             │
                             ▼
                           END
```

## 7. State Diagram - QR Code Status

```
        ┌──────────┐
        │  CREATED │
        │ (valid=T)│
        └────┬─────┘
             │
             │ Registration Created
             │
             ▼
        ┌──────────┐
        │  VALID   │
        │ (valid=T)│
        │(attend=F)│
        └────┬─────┘
             │
             │ First Scan
             │
             ▼
        ┌──────────┐
        │  USED    │
        │ (valid=F)│
        │(attend=T)│
        └────┬─────┘
             │
             │ Subsequent Scans
             │
             ▼
        ┌──────────┐
        │ REJECTED │
        │ (invalid)│
        └──────────┘
```

## 8. Component Diagram

```
┌────────────────────────────────────────────────────────┐
│                   Frontend Layer                        │
├────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  Index   │  │Dashboard │  │ Scanner  │            │
│  │   Page   │  │   Page   │  │   Page   │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
└───────┼─────────────┼─────────────┼───────────────────┘
        │             │             │
        │      REST API Calls       │
        ▼             ▼             ▼
┌────────────────────────────────────────────────────────┐
│                  Backend API Layer                      │
├────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │  EventViewSet    │  │ RegistrationView │          │
│  │  - CRUD Events   │  │ - Register       │          │
│  │  - Statistics    │  │ - Verify QR      │          │
│  └────────┬─────────┘  └────────┬─────────┘          │
│           │                     │                      │
│           └──────────┬──────────┘                      │
│                      ▼                                 │
│           ┌─────────────────────┐                     │
│           │   Django Models     │                     │
│           │ - Event             │                     │
│           │ - Registration      │                     │
│           │ - AttendanceLog     │                     │
│           └──────────┬──────────┘                     │
└──────────────────────┼────────────────────────────────┘
                       ▼
┌────────────────────────────────────────────────────────┐
│                Database Layer (SQLite)                  │
├────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐   │
│  │  Events  │  │ Registrations│  │AttendanceLogs │   │
│  │  Table   │  │    Table     │  │    Table      │   │
│  └──────────┘  └──────────────┘  └───────────────┘   │
└────────────────────────────────────────────────────────┘
```

## Key Features Implemented:

### 1. **Single-Use QR Code System**
- `is_valid` flag tracks if QR code has been used
- `mark_as_scanned()` method atomically marks code as used
- All scan attempts logged in `AttendanceLog`

### 2. **Dashboard with Statistics**
- Pie charts showing Present/Absent/Registered
- Real-time statistics per event
- Overall system statistics

### 3. **Admin Authentication**
- Django built-in admin with custom login page
- Role-based access control
- Secure session management

### 4. **Event Management**
- Create, update, delete events
- Track event status (upcoming/ongoing/completed)
- Capacity management

### 5. **Email Integration**
- QR code sent via email
- College logo in template
- Professional formatting

### 6. **Running Events Display**
- Homepage shows active events
- Real-time registration counts
- Easy registration flow

### 7. **Attendance Tracking**
- Real-time scan count
- Detailed attendance logs
- IP address tracking for security
