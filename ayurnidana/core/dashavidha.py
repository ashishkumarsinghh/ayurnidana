"""Dashavidha Pariksha - Ten-fold Patient Examination System.
Source: Charaka Samhita Vimanasthana Adhyaya 8.
"""
from typing import Dict, Any, List
from .models import DashavidhaPariksha, AgniType, KoshthaType

DASHAVIDHA_CRITERIA = {
    "sara": {
        "title": "Sara Pariksha (Tissue Excellence / Dhatu Vitality)",
        "description": "Evaluation of constitutional purity and functional reserves of the 7 Dhatus and Satva.",
        "options": [
            "Pravara Sara (Superior Vitality / High Tissue Strength)",
            "Madhyama Sara (Moderate Tissue Reserve)",
            "Avara Sara (Deficient / Vulnerable Tissue Tone)"
        ]
    },
    "samhanana": {
        "title": "Samhanana Pariksha (Body Compactness & Skeletal Integrity)",
        "description": "Firmness of bone junctions, ligamentous symmetry, and musculoskeletal alignment.",
        "options": [
            "Su-samhata (Well-compacted, dense, robust skeletal frame)",
            "Madhyama Samhanana (Moderately compacted frame)",
            "Hina Samhanana (Loose joint architecture, low bone density, fragile)"
        ]
    },
    "pramana": {
        "title": "Pramana Pariksha (Anthropometric Proportions / Anguli Pramana)",
        "options": [
            "Yathokta Pramana (Classical anatomical symmetry and proportion)",
            "Ati-Sthula (Excessive adipose tissue / hyper-proportioned)",
            "Ati-Krisha (Severe cachexia / sub-normal proportions)"
        ]
    },
    "satmya": {
        "title": "Satmya Pariksha (Dietary & Environmental Adaptability)",
        "options": [
            "Pravara Satmya (Adapted to all 6 tastes, changes in climate and food)",
            "Madhyama Satmya (Moderate dietary adaptability)",
            "Avara / Eka-rasa Satmya (Fragile, allergic, adapted to only 1-2 tastes)"
        ]
    },
    "sattva": {
        "title": "Sattva Pariksha (Psychological Resilience & Mental Tenacity)",
        "options": [
            "Pravara Sattva (High emotional resilience, tolerance to pain and adversity)",
            "Madhyama Sattva (Average emotional tolerance, requires reassurance)",
            "Avara / Heena Sattva (Low pain threshold, prone to acute panic, grief, anxiety)"
        ]
    },
    "ahara_shakti": {
        "title": "Ahara Shakti (Digestive Capacity - Abhyavaharana & Jarana Shakti)",
        "options": [
            "Pravara Ahara Shakti (Strong ingestion and rapid, complete digestion - Samagni/Tikshnagni)",
            "Madhyama Ahara Shakti (Moderate ingestion and steady digestion)",
            "Avara Ahara Shakti (Poor appetite, sluggish digestion, post-prandial distress - Mandagni)"
        ]
    },
    "vyayama_shakti": {
        "title": "Vyayama Shakti (Physical Stamina & Exercise Tolerance)",
        "options": [
            "Pravara (Capable of intense sustained physical exertion without undue dyspnea)",
            "Madhyama (Moderate physical tolerance)",
            "Avara (Fatigues rapidly with minimal effort, early breathlessness)"
        ]
    },
    "vaya": {
        "title": "Vaya Pariksha (Chronological & Biological Age Stage)",
        "options": [
            "Balyavastha (Childhood / Growth stage up to 16-20 yrs - Kapha dominant)",
            "Madhyamavastha (Youth & Adulthood 20-60 yrs - Pitta dominant)",
            "Vriddhavastha (Geriatric stage >60 yrs - Vata dominant)"
        ]
    }
}

class DashavidhaEvaluator:
    @staticmethod
    def evaluate_bala(findings: DashavidhaPariksha) -> Dict[str, Any]:
        """Evaluates Rogi Bala (patient constitutional strength) for treatment dosing."""
        score = 0
        
        if "Pravara" in findings.sara_tissue_excellence:
            score += 3
        elif "Madhyama" in findings.sara_tissue_excellence:
            score += 2
        else:
            score += 1

        if "Su-samhata" in findings.samhanana_compactness:
            score += 3
        elif "Madhyama" in findings.samhanana_compactness:
            score += 2
        else:
            score += 1

        if "Pravara" in findings.sattva_mental_strength:
            score += 3
        elif "Madhyama" in findings.sattva_mental_strength:
            score += 2
        else:
            score += 1

        if "Pravara" in findings.ahara_shakti_digestive_power:
            score += 3
        elif "Madhyama" in findings.ahara_shakti_digestive_power:
            score += 2
        else:
            score += 1

        if score >= 10:
            bala_grade = "Pravara Bala (Superior Patient Strength) - Eligible for Teekshna Shodhana"
            eligible_for_panchakarma = True
        elif score >= 6:
            bala_grade = "Madhyama Bala (Moderate Strength) - Eligible for Madhyama Shodhana & Shamana"
            eligible_for_panchakarma = True
        else:
            bala_grade = "Avara / Hina Bala (Frail / Low Strength) - Shodhana Contraindicated; Only Mridu Shamana"
            eligible_for_panchakarma = False

        return {
            "bala_score": score,
            "bala_grade": bala_grade,
            "panchakarma_eligible": eligible_for_panchakarma
        }
