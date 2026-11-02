# FitTrack – Fitness & Workout Management Platform

## Project Overview

FitTrack is a fitness and workout management platform developed using Python and FastAPI. It allows users to manage workouts, track daily fitness progress, set fitness goals, view reports and analytics, and receive notifications.

This project focuses on backend development, REST API design, authentication, database management, and user data security.

## Technologies Used

- **Language:** Python 3.10+
- **Backend Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Data Validation:** Pydantic
- **Authentication:** JWT
- **Password Security:** Bcrypt
- **API Testing:** Swagger UI
- **Version Control:** Git and GitHub

## Implemented Modules

### Module 1 – Authentication and User Management
- User registration
- User login
- Password hashing using bcrypt
- JWT token generation
- Protected user profile endpoint

### Module 2 – Workout Management
- Create workouts
- View workouts
- Update workouts
- Delete workouts
- Search and filter workouts

### Module 3 – Daily Progress Tracking
- Track daily workouts
- Calculate total calories burned
- View daily progress
- Maintain progress history

### Module 4 – Fitness Goals
- Create fitness goals
- View goals
- Update goals
- Delete goals
- Track target and current values

### Module 5 – Reports and Analytics
- Fitness summary
- Category-wise workout reports
- Weekly reports
- Monthly reports
- Workout streak tracking
- Dashboard analytics

### Module 6 – Notifications
- Create notifications
- View all notifications
- View unread notifications
- Mark notifications as read
- Delete notifications

## Project Structure

```text
FitTrack/
│
└── backend/
    │
    ├── app/
    │   ├── routers/
    │   │   ├── auth.py
    │   │   ├── workouts.py
    │   │   ├── progress.py
    │   │   ├── goals.py
    │   │   ├── reports.py
    │   │   └── notifications.py
    │   │
    │   ├── main.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── database.py
    │   ├── security.py
    │   ├── dependencies.py
    │   └── progress_utils.py
    │
    ├── .env
    ├── .gitignore
    ├── requirements.txt
    └── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the backend folder

```bash
cd FitTrack/backend
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file inside the backend folder:

```env
SECRET_KEY=your_strong_random_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./fittrack.db
```

Use a unique, strong secret key. Never commit `.env` to GitHub.

### 7. Start the FastAPI server

Run from the backend directory:

```bash
python -m uvicorn app.main:app --reload
```

## API Documentation

After starting the server, open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health Check: http://127.0.0.1:8000/health

Use Swagger UI to explore and test the API endpoints.

## Security Features

- JWT-based authentication
- Bcrypt password hashing
- Protected API endpoints
- User-specific data access
- Environment-based secret configuration
- Input validation using Pydantic

## Testing

The implemented APIs have been manually tested through Swagger UI.

Testing includes:

- User registration and login
- JWT authentication
- Workout CRUD operations
- Progress tracking
- Fitness goal management
- Reports and analytics
- Notification management
- User data isolation
- Database persistence after server restart
- API health check

## Future Improvements

- Automated unit and integration tests
- PostgreSQL database integration
- Database migrations using Alembic
- Docker deployment
- Advanced analytics
- Frontend integration

## Important Note

FitTrack is a learning and development project. Additional security hardening, automated testing, database migrations, and deployment configuration are recommended before production use.

## Author

Developed as a backend development project using Python and FastAPI.