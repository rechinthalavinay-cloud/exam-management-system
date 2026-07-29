# Examination Module

A full-stack **Examination Management System** built for the Robokalam Technologies Full Stack Web Development Intern assignment. It manages students, exams, and results with REST APIs, JWT authentication, and a responsive web UI.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript (Fetch API) |
| Database | MySQL |
| Authentication | JWT (API) + Session (Web UI) |
| Password Hashing | Werkzeug (scrypt) |

---

## Project Structure

```
exam-module/
├── app.py                  # Application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── database.sql            # Database schema + sample data
├── .env.example            # Environment variables template
│
├── models/
│   └── database.py         # MySQL connection handler
│
├── controllers/
│   ├── auth_controller.py  # Login logic
│   ├── student_controller.py
│   ├── exam_controller.py
│   └── result_controller.py
│
├── routes/
│   ├── auth_routes.py      # /api/auth/*
│   ├── student_routes.py   # /api/students/*
│   ├── exam_routes.py      # /api/exams/*
│   ├── result_routes.py    # /api/results/*
│   └── page_routes.py      # Web page routes
│
├── utils/
│   ├── auth.py             # JWT helpers, grade calculation
│   └── validators.py       # Input validation
│
├── static/
│   ├── css/style.css
│   └── js/                 # Frontend API calls
│
└── templates/              # HTML pages
```

---

## Features

- **CRUD APIs** for Students, Exams, and Results
- **JWT Authentication** for all API endpoints
- **Login System** for web UI access
- **Auto Grade Calculation** (A+ to F based on percentage)
- **Input Validation** on all forms and API requests
- **Analytics Dashboard** with pass rate, grade distribution, and exam stats
- **Proper MVC Architecture** (Models, Routes, Controllers)

---

## Database Design

```
users          students         exams
  |               |                |
  |               +---- results ---+
  |                    (FK)
  id, username         id, student_id, exam_id
  password             marks, grade, percentage
```

### Tables

| Table | Description |
|-------|------------|
| `users` | Admin login credentials |
| `students` | Student records (name, email, phone, course) |
| `exams` | Exam details (name, subject, total marks) |
| `results` | Student exam results with auto-calculated grade |

### Grade Scale

| Percentage | Grade |
|-----------|-------|
| 90%+ | A+ |
| 80-89% | A |
| 70-79% | B |
| 60-69% | C |
| 40-59% | D |
| Below 40% | F |

---

## Setup & Run

### Prerequisites

- Python 3.10+
- MySQL Server

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/exam-module.git
cd exam-module
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup database

```bash
mysql -u root -p < database.sql
```

Or run the SQL manually in MySQL Workbench.

### 5. Configure environment

```bash
copy .env.example .env
```

Edit `.env` with your MySQL password:

```
MYSQL_PASSWORD=your_mysql_password
```

### 6. Run the application

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

### Default Login

| Username | Password |
|----------|----------|
| admin | admin123 |

---

## API Endpoints

All API endpoints (except login) require JWT token in header:
```
Authorization: Bearer <token>
```

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Login and get JWT token |
| POST | `/api/login` | Web login (returns token + session) |
| GET | `/api/auth/verify` | Verify token validity |

**Login Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Login Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "username": "admin"
}
```

### Students

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students` | Get all students |
| GET | `/api/students/:id` | Get student by ID |
| POST | `/api/students` | Create student |
| PUT | `/api/students/:id` | Update student |
| DELETE | `/api/students/:id` | Delete student |

**Create Student:**
```json
{
  "student_name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "course": "Computer Science"
}
```

### Exams

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/exams` | Get all exams |
| GET | `/api/exams/:id` | Get exam by ID |
| POST | `/api/exams` | Create exam |
| PUT | `/api/exams/:id` | Update exam |
| DELETE | `/api/exams/:id` | Delete exam |

**Create Exam:**
```json
{
  "exam_name": "Mid Term",
  "subject": "Data Structures",
  "total_marks": 100
}
```

### Results

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/results` | Get all results (with joins) |
| GET | `/api/results/analytics` | Get analytics data |
| GET | `/api/results/:id` | Get result by ID |
| POST | `/api/results` | Create result (auto grade) |
| PUT | `/api/results/:id` | Update result |
| DELETE | `/api/results/:id` | Delete result |

**Create Result:**
```json
{
  "student_id": 1,
  "exam_id": 1,
  "marks": 85
}
```

**Response includes auto-calculated grade:**
```json
{
  "success": true,
  "data": {
    "marks": 85,
    "grade": "A",
    "percentage": 85.0
  }
}
```

---

## Testing with Postman

1. **Login:** POST `http://localhost:5000/api/auth/login` with admin credentials
2. Copy the `token` from response
3. Add header: `Authorization: Bearer <token>`
4. Test CRUD endpoints

---

## Screenshots

> Add screenshots here before submission:
> - Login page
> - Dashboard
> - Student / Exam / Result management
> - Analytics page
> - Postman API responses

---

## Developer

**RECHINTHALA VINAY**

Robokalam Technologies — Full Stack Web Development Intern Assignment

---

## License

This project is developed for educational and internship purposes.
