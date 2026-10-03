# FitBuddy Project Documentation

## Abstract
FitBuddy is a Generative AI fitness assistant using Google Gemini, FastAPI, Jinja2, Vanilla JavaScript and SQLite.

## Objectives
- Generate a seven-day general fitness plan.
- Adapt plans to goal, level, schedule and equipment.
- Generate general meal suggestions.
- Track progress and weight.
- Demonstrate Gemini prompt engineering.

## Architecture
Browser → FastAPI → Gemini API
Browser → FastAPI → SQLite

## Modules
- Fitness Plan Generator
- Meal Recommendation Generator
- Progress Tracking
- Responsive Frontend

## API
GET `/`
GET `/progress`
GET `/api/health`
POST `/api/generate-plan`
POST `/api/generate-meal-plan`
POST `/api/progress`
GET `/api/progress`

## Safety
FitBuddy provides general educational fitness information and is not a substitute for professional medical advice. It does not diagnose conditions, prescribe treatment, or provide medical nutrition prescriptions.
