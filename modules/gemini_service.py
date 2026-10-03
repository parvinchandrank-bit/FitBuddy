import json, os, re
from dotenv import load_dotenv
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None
load_dotenv()

class GeminiServiceError(RuntimeError):
    pass

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
        self.client = genai.Client(api_key=self.api_key) if genai and self.api_key else None

    def generate_json(self, prompt):
        if genai is None:
            raise GeminiServiceError("google-genai is not installed. Run pip install -r requirements.txt.")
        if not self.api_key:
            raise GeminiServiceError("Gemini API key is missing. Create .env and set GEMINI_API_KEY.")
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.6, response_mime_type="application/json"),
            )
        except Exception as exc:
            raise GeminiServiceError("Gemini request failed. Check API key, model, network, or quota.") from exc
        text = getattr(response, "text", None)
        if not text:
            raise GeminiServiceError("Gemini returned an empty response.")
        text = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.I)
        text = re.sub(r"\s*```$", "", text)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise GeminiServiceError("Gemini returned invalid JSON.") from exc
