# FitBuddy – AI Fitness Plan Generator using Gemini Models

Naan Mudhalvan / Google Cloud Generative AI student project.

## Run on Windows

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set:

```env
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_MODEL=gemini-2.5-flash
```

Start:

```powershell
uvicorn main:app --reload
```

Open http://127.0.0.1:8000

Health check: http://127.0.0.1:8000/api/health

The project uses the current `google-genai` SDK and the modern FastAPI/Starlette TemplateResponse syntax. Never upload `.env` to GitHub.
