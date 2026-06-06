# CarePoint Clinic

> **Live URL:** https://your-app-name.onrender.com

A fully functional clinic management web application built with Django. Patients can register, browse doctors and services, and book appointments. Staff can manage doctor profiles through the site.

---

## Features

- Browse doctors filtered by specialisation
- View detailed doctor profiles
- Book, edit, and cancel appointments (authenticated users)
- Staff-only doctor management (Create, Edit, Delete)
- Full REST API for doctors, services, and appointments
- Token + session authentication
- Responsive design across all pages

---

## Tech Stack

- **Backend:** Django 4.2, Django REST Framework
- **Database:** PostgreSQL (production), SQLite (local dev)
- **Static files:** WhiteNoise
- **Deployment:** Render
- **Image handling:** Pillow

---

## Local Setup

### Prerequisites
- Python 3.11+
- pip

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/dune-cohort-final-project.git
cd dune-cohort-final-project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and fill in your values

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Start dev server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Environment Variables

| Variable       | Description                        |
|----------------|------------------------------------|
| `SECRET_KEY`   | Django secret key                  |
| `DEBUG`        | `True` for local, `False` for prod |
| `DATABASE_URL` | PostgreSQL connection string       |
| `ALLOWED_HOSTS`| Comma-separated allowed hostnames  |

---

## Apps

| App            | Responsibility                                |
|----------------|-----------------------------------------------|
| `clinic`       | Doctors, services, homepage, user auth, API   |
| `appointments` | Appointment booking, editing, and cancellation|

---

## Models

| Model           | App          | Key Relations                          |
|-----------------|--------------|----------------------------------------|
| `Specialisation`| clinic       | —                                      |
| `Doctor`        | clinic       | ForeignKey → Specialisation            |
| `Service`       | clinic       | —                                      |
| `Appointment`   | appointments | ForeignKey → User (CASCADE), Doctor, Service |

---

## API Endpoints

See [`api_docs.md`](./api_docs.md) for full documentation.

| Method | Endpoint                    | Auth | Description             |
|--------|-----------------------------|------|-------------------------|
| GET    | `/api/doctors/`             | No   | List doctors            |
| GET    | `/api/doctors/<id>/`        | No   | Doctor detail           |
| GET    | `/api/services/`            | No   | List services           |
| GET    | `/api/appointments/`        | ✅   | My appointments         |
| POST   | `/api/appointments/`        | ✅   | Book appointment        |
| DELETE | `/api/appointments/<id>/`   | ✅   | Cancel appointment      |

---

## Deployment (Render)

1. Push repo to GitHub
2. Create new Web Service on [render.com](https://render.com)
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
5. Set start command: `gunicorn config.wsgi:application`
6. Add environment variables: `SECRET_KEY`, `DEBUG=False`, `DATABASE_URL`, `ALLOWED_HOSTS`
7. Add a PostgreSQL database and copy the internal URL to `DATABASE_URL`

---

## Screenshots

*(Add screenshots of your live site here)*

---

## Git Commit History

This project was built incrementally with meaningful commits:

1. `init: project structure and Django config`
2. `feat: clinic app with Doctor and Service models`
3. `feat: appointments app with Appointment model`
4. `feat: full CRUD views for doctor management`
5. `feat: appointment booking, edit, and cancel views`
6. `feat: REST API endpoints with DRF`
7. `feat: authentication — register, login, logout`
8. `style: custom CSS stylesheet and base template`
9. `config: WhiteNoise static files and production settings`
10. `deploy: Procfile and Render configuration`

---

## Author

Built by [Your Name] for the Dune Cohort Backend Development Capstone.
