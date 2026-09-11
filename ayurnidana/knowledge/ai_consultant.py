"""AI Clinical Co-Pilot & Treatise Synthesizer.
Powered by Google Gemini models, grounded in classical Ayurvedic epistemology.
Supports local .env, Streamlit Cloud secrets, and runtime dynamic keys.
"""
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Search project roots for .env
for cand in [Path.cwd(), Path(__file__).resolve().parent.parent.parent]:
    cand_env = cand / ".env"
    if cand_env.exists():
        load_dotenv(cand_env)
        break
else:
    load_dotenv()

class AIConsultant:
    """Leverages Google Gemini with Ayurvedic systemic knowledge."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            try:
                import streamlit as st
                if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                    self.api_key = st.secrets["GEMINI_API_KEY"]
            except Exception:
                pass

        self.client = None
        self._init_client()

    def _init_client(self):
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None

    def set_api_key(self, api_key: str):
        """Allows setting the API key dynamically from Streamlit UI."""
        self.api_key = api_key.strip()
        self._init_client()

    def is_configured(self) -> bool:
        return self.client is not None

    def synthesize_consultation(
        self,
        patient_summary: str,
        diagnosis_summary: str,
        treatment_summary: str,
        user_question: str,
        notebook_context: str = "",
        treatise_context: str = "",
        mode: str = "layman"
    ) -> str:
        if not self.client:
            return (
                "Gemini AI API key not configured or client initialization failed. "
                "Please configure GEMINI_API_KEY in .env, add it to Streamlit Cloud Secrets, "
                "or enter your API key in the sidebar settings."
            )

        if mode == "physician":
            system_prompt = (
                "You are an eminent Ayurvedic Physician and Scholar (Pranacharya / Vaidya) with profound mastery of the "
                "Brihat Trayi (Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya) and Laghu Trayi (Madhava Nidana, "
                "Sharngadhara, Bhavaprakasha).\n\n"
                "Provide a rigorous, classical clinical analysis: cite specific Sthana and Adhyaya, explain the Shat Kriya Kala "
                "pathogenesis, detail Guna-Karma pharmacology of formulations, specify Aushadha Sevana Kala, Anupana, and modern red flags."
            )
        else:
            system_prompt = (
                "You are a friendly, compassionate, and experienced Ayurvedic Health Guide (AyurVaidya).\n\n"
                "Your role is to explain health issues to everyday patients in simple, clear, empowering language without "
                "confusing medical jargon. Use vivid analogies (e.g. comparing digestion to a cooking fire, Vata to the wind), "
                "focus on practical kitchen remedies, daily habits, teas, and soothing home guidance. Always maintain safety "
                "and alert the patient if something needs urgent in-person medical evaluation."
            )

        context_blocks = []
        if treatise_context:
            context_blocks.append(f"RELEVANT LOCAL CLASSICAL TREATISES AVAILABLE IN USER'S LIBRARY:\n{treatise_context}")
        if notebook_context:
            context_blocks.append(f"GROUNDED EVIDENCE FROM PERSONAL AYURVEDA NOTEBOOK:\n{notebook_context}")

        extra_grounding = "\n\n".join(context_blocks)
        if extra_grounding:
            extra_grounding = f"\n{extra_grounding}\n"

        user_content = f"""
PATIENT CASE DETAILS:
{patient_summary}

DIAGNOSTIC ASSESSMENT:
{diagnosis_summary}

TREATMENT BLUEPRINT:
{treatment_summary}

{extra_grounding}
PATIENT / PRACTITIONER QUESTION:
{user_question}

Deliver an organized, empathetic, and highly actionable response tailored to the requested perspective.
"""
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-flash-latest",
            "gemini-2.5-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-2.5-pro"
        ]
        last_err = None
        for model_name in models_to_try:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=user_content,
                    config={
                        "system_instruction": system_prompt,
                        "temperature": 0.3
                    }
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                last_err = e
                continue
        return f"Error communicating with AI consultant: {str(last_err)}"
