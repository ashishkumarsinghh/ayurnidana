"""Layman Natural Language Symptom Parser & Mapping Utilities.
Translates everyday patient descriptions into clinical diagnostic markers.
"""
import re
from typing import List, Set

KEYWORD_MAP = {
    "joint_pain_cracking": [
        "crack", "clicking", "click", "knee pain", "joint pain", "joints hurt", 
        "arthritis", "crepitus", "hip pain", "elbow pain", "finger joint", "pain in joints"
    ],
    "pain_sharp_throbbing": [
        "sharp pain", "throbbing", "severe pain", "shooting pain", "stabbing pain", 
        "nerve pain", "sciatica", "excruciating"
    ],
    "tremors_stiffness": [
        "stiff", "stiffness", "tightness", "spasm", "cramp", "tremor", "trembling", 
        "can't bend", "locked joint", "morning stiffness"
    ],
    "constipation_hard_stools": [
        "constipat", "hard stool", "hard motion", "straining", "dry stool", 
        "can't poop", "irregular bowel", "pellet"
    ],
    "bloating_flatulence": [
        "bloat", "gas", "wind", "flatulence", "distended", "heavy stomach", 
        "swollen belly", "gassy"
    ],
    "insomnia_disturbed_sleep": [
        "can't sleep", "insomnia", "sleepless", "waking up", "poor sleep", 
        "disturbed sleep", "restless sleep"
    ],
    "anxiety_restlessness": [
        "anxious", "anxiety", "restless", "racing mind", "worry", "panic", 
        "nervous", "stressed"
    ],
    "dryness_skin_hair": [
        "dry skin", "dry lips", "rough skin", "dry hair", "flaking", 
        "itching from dryness", "ashy"
    ],
    "burning_sensation": [
        "burning", "burning feet", "burning palms", "heat in body", "feels like fire", 
        "burning sensation"
    ],
    "acid_reflux_heartburn": [
        "acid", "heartburn", "reflux", "gerd", "sour burp", "sour water", 
        "acidity", "chest burning", "belch"
    ],
    "intense_sharp_hunger": [
        "always hungry", "starving", "sharp hunger", "can't skip meal", "ravenous"
    ],
    "skin_rashes_inflammation_acne": [
        "rash", "redness", "acne", "pimples", "boil", "eczema", "hives", 
        "inflamed skin", "psoriasis"
    ],
    "loose_stools_diarrhea": [
        "loose stool", "diarrhea", "loose motion", "watery stool", "burning stool", "frequent stool"
    ],
    "yellowish_eyes_urine": [
        "yellow urine", "yellow eyes", "dark urine"
    ],
    "irritability_anger": [
        "angry", "short temper", "irritable", "frustrated", "snapping", "irritability"
    ],
    "heaviness_body_limbs": [
        "heavy", "heaviness", "lethargic", "feeling like a weight", "sluggish", 
        "heavy head", "heavy legs"
    ],
    "excess_mucus_congestion": [
        "mucus", "phlegm", "congestion", "clogged nose", "wet cough", "runny nose"
    ],
    "dull_pain_swelling_edema": [
        "swelling", "swollen", "puffy", "water retention", "edema", "puffy eyes", "swollen feet"
    ],
    "weight_gain_slow_metabolism": [
        "weight gain", "gaining weight", "slow metabolism", "obesity", "can't lose weight"
    ],
    "fever": [
        "fever", "feverish", "high temperature", "chills", "mild fever"
    ],
    "tongue_thick_white_coating": [
        "white tongue", "coated tongue", "furry tongue", "gross tongue", "pasty tongue"
    ],
    "loss_of_taste_aruchi": [
        "no appetite", "loss of appetite", "no taste", "food tastes bad", "don't feel like eating"
    ]
}

def extract_symptoms_from_text(text: str) -> List[str]:
    """Analyzes layman English text and extracts matching symptom IDs."""
    text_lower = text.lower()
    matched = set()

    for sym_id, keywords in KEYWORD_MAP.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower) or kw in text_lower:
                matched.add(sym_id)
                break

    return list(matched)
