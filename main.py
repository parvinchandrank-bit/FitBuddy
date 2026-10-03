from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from database.database import init_db, insert_progress, get_progress_records
from modules.gemini_service import GeminiService, GeminiServiceError
from modules.fitness_plan import build_fitness_plan_prompt
from modules.meal_plan import build_meal_plan_prompt

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="FitBuddy", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
gemini = GeminiService()

class FitnessProfile(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    age: int = Field(..., ge=13, le=100)
    gender: str
    height: float = Field(..., gt=50, lt=250)
    weight: float = Field(..., gt=20, lt=400)
    goal: str
    level: str
    workout_days: int = Field(..., ge=1, le=7)
    duration: int = Field(..., ge=10, le=180)
    equipment: str
    dietary_preference: str
    limitations: str = Field(default="", max_length=500)

class MealRequest(BaseModel):
    goal: str
    level: str
    dietary_preference: str
    weight: Optional[float] = None
    limitations: str = ""

class ProgressEntry(BaseModel):
    date: str
    weight: float = Field(..., gt=20, lt=400)
    workout_completed: bool = False
    workout_duration: int = Field(default=0, ge=0, le=480)
    notes: str = Field(default="", max_length=500)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"page": "home"})

@app.get("/progress", response_class=HTMLResponse)
async def progress_page(request: Request):
    return templates.TemplateResponse(request=request, name="progress.html", context={"page": "progress"})

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/generate-plan")
async def generate_plan(profile: FitnessProfile):
    try:
        return {"success": True, "plan": gemini.generate_json(build_fitness_plan_prompt(profile.model_dump()))}
    except GeminiServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

@app.post("/api/generate-meal-plan")
async def generate_meal_plan(data: MealRequest):
    try:
        return {"success": True, "meal_plan": gemini.generate_json(build_meal_plan_prompt(data.model_dump()))}
    except GeminiServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

@app.post("/api/progress")
async def add_progress(entry: ProgressEntry):
    return {"success": True, "record": insert_progress(entry.date, entry.weight, entry.workout_completed, entry.workout_duration, entry.notes)}

@app.get("/api/progress")
async def progress():
    return {"success": True, "records": get_progress_records()}
