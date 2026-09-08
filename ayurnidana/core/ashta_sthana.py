"""Ashta Sthana Pariksha - Eight-Fold Ayurvedic Clinical Examination System.
Based on Yogaratnakara and classical treatises.
"""
from typing import Dict, Any, List
from .models import AshtaSthanaPariksha

ASHTA_STHANA_CATALOG = {
    "nadi": {
        "title": "Nadi Pariksha (Radial Pulse Examination)",
        "classical_ref": "Yogaratnakara - Rogi Pariksha Vidhi",
        "description": "Assessment of pulse velocity, rhythm, tension, and volume under index, middle, and ring fingers.",
        "options": [
            ("Sarpa Gati (Serpentine / Quick / Light / Thread-like) - Vata Pradhana", "Vata"),
            ("Manduka Gati (Frog-like / Bounding / Sharp / Rapid) - Pitta Pradhana", "Pitta"),
            ("Hamsa Gati (Swan-like / Slow / Broad / Heavy / Deep) - Kapha Pradhana", "Kapha"),
            ("Sarpa-Manduka Gati (Mixed Irregular-Jumping Pulse) - Vata-Pitta", "Vata-Pitta"),
            ("Manduka-Hamsa Gati (Bounding yet Heavy Pulse) - Pitta-Kapha", "Pitta-Kapha"),
            ("Sannipataja Nadi (Tremulous, erratic, shifting between fingers)", "Sannipata")
        ]
    },
    "jihva": {
        "title": "Jihva Pariksha (Tongue Examination)",
        "classical_ref": "Sushruta Samhita & Yogaratnakara",
        "description": "Evaluation of lingual coating, color, texture, moisture, and papillae.",
        "options": [
            ("Dry, rough, dark/brownish coating with central fissures - Vataja", "Vata"),
            ("Red margins, prominent inflamed papillae, yellow/greenish central coat - Pittaja", "Pitta"),
            ("Pale, swollen, teeth impressions on lateral borders, thick white slimy coating - Kaphaja/Sama", "Kapha"),
            ("Heavy greasy white coat over whole tongue (Severe Ama) - Sama Jihva", "Ama"),
            ("Clean, pink, moist, flexible without coating - Nirama / Prakrita", "Balanced")
        ]
    },
    "mutra": {
        "title": "Mutra Pariksha (Urine Examination)",
        "classical_ref": "Bhavaprakasha & Yogaratnakara Taila Bindu Pariksha",
        "description": "Analysis of morning urine color, transparency, odor, and dispersion.",
        "options": [
            ("Pale, clear, scanty, frequent with slight astringency - Vataja", "Vata"),
            ("Deep yellow, reddish, warm with burning sensation on micturition - Pittaja", "Pitta"),
            ("Cloudy, milky, frothy with heavy sediment - Kaphaja", "Kapha"),
            ("Normal clear straw color, free flow, non-burning - Prakrita", "Balanced")
        ]
    },
    "mala": {
        "title": "Mala Pariksha (Stool Examination & Ama Float Test)",
        "classical_ref": "Charaka Samhita Chikitsasthana 15",
        "description": "Jala Nimajjana Pariksha: assessing buoyancy, consistency, odor, and transit.",
        "options": [
            ("Dry, hard, dark, scybalous, painful evacuation (Krura Koshtha) - Vataja", "Vata"),
            ("Loose, yellowish, foul-smelling with anal burning (Mridu Koshtha) - Pittaja", "Pitta"),
            ("Pale, heavy, sticky with mucus, sinks in water (Sama Mala) - Kaphaja / Sama", "Kapha"),
            ("Well-formed, floats easily in water, cleanses without effort - Nirama Pakwa", "Balanced")
        ]
    },
    "shabda": {
        "title": "Shabda Pariksha (Voice & Internal Sounds)",
        "classical_ref": "Yogaratnakara",
        "description": "Phonation tone, volume, cadence, borborygmi, and respiratory stridor.",
        "options": [
            ("Hoarse, broken, feeble, rapid, dry raspy voice - Vataja", "Vata"),
            ("Sharp, loud, impatient, high-pitched, penetrating voice - Pittaja", "Pitta"),
            ("Deep, resonant, heavy, slow, mucous gurgling sound - Kaphaja", "Kapha"),
            ("Clear, resonant, steady, and melodious - Prakrita", "Balanced")
        ]
    },
    "sparsha": {
        "title": "Sparsha Pariksha (Skin & Tactile Quality)",
        "classical_ref": "Charaka Samhita Vimanasthana 8",
        "description": "Cutaneous temperature, texture, moisture, turgor, and sensibility.",
        "options": [
            ("Cold, dry, rough, scaling, hypothermic extremities - Vataja", "Vata"),
            ("Warm/hot, flushed, excessive diaphoresis, tender, burning - Pittaja", "Pitta"),
            ("Cool, moist, oily, smooth, thick, doughy - Kaphaja", "Kapha"),
            ("Normal warmth, supple, uniform hydration - Prakrita", "Balanced")
        ]
    },
    "druk": {
        "title": "Druk Pariksha (Ocular & Visual Examination)",
        "classical_ref": "Sushruta Samhita Uttaratantra",
        "description": "Scleral hue, luster, conjunctival vascularity, lacrimation, and palpebral edema.",
        "options": [
            ("Dry, dull, lusterless, sunken eyes, frequent involuntary blinking - Vataja", "Vata"),
            ("Red, burning, photophobic, icteric/yellow sclera - Pittaja", "Pitta"),
            ("Puffy eyelids, excessive unctuous tearing, white sclera, thick lashes - Kaphaja", "Kapha"),
            ("Clear, lustrous, steady gaze with healthy conjunctiva - Prakrita", "Balanced")
        ]
    },
    "akruti": {
        "title": "Akruti Pariksha (Physical Habitus & Facies)",
        "classical_ref": "Charaka Samhita Indriyasthana",
        "description": "Somatic constitution, skeletal geometry, posture, and locomotive gait.",
        "options": [
            ("Ectomorphic, thin, prominent veins & tendons, restless gait - Vataja", "Vata"),
            ("Mesomorphic, moderate build, symmetrical musculature, purposeful gait - Pittaja", "Pitta"),
            ("Endomorphic, broad frame, heavy adipose/muscle, slow deliberate gait - Kaphaja", "Kapha"),
            ("Symmetrical, proportionate, balanced posture and vitality - Sama", "Balanced")
        ]
    }
}

class AshtaSthanaEvaluator:
    @staticmethod
    def evaluate(findings: AshtaSthanaPariksha) -> Dict[str, Any]:
        doshic_weights = {"Vata": 0.0, "Pitta": 0.0, "Kapha": 0.0}
        highlights = []

        all_text = f"{findings.nadi_pulse} {findings.jihva_tongue} {findings.mutra_urine} {findings.mala_stool} {findings.shabda_voice} {findings.sparsha_skin} {findings.druk_eyes} {findings.akruti_appearance}".lower()

        if "vata" in all_text or "sarpa" in all_text:
            doshic_weights["Vata"] += 3.0
        if "pitta" in all_text or "manduka" in all_text:
            doshic_weights["Pitta"] += 3.0
        if "kapha" in all_text or "hamsa" in all_text:
            doshic_weights["Kapha"] += 3.0

        if "ama" in all_text or "thick white" in all_text or "sinks" in all_text:
            highlights.append("Marked presence of Ama (endotoxin) detected across Jihva and Mala examinations.")
        if "sarpa-manduka" in all_text:
            highlights.append("Dvandvaja Nadi indicating dual Vata-Pitta provocation.")

        return {
            "weights": doshic_weights,
            "highlights": highlights,
            "pulse": findings.nadi_pulse,
            "tongue": findings.jihva_tongue,
            "stool": findings.mala_stool
        }
