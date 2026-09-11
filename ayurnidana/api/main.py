from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json

from ayurnidana.core.models import (
    Gender, AmaStatus, AgniType, KoshthaType,
    PatientDemographics, AshtaSthanaPariksha, DashavidhaPariksha, ClinicalCase
)
from ayurnidana.core.dosha_engine import DoshaEngine
from ayurnidana.core.nidana_engine import NidanaEngine
from ayurnidana.core.chikitsa_engine import ChikitsaEngine
from ayurnidana.core.layman_mapper import (
    get_symptom_label,
    get_symptoms_by_category,
    SYMPTOM_DEFINITIONS,
    extract_symptoms_with_ai,
)
from ayurnidana.knowledge.ai_consultant import AIConsultant
from ayurnidana.ui.components.case_sheet import generate_markdown_case_sheet
from ayurnidana.api.database import (
    authenticate_user, register_user, save_consultation, get_user_consultations
)

app = FastAPI(title="AyurNidana API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai = AIConsultant()

class AuthRequest(BaseModel):
    identity: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    age: int
    gender: str

class ExtractRequest(BaseModel):
    story: str

class ConsultRequest(BaseModel):
    patient_name: str
    age: int
    gender: str
    symptoms: Dict[str, str]
    tongue: str
    stool: str
    hunger: str
    comorbidities: str = ""

class ChatRequest(BaseModel):
    patient_summary: str
    diagnosis_summary: str
    treatment_summary: str
    user_question: str

@app.post("/api/auth/login")
def login(req: AuthRequest):
    ok, msg, user = authenticate_user(req.identity, req.password)
    if not ok: raise HTTPException(status_code=401, detail=msg)
    return {"user": user, "message": msg}

@app.post("/api/auth/register")
def register(req: RegisterRequest):
    ok, msg, user = register_user(req.username, req.email, req.password, req.full_name, req.age, req.gender)
    if not ok: raise HTTPException(status_code=400, detail=msg)
    return {"user": user, "message": msg}

@app.get("/api/symptoms")
def get_symptoms():
    return SYMPTOM_DEFINITIONS

@app.post("/api/symptoms/extract")
def extract_symptoms(req: ExtractRequest):
    found = extract_symptoms_with_ai(req.story, ai)
    return {"extracted": found}

@app.post("/api/consult")
def run_consultation(req: ConsultRequest):
    tongue_str = {"clean": "Clean — healthy pink, no coating", "white": "Thick white coating (Ama / Kapha)", "red": "Red, yellow, or inflamed (Pitta)", "dry": "Dry, rough, or cracked (Vata)"}.get(req.tongue, "Clean")
    stool_str = {"normal": "Normal, regular, easy to pass", "hard": "Hard, dry, pebble-like", "loose": "Loose, watery, urgent", "sticky": "Sticky, heavy, foul-smelling"}.get(req.stool, "Normal")
    hunger_str = {"normal": "Normal and steady", "intense": "Intense & sharp", "irregular": "Irregular", "weak": "Weak / sluggish"}.get(req.hunger, "Normal")

    dosha_pct, vikriti = DoshaEngine.calculate_vikriti(req.symptoms)
    ama_status, ama_reasons = DoshaEngine.assess_ama(req.symptoms, tongue_str)
    dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(req.symptoms)

    if "sharp" in hunger_str.lower() or "intense" in hunger_str.lower(): agni = AgniType.TIKSHNAGNI
    elif "weak" in hunger_str.lower() or ama_status == AmaStatus.SAMA: agni = AgniType.MANDAGNI
    elif "irregular" in hunger_str.lower(): agni = AgniType.VISHAMAGNI
    else: agni = AgniType.SAMAGNI

    if "hard" in stool_str.lower(): koshtha = KoshthaType.KRURA
    elif "loose" in stool_str.lower(): koshtha = KoshthaType.MRIDU
    else: koshtha = KoshthaType.MADHYAMA

    dx = NidanaEngine.diagnose(req.symptoms, vikriti, ama_status, agni, koshtha, dhatus, srotas, req.age, req.comorbidities)
    dasha = DashavidhaPariksha(prakriti=vikriti.split("(")[0].strip(), vikriti=vikriti, sara_tissue_excellence="Madhyama", samhanana_compactness="Madhyama", sattva_mental_strength="Madhyama", ahara_shakti_digestive_power=hunger_str, vyayama_shakti_physical_stamina="Madhyama", vaya_age_stage="Madhyamavastha" if req.age < 60 else "Vriddhavastha")
    
    tx = ChikitsaEngine.generate_plan(dx, dasha, req.age, req.comorbidities, "Current Season")

    return {
        "diagnosis": dx.dict() if hasattr(dx, 'dict') else dx.__dict__,
        "treatment": tx.dict() if hasattr(tx, 'dict') else tx.__dict__,
        "dosha_pct": dosha_pct,
        "ama_status": ama_status.value if hasattr(ama_status, 'value') else str(ama_status),
        "agni": agni.value if hasattr(agni, 'value') else str(agni),
        "koshtha": koshtha.value if hasattr(koshtha, 'value') else str(koshtha)
    }

@app.post("/api/chat")
def ask_vaidya(req: ChatRequest):
    resp = ai.synthesize_consultation(req.patient_summary, req.diagnosis_summary, req.treatment_summary, req.user_question, "layman")
    return {"reply": resp}

@app.get("/api/history/{user_id}")
def history(user_id: int):
    return get_user_consultations(user_id)

class SaveHistoryRequest(BaseModel):
    user_id: int
    story: str
    symptoms: dict
    primary_condition: str
    sanskrit_name: str
    dosha_scores: dict
    treatment_summary: str
    case_sheet_md: str = ''

@app.post("/api/history")
def save_hist(req: SaveHistoryRequest):
    cid = save_consultation(req.user_id, req.story, req.symptoms, req.primary_condition, req.sanskrit_name, req.dosha_scores, req.treatment_summary, req.case_sheet_md)
    return {"id": cid}
