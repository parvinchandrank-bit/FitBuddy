# FitBuddy – AI Fitness Plan Generator using Gemini Models

Naan Mudhalvan / Google Cloud Generative AI student project.

FitBuddy is an AI-powered fitness planning web application that generates personalized workout plans and meal suggestions using Google Gemini models.

Users can enter their fitness information, fitness goal, experience level, workout preferences, equipment availability, dietary preference, and limitations. FitBuddy then generates a personalized fitness plan using the Gemini API.

---

## 🚀 Live Demo

Open the live application:

https://fitbuddy-9hzu.onrender.com

The project is deployed using Render and can be accessed directly from a web browser.

---

## ✨ Features

- AI-generated personalized fitness plans
- 7-day workout planning
- Workout recommendations based on fitness level
- AI-generated meal suggestions
- Different fitness goals
- Beginner, Intermediate, and Advanced levels
- Workout duration and frequency customization
- Equipment-based workout recommendations
- Dietary preference support
- Fitness limitations support
- Progress tracking
- Weight tracking
- Workout completion tracking
- Progress history
- Weight progress chart
- SQLite database
- Responsive web interface
- Google Gemini API integration
- FastAPI backend
- Secure API key configuration
- Health check endpoint

---

## 🎯 Fitness Goals

FitBuddy supports multiple fitness goals:

- General Fitness
- Muscle Building
- Strength Improvement
- Weight Management
- Endurance
- Flexibility

---

## 🛠️ Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLite
- Jinja2

### Artificial Intelligence

- Google Gemini API
- `google-genai` Python SDK
- Gemini `gemini-3.5-flash-lite` model

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 Templates
- Chart.js

### Development & Deployment

- Git
- GitHub
- Render
- VS Code

---

## 📁 Project Structure

```text
FitBuddy/
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── PROJECT_DOCUMENTATION.md
├── LICENSE
│
├── modules/
│   ├── __init__.py
│   ├── gemini_service.py
│   ├── fitness_plan.py
│   └── meal_plan.py
│
├── database/
│   ├── __init__.py
│   └── database.py
│
├── templates/
│   ├── index.html
│   └── progress.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    ├── js/
    │   └── app.js
    │
    └── images/
        └── .gitkeep    