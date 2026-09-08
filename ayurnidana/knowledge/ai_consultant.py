"""AI Clinical Co-Pilot & Treatise Synthesizer.
Powered by Google Gemini models, grounded in classical Ayurvedic epistemology.
"""
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class AIConsultant:
    """Leverages Google Gemini with Ayurvedic systemic knowledge."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                pass

    def is_configured(self) -> bool:
        return self.client is not None

    def synthesize_consultation(
        self,
        patient_summary: str,
        diagnosis_summary: str,
        treatment_summary: str,
        user_question: str
    ) -> str:
        if not self.client:
            return "Gemini AI API key not configured or client initialization failed. Please verify GEMINI_API_KEY in .env."

        system_prompt = (
            "You are a master Ayurvedic Physician (Pranacharya / Vaidya) possessing deep mastery of the "
            "classical Brihat Trayi (Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya) and Laghu Trayi "
            "(Madhava Nidana, Sharngadhara Samhita, Bhavaprakasha), as well as modern integrative physiology.\n\n"
            "Your task is to analyze patient cases, explain the intricate Samprapti (pathogenesis), provide "
            "classical Sanskrit shloka references where applicable, specify exact Aushadha Sevana Kala (timing), "
            "Anupana (vehicles), Pathya-Apathya regimens, and alert to modern red flags."
        )

        user_content = f"""
PATIENT CASE DETAILS:
{patient_summary}

DIAGNOSTIC ASSESSMENT:
{diagnosis_summary}

TREATMENT BLUEPRINT:
{treatment_summary}

CLINICAL QUERY / USER INQUIRY:
{user_question}

Provide a deep, authoritative, compassionate, and systematically organized clinical response.
"""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_content,
                config={
                    "system_instruction": system_prompt,
                    "temperature": 0.3
                }
            )
            return response.text
        except Exception as e:
            # Try fallback model
            try:
                response = self.client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=user_content
                )
                return response.text
            except Exception as e2:
                return f"Error communicating with AI consultant: {str(e2)}"
