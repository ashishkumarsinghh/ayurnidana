"""Layman Natural Language Symptom Parser & Mapping Utilities.
Translates everyday patient descriptions into clinical diagnostic markers with frequency & severity detection.
Supports rich English, Hindi/Hinglish, colloquial expressions, and Gemini AI parsing.
"""
import re
import json
from typing import List, Dict, Set, Optional, Tuple, Any

# Complete definitions for all clinical symptoms in AyurNidana
SYMPTOM_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    # ----------------- Digestion & Gut -----------------
    "acid_reflux_heartburn": {
        "label": "Acid reflux, heartburn, or sour liquid rising in throat",
        "category": "Stomach & Digestion",
        "keywords": [
            "acid", "heartburn", "reflux", "gerd", "sour burp", "sour water", "acidity",
            "chest burning", "belch", "water brash", "amlapitta", "burning stomach",
            "pitta", "jalan in chest", "khatta dakar", "pet me jalan", "chhati me jalan",
            "hyperacidity", "sour stomach", "gastric burning", "burning in food pipe"
        ]
    },
    "bloating_flatulence": {
        "label": "Bloated stomach, gas, flatulence, or distension",
        "category": "Stomach & Digestion",
        "keywords": [
            "bloat", "bloating", "gas", "gassy", "wind", "flatulence", "distended",
            "heavy stomach", "swollen belly", "belching wind", "tympanites", "admana",
            "pet phoolna", "gas banna", "afra", "pet bhari", "stomach gas", "burping excess"
        ]
    },
    "constipation_hard_stools": {
        "label": "Constipation, hard/dry stools, straining, or infrequent motions",
        "category": "Stomach & Digestion",
        "keywords": [
            "constipat", "hard stool", "hard motion", "straining", "dry stool", "can't poop",
            "irregular bowel", "pellet", "dry motions", "vibandha", "kabz", "pet saaf nahi hota",
            "hard bowel", "passing stool with pain", "straining on toilet", "stools dry"
        ]
    },
    "loose_stools_diarrhea": {
        "label": "Loose stools, frequent bowel movements, or mild diarrhea",
        "category": "Stomach & Digestion",
        "keywords": [
            "loose stool", "diarrhea", "diarrhoea", "loose motion", "watery stool", "burning stool",
            "frequent stool", "atisara", "dast", "pet kharab", "frequent motions", "urgent stool",
            "runny stomach", "loose motions"
        ]
    },
    "severe_acute_diarrhea": {
        "label": "Severe acute diarrhea, sudden watery purging, or infection",
        "category": "Stomach & Digestion",
        "keywords": [
            "frequent loose motions", "watery diarrhea", "stomach infection", "acute diarrhea",
            "cramping and loose stools", "gastroenteritis", "severe atisara", "dehydrating diarrhea",
            "constant loose motions", "bahut dast"
        ]
    },
    "malabsorption_mucus_stools": {
        "label": "Mucus in stool, undigested food particles, or alternating bowels",
        "category": "Stomach & Digestion",
        "keywords": [
            "mucus in stool", "sticky stool", "undigested food in stool", "alternating loose and hard",
            "ibs", "irritable bowel", "grahani", "greasy stool", "floating stool", "stools stick to bowl",
            "amashaya", "aon padna", "aon nikalna", "pechis"
        ]
    },
    "loss_of_taste_aruchi": {
        "label": "Loss of appetite, food tastes bland, or aversion to eating",
        "category": "Stomach & Digestion",
        "keywords": [
            "no appetite", "loss of appetite", "no taste", "food tastes bad", "don't feel like eating",
            "aruchi", "anorexia", "bhookh nahi lagti", "muh ka swad kharab", "distaste for food",
            "food aversion", "loss of taste buds"
        ]
    },
    "intense_sharp_hunger": {
        "label": "Sharp, ravenous hunger (weak/faint/angry if meals delayed)",
        "category": "Stomach & Digestion",
        "keywords": [
            "always hungry", "starving", "sharp hunger", "can't skip meal", "ravenous",
            "tikshnagni", "bhookh bardasht nahi hoti", "extreme hunger", "shaking when hungry",
            "voracious appetite"
        ]
    },
    "irregular_appetite": {
        "label": "Unpredictable appetite (starving one day, no appetite the next)",
        "category": "Stomach & Digestion",
        "keywords": [
            "irregular appetite", "variable hunger", "sometimes hungry sometimes not", "vishamagni",
            "unpredictable hunger", "forgetting to eat", "kabhi bhookh lagti kabhi nahi"
        ]
    },
    "slow_sluggish_digestion": {
        "label": "Sluggish digestion, food sits for hours like a stone",
        "category": "Stomach & Digestion",
        "keywords": [
            "slow digestion", "sluggish metabolism", "food sits like a stone", "heavy after small meal",
            "mandagni", "hazam nahi hota", "khana pachta nahi", "slow digestion process"
        ]
    },
    "heaviness_in_abdomen": {
        "label": "Abdominal heaviness and dull fullness after meals",
        "category": "Stomach & Digestion",
        "keywords": [
            "heavy abdomen", "stomach heaviness", "fullness after eating", "stomach feels packed",
            "pet me bhari pan", "abdominal weight", "postprandial fullness"
        ]
    },
    "sticky_foul_smelling_stools": {
        "label": "Foul-smelling, sticky, sinking stools (Ama signs)",
        "category": "Stomach & Digestion",
        "keywords": [
            "sticky stool", "foul smelling stool", "very smelly poop", "stool sinks",
            "offensive stool", "bad smelling motion", "durgandhita mala"
        ]
    },
    "sweet_taste_in_mouth": {
        "label": "Persistent sweet or sticky taste in mouth",
        "category": "Stomach & Digestion",
        "keywords": [
            "sweet taste in mouth", "sugary taste", "sweet saliva", "madhurya",
            "mouth tastes sweet", "muh me meetha swad"
        ]
    },
    "foul_breath": {
        "label": "Bad breath, unpleasant odor despite brushing",
        "category": "Stomach & Digestion",
        "keywords": [
            "foul breath", "bad breath", "halitosis", "mouth odor", "mukhadurgandhi",
            "muh se badbu"
        ]
    },
    "obstruction_mala_stambha": {
        "label": "Difficulty passing flatus or feeling of blockage in bowels",
        "category": "Stomach & Digestion",
        "keywords": [
            "bowel obstruction", "cannot pass gas", "trapped gas", "mala stambha",
            "gas ruki hui", "blocked bowel", "incomplete evacuation"
        ]
    },

    # ----------------- Joints, Back & Nerves -----------------
    "joint_pain_cracking": {
        "label": "Joint pain, stiffness, or cracking / clicking sounds on movement",
        "category": "Joints, Back & Muscles",
        "keywords": [
            "crack", "clicking", "click", "knee pain", "joint pain", "joints hurt",
            "arthritis", "crepitus", "hip pain", "elbow pain", "finger joint", "pain in joints",
            "creaking", "sandhivata", "ghutne me dard", "jod me dard", "clicking knee",
            "popping joints", "joint ache"
        ]
    },
    "pain_sharp_throbbing": {
        "label": "Sharp, throbbing, excruciating, or shooting pains",
        "category": "Joints, Back & Muscles",
        "keywords": [
            "sharp pain", "throbbing", "severe pain", "shooting pain", "stabbing pain",
            "nerve pain", "excruciating", "piercing pain", "shoola", "tez dard",
            "tash-tash dard", "pulsating pain", "stabbing sensation"
        ]
    },
    "sciatica_radiating_leg_pain": {
        "label": "Sciatica shooting pain from lower back / buttock down the leg",
        "category": "Joints, Back & Muscles",
        "keywords": [
            "sciatica", "pain shooting down leg", "pain radiating down leg", "hip to foot pain",
            "buttock pain", "lumbar radiculopathy", "lower back shooting pain", "gridhrasi",
            "radiating back pain", "kamar se pair tak dard", "leg shooting ache"
        ]
    },
    "tremors_stiffness": {
        "label": "Morning joint stiffness, spasms, muscle cramps, or tremors",
        "category": "Joints, Back & Muscles",
        "keywords": [
            "stiff", "stiffness", "tightness", "spasm", "cramp", "tremor", "trembling",
            "can't bend", "locked joint", "morning stiffness", "rigid", "stambha",
            "jakdan", "subah jakad", "muscle stiffness", "muscle cramps", "shaking hands"
        ]
    },
    "dull_pain_swelling_edema": {
        "label": "Swelling, puffiness, fluid retention, or heavy dull ache in joints",
        "category": "Joints, Back & Muscles",
        "keywords": [
            "swelling", "swollen", "puffy", "water retention", "edema", "puffy eyes",
            "swollen feet", "shotha", "sujan", "swollen ankles", "fluid retention",
            "puffy joints", "edematous"
        ]
    },
    "gout_big_toe_burning_pain": {
        "label": "Fiery, throbbing pain, heat and redness in big toe / foot",
        "category": "Joints, Back & Muscles",
        "keywords": [
            "big toe pain", "uric acid", "gout", "vatarakta", "inflamed toe",
            "throbbing foot pain", "red hot toe", "podagra", "anguthe me dard aur jalan"
        ]
    },
    "body_aches_angamarda": {
        "label": "Generalized body ache, feeling beaten up, muscle fatigue",
        "category": "Joints, Back & Muscles",
        "keywords": [
            "body ache", "body aches", "angamarda", "feeling beaten", "muscles hurt all over",
            "badan dard", "sharir me dard", "whole body pain", "general aches"
        ]
    },

    # ----------------- Breathing & Respiratory -----------------
    "wheezing_shortness_of_breath": {
        "label": "Wheezing, breathlessness, chest tightness, worse lying down",
        "category": "Breathing & Chest",
        "keywords": [
            "wheezing", "asthma", "short of breath", "breathlessness", "tight chest breathing",
            "can't breathe lying down", "tamaka shwasa", "dyspnea", "saans lene me takleef",
            "saans phoolna", "whistling breath", "chest congestion breathing", "bronchial spasm"
        ]
    },
    "cough_chronic": {
        "label": "Chronic hacking, dry, or tickling cough",
        "category": "Breathing & Chest",
        "keywords": [
            "cough", "coughing", "dry cough", "hacking cough", "chronic cough", "kasa",
            "throat tickle", "khansi", "sukhi khansi", "cough fits", "constant coughing"
        ]
    },
    "excess_mucus_congestion": {
        "label": "Excess phlegm, sinus congestion, runny nose, or post-nasal drip",
        "category": "Breathing & Chest",
        "keywords": [
            "mucus", "phlegm", "congestion", "clogged nose", "wet cough", "runny nose",
            "sinus", "kapha", "balgam", "nazla", "jukam", "stuffy nose", "sinusitis",
            "productive cough", "mucus in throat"
        ]
    },
    "fever": {
        "label": "Feverish temperature, hot body, chills, or low-grade pyrexia",
        "category": "Breathing & Chest",
        "keywords": [
            "fever", "feverish", "high temperature", "chills", "mild fever", "jwara",
            "bukhar", "tap", "hot forehead", "shivering with heat", "low grade fever"
        ]
    },

    # ----------------- Skin & Elimination -----------------
    "burning_sensation": {
        "label": "Burning sensation in palms, soles, chest, or throughout the body",
        "category": "Skin & Elimination",
        "keywords": [
            "burning", "burning feet", "burning palms", "heat in body", "feels like fire",
            "burning sensation", "daha", "jalan", "hatheli me jalan", "talwon me jalan",
            "hot sensations", "flaming heat"
        ]
    },
    "skin_rashes_inflammation_acne": {
        "label": "Red rashes, itchy eczema patches, psoriasis scaling, or acne/boils",
        "category": "Skin & Elimination",
        "keywords": [
            "rash", "redness", "acne", "pimples", "boil", "eczema", "hives",
            "inflamed skin", "psoriasis", "skin lesions", "kushtha", "itching and scaling",
            "chhapaki", "khujli", "chakatte", "skin red patches", "dermatitis", "itching skin"
        ]
    },
    "dryness_skin_hair": {
        "label": "Dry, rough, flaky skin, chapped lips, or dry brittle hair",
        "category": "Skin & Elimination",
        "keywords": [
            "dry skin", "dry lips", "rough skin", "dry hair", "flaking", "itching from dryness",
            "ashy", "cracked skin", "xeroderma", "rukha pan", "tvak rukshata", "scaly dry skin",
            "chapped hands"
        ]
    },
    "oily_greasy_skin": {
        "label": "Excessively oily face, greasy forehead, sebum buildup",
        "category": "Skin & Elimination",
        "keywords": [
            "oily skin", "greasy face", "oily forehead", "greasy skin", "excess oil",
            "teliyata", "chikna chehra"
        ]
    },
    "cold_clammy_skin": {
        "label": "Cold, clammy, sweaty hands or pale cool skin",
        "category": "Skin & Elimination",
        "keywords": [
            "clammy skin", "cold sweat", "cool clammy hands", "moist cold skin",
            "thanda pasina"
        ]
    },
    "burning_painful_urination": {
        "label": "Burning sensation or sharp pain while urinating (dysuria)",
        "category": "Skin & Elimination",
        "keywords": [
            "burning pee", "burning urine", "painful urination", "dysuria", "stinging urine",
            "uti", "urine hurts", "mutrakrichhra", "difficulty urinating", "peshab me jalan",
            "peshab me dard", "scalding urine"
        ]
    },
    "frequent_cloudy_urination": {
        "label": "Frequent urination, cloudy/turbid urine, or waking to urinate",
        "category": "Skin & Elimination",
        "keywords": [
            "frequent urination", "peeing often", "cloudy urine", "prameha", "night urination",
            "nocturia", "bar bar peshab", "turbid urine", "peeing many times"
        ]
    },
    "cloudy_milky_frothy_urine": {
        "label": "Milky, frothy, dense urine with sediment",
        "category": "Skin & Elimination",
        "keywords": [
            "frothy urine", "milky urine", "foamy urine", "sediment in urine",
            "shuklameha", "jhag wala peshab"
        ]
    },
    "anal_pain_bleeding_piles": {
        "label": "Painful anorectal piles, hemorrhoid lumps, or rectal bleeding",
        "category": "Skin & Elimination",
        "keywords": [
            "piles", "hemorrhoid", "anal pain", "lump in anus", "bleeding after stool",
            "arsha", "rectal swelling", "bawasir", "anal fissure", "rectal pain"
        ]
    },
    "yellowish_eyes_urine": {
        "label": "Yellowish tint in eyes / sclera, dark yellow urine, severe nausea",
        "category": "Skin & Elimination",
        "keywords": [
            "yellow urine", "yellow eyes", "dark urine", "jaundice", "kamala",
            "yellow sclera", "icterus", "piliya", "aankh pili", "dark yellow pee"
        ]
    },
    "ulceration_bleeding_tendency": {
        "label": "Mouth ulcers, bleeding gums, nosebleeds, or easy bruising",
        "category": "Skin & Elimination",
        "keywords": [
            "bleeding gums", "mouth ulcers", "blood in stool", "bleeding piles", "hemorrhoids",
            "epistaxis", "raktapitta", "nosebleed", "bruising", "muh ke chhale"
        ]
    },
    "heat_intolerance": {
        "label": "Cannot tolerate warm weather, excessive heat, sweating heavily",
        "category": "Skin & Elimination",
        "keywords": [
            "feel hot", "excessive heat", "sweat too easily", "can't tolerate sun",
            "hot flushes", "garmi bardasht nahi", "excessive perspiration"
        ]
    },
    "cold_intolerance": {
        "label": "Very sensitive to cold, freezing hands and feet, shivers easily",
        "category": "Skin & Elimination",
        "keywords": [
            "feel cold", "cold hands", "cold feet", "intolerant to cold", "chills easily",
            "shivering", "sheetasahishnuta", "thand lagti hai", "freezing toes"
        ]
    },
    "excessive_thirst_sweating": {
        "label": "Extreme unquenchable thirst and profuse sweating",
        "category": "Skin & Elimination",
        "keywords": [
            "excessive thirst", "always thirsty", "profuse sweating", "trishna", "sweda",
            "bahut pyas lagti hai", "excess sweat", "drinking water continuously"
        ]
    },

    # ----------------- Mind, Sleep & Energy -----------------
    "insomnia_disturbed_sleep": {
        "label": "Trouble falling asleep, waking frequently, or racing thoughts at night",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "can't sleep", "insomnia", "sleepless", "waking up", "poor sleep",
            "disturbed sleep", "restless sleep", "anidra", "trouble sleeping", "broken sleep",
            "neend nahi aati", "neend khulna", "racing thoughts night", "sleeplessness"
        ]
    },
    "excessive_sleep_lethargy": {
        "label": "Excessive sleeping, difficulty waking, daytime drowsiness",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "sleeping too much", "oversleeping", "excessive sleep", "atinidra",
            "daytime sleepiness", "can't wake up", "bahut neend aana", "heavy drowsiness"
        ]
    },
    "lethargy_post_meal_drowsiness": {
        "label": "Intense drowsiness or total lack of energy after meals (Alasya)",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "drowsy after eating", "post meal coma", "alasya", "tandra", "heavy after food",
            "khana khate hi neend", "lazy after eating", "extreme post meal fatigue"
        ]
    },
    "anxiety_restlessness": {
        "label": "Feeling anxious, nervous, on edge, restless, or worrying excessively",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "anxious", "anxiety", "restless", "racing mind", "worry", "panic",
            "nervous", "stressed", "chittodvega", "overthinking", "nervousness",
            "bechaini", "ghabrahat", "mind jumping", "inner restlessness"
        ]
    },
    "panic_intense_worry": {
        "label": "Sudden intense panic attacks, dread, or pounding heart from fear",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "panic attack", "panic", "sudden fear", "dread", "terror", "intense worry",
            "palpitations with fear", "bhaya", "dil ghabrana", "sudden adrenaline surge"
        ]
    },
    "irritability_anger": {
        "label": "Short temper, easily frustrated, impatient, or fiery anger",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "angry", "short temper", "irritable", "frustrated", "snapping", "irritability",
            "krodha", "gussa", "chidhchidhapan", "quick temper", "loss of patience"
        ]
    },
    "attachment_depression": {
        "label": "Low mood, feelings of attachment, melancholy, or sadness",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "depressed", "sadness", "attachment", "grief", "low mood", "vishada",
            "udasi", "man udas", "hopeless feeling", "melancholic"
        ]
    },
    "headache_migraine_throbbing": {
        "label": "Throbbing temple headache, half-sided migraine, or scalp sensitivity",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "headache", "migraine", "temple pain", "throbbing head", "head hurts",
            "half head pain", "ardhavabhedaka", "shirashoola", "pounding head",
            "sar dard", "adha sar dard", "forehead pain", "cranial tension"
        ]
    },
    "heaviness_body_limbs": {
        "label": "Heavy body, limbs feel like lead, sluggishness, mental cloudiness",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "heavy", "heaviness", "lethargic", "feeling like a weight", "sluggish",
            "heavy head", "heavy legs", "gaurava", "sharir bhari", "leads in limbs",
            "sluggish body"
        ]
    },
    "pallor_fatigue_anemia": {
        "label": "Pale skin, extreme exhaustion, breathlessness on climbing stairs",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "anemia", "pale skin", "pale face", "tired easily", "fatigue", "low hemoglobin",
            "pandu", "breathless on climbing stairs", "exhaustion", "thakan", "kamzori",
            "pale tongue", "low energy all day", "asthenia"
        ]
    },
    "weight_gain_slow_metabolism": {
        "label": "Rapid or stubborn weight gain, sluggish metabolism, obesity",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "weight gain", "gaining weight", "slow metabolism", "obesity", "can't lose weight",
            "sthaulya", "heavy body", "vajan badhna", "motaapa", "putting on weight"
        ]
    },
    "weight_loss_emaciation": {
        "label": "Unexplained weight loss, muscle wasting, thinning, or weakness",
        "category": "Mind, Sleep & Energy",
        "keywords": [
            "weight loss", "losing weight", "emaciated", "thinning", "weak muscles",
            "karshya", "vajan ghatna", "shrinking muscles", "cachexia"
        ]
    },

    # ----------------- Physical Signs (Tongue & Pulse) -----------------
    "tongue_thick_white_coating": {
        "label": "Thick white or pasty tongue coating (sign of metabolic toxins/Ama)",
        "category": "Physical Signs",
        "keywords": [
            "white tongue", "coated tongue", "furry tongue", "pasty tongue", "white coating",
            "jibha par safed parat", "coated white"
        ]
    },
    "tongue_red_yellow_coating": {
        "label": "Red tongue body with yellowish or bitter coating (Pitta heat)",
        "category": "Physical Signs",
        "keywords": ["yellow coating tongue", "red tongue", "yellow tongue", "pitta tongue"]
    },
    "tongue_dry_rough_cracked": {
        "label": "Dry, rough, or fissured cracked tongue (Vata dehydration)",
        "category": "Physical Signs",
        "keywords": ["dry tongue", "rough tongue", "cracked tongue", "fissured tongue"]
    },
    "tongue_pale_thick_white_coating": {
        "label": "Pale, puffy tongue with thick white coating (Kapha/Ama)",
        "category": "Physical Signs",
        "keywords": ["pale tongue", "puffy tongue", "pale coated tongue"]
    },
    "nadi_sarpa_gati_cobra": {
        "label": "Rapid, irregular, slithering snake-like pulse (Vata pulse)",
        "category": "Physical Signs",
        "keywords": ["snake pulse", "cobra pulse", "sarpa gati", "irregular pulse"]
    },
    "nadi_manduka_gati_frog": {
        "label": "Bounding, hot, hopping frog-like pulse (Pitta pulse)",
        "category": "Physical Signs",
        "keywords": ["frog pulse", "jumping pulse", "manduka gati", "bounding pulse"]
    },
    "nadi_hamsa_gati_swan": {
        "label": "Slow, majestic, smooth swan-like pulse (Kapha pulse)",
        "category": "Physical Signs",
        "keywords": ["swan pulse", "slow pulse", "hamsa gati", "heavy pulse"]
    }
}

# Simple keyword map dictionary for backward compatibility
KEYWORD_MAP: Dict[str, List[str]] = {k: v["keywords"] for k, v in SYMPTOM_DEFINITIONS.items()}

# Frequency qualifiers
SOMETIMES_QUALIFIERS = [
    "sometimes", "occasionally", "mild", "mildly", "slight", "slightly",
    "comes and goes", "intermittent", "now and then", "on and off", "rarely",
    "kabhi kabhi", "halka", "thoda thoda", "kabhi kabhar", "occasional"
]

CONSTANT_QUALIFIERS = [
    "constant", "constantly", "severe", "severely", "always", "daily",
    "chronic", "intense", "every day", "every night", "unbearable", "sharp",
    "bahut", "bahut zyada", "har roz", "tez", "lagaataar", "persistent"
]

def get_symptom_label(symptom_id: str) -> str:
    """Returns a clear, human-readable display label for any clinical symptom ID."""
    if symptom_id in SYMPTOM_DEFINITIONS:
        return SYMPTOM_DEFINITIONS[symptom_id]["label"]
    return symptom_id.replace("_", " ").capitalize()

def get_symptoms_by_category() -> Dict[str, List[Tuple[str, str]]]:
    """Returns all symptoms grouped by human-friendly categories."""
    categories: Dict[str, List[Tuple[str, str]]] = {}
    for sym_id, data in SYMPTOM_DEFINITIONS.items():
        cat = data.get("category", "General & Systemic")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((sym_id, data["label"]))
    return categories

def extract_symptoms_with_frequency(text: str) -> Dict[str, str]:
    """Analyzes patient narrative text and extracts detected symptoms mapped to frequency.
    Returns: Dict[symptom_id, 'sometimes' | 'constant']
    """
    if not text or not text.strip():
        return {}

    text_lower = text.lower()
    results: Dict[str, str] = {}

    # Check whole text general tone
    has_global_sometimes = any(sq in text_lower for sq in SOMETIMES_QUALIFIERS)
    has_global_severe = any(cq in text_lower for cq in CONSTANT_QUALIFIERS)

    for sym_id, data in SYMPTOM_DEFINITIONS.items():
        keywords = data["keywords"]
        for kw in keywords:
            # Pattern match
            pattern = r"\b" + re.escape(kw) + r"\b"
            match = bool(re.search(pattern, text_lower))
            if not match and kw in text_lower:
                match = True
            
            if match:
                # Find local window of 40 characters around the match to detect local frequency
                start_pos = text_lower.find(kw)
                local_window = text_lower[max(0, start_pos - 40): min(len(text_lower), start_pos + len(kw) + 40)]
                
                # Check for negative qualifiers first (e.g., 'no fever', 'without headache')
                if re.search(r"\b(no|not|without|nahi|don't have)\s+" + re.escape(kw), local_window):
                    break  # Discard negated symptom
                    
                if any(sq in local_window for sq in SOMETIMES_QUALIFIERS):
                    results[sym_id] = "sometimes"
                elif any(cq in local_window for cq in CONSTANT_QUALIFIERS):
                    results[sym_id] = "constant"
                elif has_global_sometimes and not has_global_severe:
                    results[sym_id] = "sometimes"
                else:
                    results[sym_id] = "constant"
                break

    return results

def extract_symptoms_from_text(text: str) -> List[str]:
    """Backward compatible function returning list of detected symptom IDs."""
    return list(extract_symptoms_with_frequency(text).keys())

def extract_symptoms_with_ai(text: str, ai_consultant=None) -> Dict[str, str]:
    """Intelligently analyzes patient narrative using Gemini AI, mapping to symptom IDs and frequency.
    Falls back gracefully to comprehensive deterministic regex parser if AI is unavailable.
    Returns: Dict[symptom_id, 'sometimes' | 'constant']
    """
    if not text or not text.strip():
        return {}

    # Try AI-assisted extraction if configured
    if ai_consultant and hasattr(ai_consultant, "client") and ai_consultant.client:
        try:
            available_symptoms = {k: v["label"] for k, v in SYMPTOM_DEFINITIONS.items()}
            prompt = f"""You are an expert Ayurvedic clinical assistant.
Analyze the following patient's complaints and identify ALL matching symptoms from our known database.
For each matched symptom, assess whether the patient experiences it:
- 'sometimes' (intermittent, occasional, mild, comes and goes) OR
- 'constant' (persistent, daily, severe, chronic, frequent).

ALLOWED SYMPTOM DATABASE:
{json.dumps(available_symptoms, indent=2)}

PATIENT NARRATIVE:
"{text}"

INSTRUCTIONS:
1. ONLY return symptoms that the patient ACTUALLY suffers from. Do NOT include negated symptoms (e.g. "no fever", "no pain").
2. Output MUST be ONLY a valid JSON array of objects, with NO markdown formatting, NO backticks, and NO commentary.
Format:
[
  {{"symptom": "symptom_id", "frequency": "sometimes" | "constant"}}
]
"""
            models_to_try = [
                "gemini-2.5-flash",
                "gemini-flash-latest",
                "gemini-2.5-flash-lite",
                "gemini-flash-lite-latest",
                "gemini-2.5-pro"
            ]
            for m_name in models_to_try:
                try:
                    resp = ai_consultant.client.models.generate_content(
                        model=m_name,
                        contents=prompt
                    )
                    raw = resp.text.strip()
                    if raw.startswith("```"):
                        raw = re.sub(r"^```(?:json)?", "", raw).strip()
                    if raw.endswith("```"):
                        raw = re.sub(r"```$", "", raw).strip()
                    parsed = json.loads(raw)
                    if isinstance(parsed, list):
                        valid_dict = {}
                        for item in parsed:
                            if isinstance(item, dict):
                                s_id = item.get("symptom")
                                freq = item.get("frequency", "constant").lower()
                                if freq not in ["sometimes", "constant"]:
                                    freq = "constant"
                                if s_id in SYMPTOM_DEFINITIONS:
                                    valid_dict[s_id] = freq
                        if valid_dict:
                            return valid_dict
                    break
                except Exception:
                    continue
        except Exception:
            pass

    # Deterministic fallback
    return extract_symptoms_with_frequency(text)
