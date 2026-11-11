# FitTrack – Fitness & Workout Management Platform

## Project Overview

FitTrack is a fitness and workout management platform developed using Python and FastAPI. It allows users to manage workouts, track daily fitness progress, set fitness goals, monitor nutrition and water intake, receive workout recommendations, and view fitness analytics.

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

### Phase 1 – Core Fitness Tracking

**Module 1 – Authentication and User Management**
- User registration and login
- Password hashing using bcrypt
- JWT token generation
- Protected user profile endpoint

**Module 2 – Workout Management**
- Create, view, update and delete workouts
- Search and filter workouts

**Module 3 – Daily Progress Tracking**
- Track daily workouts
- Calculate total calories burned
- View daily progress and history

**Module 4 – Fitness Goals**
- Create, view, update and delete fitness goals
- Track target and current values

**Module 5 – Reports and Analytics**
- Fitness summary
- Category-wise workout reports
- Weekly and monthly reports
- Workout streak tracking
- Dashboard analytics

**Module 6 – Notifications**
- Create and view notifications
- View unread notifications
- Mark notifications as read
- Delete notifications

### Phase 2 – Advanced Tracking and User Engagement

**Module 7 – Workout Plans and Scheduling**
- Create workout plans
- Schedule workouts
- View scheduled workout plans

**Module 8 – Exercise Library**
- Manage exercise information
- Categorize exercises
- View exercise descriptions and durations

**Module 9 – Progress Comparison**
- Compare fitness progress and workout performance

### Phase 3 – Smart Features and Advanced Analytics

**Module 13 – Nutrition and Meal Tracking**
- Add meal entries
- Track calories, protein, carbohydrates and fats
- View meal history
- Generate daily nutrition summaries

**Module 14 – Water Intake Tracker**
- Record water intake in millilitres
- View water intake history
- Track daily water consumption against a 2500 ml goal

**Module 15 – AI Workout Suggestions**
- Generate workout recommendations based on fitness goals and workout history
- Suggest workout categories and exercises

**Module 16 – Workout Timer and Live Tracking**
- Start workout sessions
- Pause and resume sessions
- Stop workout sessions
- Track workout duration
- Estimate calories burned
- View workout session history

**Module 17 – Third-Party Integration**
- Support Google Fit and Apple Health provider selections
- Provide a fitness data synchronization endpoint
- Save submitted fitness activity data into the FitTrack database

Note: The current implementation uses simulated/manual synchronization. Actual Google Fit and Apple Health API connectivity is not implemented.

**Module 18 – Advanced Analytics Dashboard**
- Category-wise workout analytics
- Weekly performance analysis
- Monthly performance analysis
- Goal completion tracking
- Workout consistency analysis

**Module 19 – In-App Reminders and Alerts**
- Create reminders
- Categorize workout, meal and water reminders
- View and update reminders
- Mark reminders as completed
- Delete reminders

Note: The current implementation stores and manages reminders through APIs. Push notifications and background scheduling are not implemented.

## Project Structure

```text
FitTrack/
└── backend/
    ├── app/
    │   ├── routers/
    │   │   ├── auth.py
    │   │   ├── workouts.py
    │   │   ├── progress.py
    │   │   ├── goals.py
    │   │   ├── reports.py
    │   │   ├── notifications.py
    │   │   ├── workout_plans.py
    │   │   ├── exercises.py
    │   │   ├── dashboard.py
    │   │   ├── badges.py
    │   │   ├── meals.py
    │   │   ├── water.py
    │   │   ├── recommendations.py
    │   │   ├── workout_sessions.py
    │   │   ├── integrations.py
    │   │   ├── exports.py
    │   │   ├── analytics.py
    │   │   ├── reminders.py
    │   │   └── challenges.py
    │   ├── main.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── database.py
    │   ├── security.py
    │   ├── dependencies.py
    │   └── progress_utils.py
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

Use Swagger UI to explore and test API endpoints.

## Security Features

- JWT-based authentication
- Bcrypt password hashing
- Protected API endpoints
- User-specific data access
- Environment-based secret configuration
- Input validation using Pydantic
- Ownership validation for user data

## Testing

The implemented APIs have been manually tested through Swagger UI.

Testing includes:

- User registration and login
- JWT authentication
- Workout CRUD operations
- Progress tracking
- Fitness goal management
- Reports and analytics
- Nutrition and meal tracking
- Water intake tracking
- Workout recommendations
- Workout session management
- Fitness synchronization endpoint
- Advanced analytics endpoints
- Reminder management
- API health check

## Future Improvements

- Actual Google Fit and Apple Health API integration
- Automated push notifications and background reminder scheduling
- Machine-learning-based workout recommendations
- Automated unit and integration tests
- PostgreSQL database integration
- Database migrations using Alembic
- Docker deployment
- Frontend integration

## Important Note

FitTrack is a learning and development project focused on backend development. Additional security hardening, automated testing, real third-party integrations, and deployment configuration are recommended before production use.

## Author

Developed as a backend development project using Python and FastAPI.