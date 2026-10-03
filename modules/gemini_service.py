import json
import os
import re

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
        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        ).strip()

        self.client = (
            genai.Client(api_key=self.api_key)
            if genai and self.api_key
            else None
        )

    def generate_json(self, prompt):
        # Check whether google-genai is installed
        if genai is None:
            raise GeminiServiceError(
                "google-genai is not installed. "
                "Run: pip install -r requirements.txt"
            )

        # Check API key
        if not self.api_key:
            raise GeminiServiceError(
                "Gemini API key is missing. "
                "Create .env and set GEMINI_API_KEY."
            )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.6,
                    response_mime_type="application/json",
                ),
            )

        except Exception as exc:
            print(
                f"\nGEMINI API ERROR: "
                f"{type(exc).__name__}: {exc}\n"
            )

            raise GeminiServiceError(
                f"Gemini request failed: "
                f"{type(exc).__name__}: {exc}"
            ) from exc

        # Get Gemini response text
        text = getattr(response, "text", None)

        if not text:
            raise GeminiServiceError(
                "Gemini returned an empty response."
            )

        # Remove Markdown JSON code fences if Gemini returns them
        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text.strip(),
            flags=re.I,
        )

        text = re.sub(
            r"\s*```$",
            "",
            text,
        )

        # Parse JSON response
        try:
            return json.loads(text)

        except json.JSONDecodeError as exc:
            print(
                f"\nGEMINI JSON ERROR: {exc}"
                f"\nResponse received:\n{text}\n"
            )

            raise GeminiServiceError(
                "Gemini returned invalid JSON."
            ) from exc