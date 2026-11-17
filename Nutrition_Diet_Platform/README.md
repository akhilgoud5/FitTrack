# Nutrition & Diet Management Platform

## Project Overview

The **Nutrition & Diet Management Platform** is a backend application designed to help users manage their diet plans, track daily nutrition, monitor food intake, receive diet recommendations, manage subscriptions, and book consultations with nutritionists and doctors.

The application provides REST APIs using FastAPI and stores application data using SQLAlchemy and SQLite.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Passlib & Bcrypt
- Uvicorn
- Alembic
- ReportLab

## Project Structure

```text
Nutrition_Diet_Platform/
│
└── backend/
    ├── app/
    │   ├── routers/
    │   │   ├── auth.py
    │   │   ├── diet_plans.py
    │   │   ├── meals.py
    │   │   ├── subscriptions.py
    │   │   ├── nutritionists.py
    │   │   ├── recommendations.py
    │   │   ├── notifications.py
    │   │   └── doctors.py
    │   │
    │   ├── __init__.py
    │   ├── main.py
    │   ├── database.py
    │   ├── models.py
    │   ├── schemas.py
    │   └── dependencies.py
    │
    ├── requirements.txt
    ├── .env
    └── .gitignore
```

## Implemented Modules

### Module 1 – User Authentication
- User registration
- User login
- JWT authentication
- Password hashing
- Get logged-in user profile

### Module 2 – Diet Plan Management
- Create diet plans
- View available diet plans
- View individual diet plans
- Assign diet plans to users
- View my assigned diet plans

### Module 3 – Meal & Nutrition Tracking
- Add daily meals
- View meal history
- Track calories
- Track protein, carbohydrates and fats
- View daily nutrition summary

### Module 4 – Subscription Management
- Free subscription
- Premium subscription
- Pro subscription
- Subscribe to a plan
- Upgrade and downgrade subscription
- View current subscription

### Module 5 – Nutritionist Consultation
- Add nutritionists
- View nutritionists
- View nutritionist profiles
- Book consultations
- View consultation history

### Module 6 – Diet Recommendations
- Goal-based diet recommendations
- Weight Loss recommendations
- Muscle Gain recommendations
- Maintenance recommendations
- Activity-level and calorie-based filtering

### Module 7 – Notifications & Reminders
- Create notifications
- View personal notifications
- Mark notifications as read
- Delete notifications

### Module 8 – Doctor Support & Appointment Management
- Add doctors
- View all doctors
- View doctor profiles
- Book doctor appointments
- View personal appointment history

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to Backend

```bash
cd Nutrition_Diet_Platform/backend
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file and configure your secret key.

```env
SECRET_KEY=your_secret_key
```

Use a strong secret key for production.

### 7. Run the Application

```bash
uvicorn app.main:app --reload
```

## API Documentation

After starting the application, open:

**Swagger UI:**

http://127.0.0.1:8000/docs

**ReDoc:**

http://127.0.0.1:8000/redoc

Swagger UI allows users to test API endpoints interactively.

## Database

- Database: SQLite
- ORM: SQLAlchemy
- Database file: nutrition_diet.db

## Authentication

The application uses JWT-based authentication.

Protected endpoints require a valid Bearer token.

## Testing

The implemented APIs were tested using FastAPI Swagger UI.

Tested operations include:

- User registration and login
- Diet plan creation and assignment
- Meal tracking and nutrition summary
- Subscription management
- Nutritionist consultation booking
- Diet recommendations
- Notification creation and management
- Doctor creation and appointment booking

## Future Enhancements

- React frontend integration
- Online payment gateway
- Automated meal reminders
- AI-powered personalized diet recommendations
- Advanced nutrition analytics
- Doctor appointment confirmation and cancellation
- PDF nutrition reports

## Project Status

**Backend development: 8 modules implemented and tested through Swagger UI.**

## Author

Developed as a Python FastAPI backend project.

