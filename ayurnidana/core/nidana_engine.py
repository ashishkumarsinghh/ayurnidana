"""Nidana Engine - Classical Ayurvedic Disease Recognition & Nidana Panchaka Builder.
Correlates presenting symptoms with 45+ classical disease profiles.
"""
from typing import List, Dict, Any, Tuple
from .models import (
    NidanaPanchaka, DiseaseDiagnosis, Prognosis, AmaStatus, AgniType, KoshthaType
)
from ..knowledge.classical_db import CLASSICAL_DISEASES

class NidanaEngine:
    """Systematically performs Roga Pariksha and constructs the Nidana Panchaka."""

    @staticmethod
    def diagnose(
        symptoms: List[str],
        vikriti_pattern: str,
        ama_status: AmaStatus,
        agni_status: AgniType,
        koshtha_status: KoshthaType,
        dhatu_involved: List[str],
        srotas_involved: List[str]
    ) -> DiseaseDiagnosis:
        
        matched_scores = {}
        symptom_set = set(symptoms)

        for dis_id, data in CLASSICAL_DISEASES.items():
            cardinal = set(data.get("cardinal_symptoms", []))
            overlap = cardinal.intersection(symptom_set)
            
            score = len(overlap) * 2.0
            
            # Primary dosha match boost
            primary_dosha = data.get("primary_dosha", "")
            if primary_dosha in vikriti_pattern:
                score += 3.0
                
            # Ama status match
            if data.get("requires_ama") and ama_status == AmaStatus.SAMA:
                score += 2.5
                
            matched_scores[dis_id] = score

        # Rank candidates
        ranked = sorted(matched_scores.items(), key=lambda x: x[1], reverse=True)
        top_id, top_score = ranked[0]
        primary_disease = CLASSICAL_DISEASES[top_id]
        
        secondary_conditions = []
        if len(ranked) > 1 and ranked[1][1] >= 3.0:
            secondary_conditions.append(CLASSICAL_DISEASES[ranked[1][0]]["name"])

        # Construct Nidana Panchaka
        np = NidanaPanchaka(
            nidana_etiology=primary_disease.get("nidana", [
                "Apathyakara Ahara (Irregular, incompatible, heavy food habits)",
                "Vishamashana and Ati-krichhra Vihara (Sedentary or excessively strenuous lifestyle)",
                "Vega Vidharana (Suppression of natural biological urges)"
            ]),
            purvarupa_prodromes=primary_disease.get("purvarupa", [
                "Alasya (Malaise and lethargy)",
                "Aruchi (Anorexia or taste disturbance)",
                "Gaurava (Heaviness in the torso and limbs)"
            ]),
            rupa_cardinal_symptoms=primary_disease.get("cardinal_symptoms", list(symptom_set)[:5]),
            upashaya_anupashaya=primary_disease.get("upashaya_anupashaya", {
                "Upashaya (Alleviating)": ["Ushna Ahara-Vihara (Warm, unctuous regimen)", "Deepana-Pachana herbs"],
                "Anupashaya (Aggravating)": ["Sheeta Ahara (Cold, raw foods)", "Divasvapna (Day sleeping)"]
            }),
            samprapti_pathogenesis=primary_disease.get("samprapti", {
                "Sanchaya": "Initial doshic accumulation in prime anatomical seat.",
                "Prakopa": "Aggravation due to persistent dietary & seasonal hetus.",
                "Prasara": "Systemic circulation of vitiated Doshas via circulatory channels.",
                "Sthana Samshraya": "Localization in vulnerable tissues (Khavaigunya).",
                "Vyakti": "Full manifestation of disease-specific signs and symptoms.",
                "Bheda": "Chronicity, tissue destruction, and complication stage."
            })
        )

        raw_prog = str(primary_disease.get("prognosis", ""))
        if "Sukha" in raw_prog:
            prognosis = Prognosis.SUKHA_SADHYA
        elif "Yapya" in raw_prog:
            prognosis = Prognosis.YAPYA
        elif "Pratyakhyeya" in raw_prog or "Asadhya" in raw_prog:
            prognosis = Prognosis.PRATYAKHYEYA
        else:
            prognosis = Prognosis.KRICHHRA_SADHYA

        reasoning = (
            f"The clinical presentation strongly aligns with {primary_disease['name']} ({primary_disease['sanskrit_name']}). "
            f"Key presenting features ({', '.join(list(symptom_set)[:4])}) correspond with classical pathology described in {primary_disease.get('classical_source', 'Charaka Samhita')}. "
            f"The patient exhibits {vikriti_pattern} with {ama_status.value} and {agni_status.value}. "
            f"Dhatu involvement is prominent in {', '.join(dhatu_involved[:2])} manifesting via {', '.join(srotas_involved[:2])}."
        )

        return DiseaseDiagnosis(
            primary_condition=primary_disease["name"],
            sanskrit_name=primary_disease["sanskrit_name"],
            doshic_subtype=primary_disease.get("doshic_subtype", "Vata-Kapha Pradhana"),
            secondary_conditions=secondary_conditions,
            dhatu_involved=dhatu_involved,
            srotas_involved=srotas_involved,
            ama_status=ama_status,
            agni_status=agni_status,
            koshtha_status=koshtha_status,
            prognosis=prognosis,
            nidana_panchaka=np,
            clinical_reasoning=reasoning,
            classical_citations=primary_disease.get("citations", [
                "Charaka Samhita, Chikitsasthana",
                "Madhava Nidana, Rogavinishchaya",
                "Ashtanga Hridaya, Nidanasthana"
            ])
        )
