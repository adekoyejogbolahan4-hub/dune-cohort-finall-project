# CarePoint Clinic — API Documentation

Base URL: `https://your-app.onrender.com/api/`

All endpoints return JSON. Authentication uses **Token Authentication** or **Session Authentication**.

---

## Authentication

For protected endpoints, include in request headers:
```
Authorization: Token <your_token_here>
```

Get a token by logging in via the browser session or using the Django admin to create one.

---

## Endpoints

### 1. List Doctors
**GET** `/api/doctors/`

Returns all available doctors.

**Auth required:** No

**Response 200:**
```json
[
  {
    "id": 1,
    "first_name": "Amaka",
    "last_name": "Okafor",
    "specialisation": 2,
    "specialisation_name": "Cardiology",
    "email": "amaka@carepoint.ng",
    "phone": "+234 801 234 5678",
    "bio": "Board-certified cardiologist with 12 years experience.",
    "is_available": true,
    "years_experience": 12
  }
]
```

---

### 2. Doctor Detail
**GET** `/api/doctors/<id>/`

Returns a single doctor by ID.

**Auth required:** No

**Response 200:** Single doctor object (same shape as above)

**Response 404:**
```json
{"detail": "Not found."}
```

---

### 3. List Services
**GET** `/api/services/`

Returns all active services.

**Auth required:** No

**Response 200:**
```json
[
  {
    "id": 1,
    "name": "General Consultation",
    "description": "Initial assessment with a general practitioner.",
    "price": "5000.00",
    "duration_minutes": 30,
    "is_active": true
  }
]
```

---

### 4. List My Appointments
**GET** `/api/appointments/`

Returns all appointments for the authenticated user.

**Auth required:** ✅ Yes

**Response 200:**
```json
[
  {
    "id": 3,
    "patient": 1,
    "patient_username": "john_doe",
    "doctor": 2,
    "doctor_name": "Dr. Amaka Okafor",
    "service": 1,
    "service_name": "General Consultation",
    "appointment_date": "2025-08-15",
    "appointment_time": "10:00:00",
    "status": "pending",
    "notes": "Feeling chest pains occasionally.",
    "created_at": "2025-07-01T09:42:00Z"
  }
]
```

**Response 401 (unauthenticated):**
```json
{"detail": "Authentication credentials were not provided."}
```

---

### 5. Book Appointment
**POST** `/api/appointments/`

Books a new appointment for the authenticated user.

**Auth required:** ✅ Yes

**Request Body:**
```json
{
  "doctor": 2,
  "service": 1,
  "appointment_date": "2025-08-15",
  "appointment_time": "10:00:00",
  "notes": "Routine check-up."
}
```

**Response 201:** Created appointment object

**Response 400:**
```json
{
  "appointment_date": ["This field is required."]
}
```

---

### 6. Cancel Appointment
**DELETE** `/api/appointments/<id>/`

Cancels (deletes) an appointment belonging to the authenticated user.

**Auth required:** ✅ Yes

**Response 204:** No content

**Response 404:**
```json
{"detail": "Not found."}
```

---

## HTTP Status Codes Used

| Code | Meaning |
|------|---------|
| 200  | OK — successful GET |
| 201  | Created — successful POST |
| 204  | No Content — successful DELETE |
| 400  | Bad Request — validation errors |
| 401  | Unauthorized — missing/invalid credentials |
| 403  | Forbidden — authenticated but not permitted |
| 404  | Not Found — resource doesn't exist |
