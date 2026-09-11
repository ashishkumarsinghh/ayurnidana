"""Nidana Engine - Classical Ayurvedic Disease Recognition & Nidana Panchaka Builder.
Correlates presenting symptoms with 45+ classical disease profiles.
"""
from typing import List, Dict, Any, Tuple, Union
from .knowledge_base import ALLOPATHIC_MAPPING
from .models import (
    NidanaPanchaka, DiseaseDiagnosis, Prognosis, AmaStatus, AgniType, KoshthaType
)
from ..knowledge.classical_db import CLASSICAL_DISEASES

class NidanaEngine:
    """Systematically performs Roga Pariksha and constructs the Nidana Panchaka."""

    @staticmethod
    def diagnose(
        symptoms: Union[List[str], Dict[str, Any]],
        vikriti_pattern: str,
        ama_status: AmaStatus,
        agni_status: AgniType,
        koshtha_status: KoshthaType,
        dhatu_involved: List[str],
        srotas_involved: List[str],
        age: int = 35,
        comorbidities: str = ""
    ) -> DiseaseDiagnosis:
        
        matched_scores = {}
        if isinstance(symptoms, dict):
            symptom_map = symptoms
            symptom_set = set(symptoms.keys())
        else:
            symptom_map = {s: "constant" for s in symptoms}
            symptom_set = set(symptoms)

        for dis_id, data in CLASSICAL_DISEASES.items():
            cardinal = set(data.get("cardinal_symptoms", []))
            overlap = cardinal.intersection(symptom_set)
            
            if not overlap:
                matched_scores[dis_id] = 0.0
                continue

            # Base score: each cardinal symptom matched is 3.0 points with frequency weight
            score = 0.0
            for s in overlap:
                freq = str(symptom_map.get(s, "constant")).lower()
                weight = 0.7 if freq in ["sometimes", "mild", "occasional"] else 1.2 if freq in ["constant", "severe", "frequent"] else 1.0
                score += 3.0 * weight
            
            # Primary dosha match boost
            primary_doshas = [d.strip() for d in data.get("primary_dosha", "").replace("&", ",").replace("/", ",").split(",") if d.strip()]
            if any(d in vikriti_pattern for d in primary_doshas):
                score += 3.0
                
            # Ama status clinical differentiation
            if data.get("requires_ama"):
                if ama_status == AmaStatus.SAMA:
                    score += 4.0
                elif ama_status == AmaStatus.MILD_AMA:
                    score += 1.5
                elif ama_status == AmaStatus.NIRAMA:
                    score -= 3.0  # Strong penalty: Amavata cannot be diagnosed without Ama
            else:
                if dis_id == "sandhivata" and ama_status == AmaStatus.SAMA:
                    score -= 2.0  # Sandhivata is Nirama Vata; if high Ama is present, favor Amavata
                    
            # Srotas alignment boost
            dis_srotas = set(data.get("srotas", []))
            if dis_srotas.intersection(set(srotas_involved)):
                score += 2.0
                
            matched_scores[dis_id] = max(0.0, score)

        # Rank candidates
        ranked = sorted(matched_scores.items(), key=lambda x: x[1], reverse=True)
        top_id, top_score = ranked[0]
        
        secondary_conditions = []
        for cand_id, cand_score in ranked[1:4]:
            if cand_score >= 3.0 and cand_id != top_id:
                secondary_conditions.append(CLASSICAL_DISEASES[cand_id]["name"])

        if top_score >= 3.0:
            # High-confidence match with a canonical Brihat Trayi disease
            primary_disease = CLASSICAL_DISEASES[top_id]
            primary_name = primary_disease["name"]
            sanskrit_name = primary_disease["sanskrit_name"]
            doshic_subtype = primary_disease.get("doshic_subtype", vikriti_pattern)
            citations = primary_disease.get("citations", [
                "Charaka Samhita, Chikitsasthana",
                "Madhava Nidana, Rogavinishchaya",
                "Ashtanga Hridaya, Nidanasthana"
            ])
            nidana_list = primary_disease.get("nidana", [
                "Apathyakara Ahara (Irregular, incompatible, heavy food habits)",
                "Vishamashana and Ati-krichhra Vihara (Sedentary or excessively strenuous lifestyle)",
                "Vega Vidharana (Suppression of natural biological urges)"
            ])
            purvarupa_list = primary_disease.get("purvarupa", [
                "Alasya (Malaise and lethargy)",
                "Aruchi (Anorexia or taste disturbance)",
                "Gaurava (Heaviness in the torso and limbs)"
            ])
            rupa_list = primary_disease.get("cardinal_symptoms", list(symptom_set)[:5])
            upashaya_dict = primary_disease.get("upashaya_anupashaya", {
                "Upashaya (Alleviating)": ["Ushna Ahara-Vihara (Warm, unctuous regimen)", "Deepana-Pachana herbs"],
                "Anupashaya (Aggravating)": ["Sheeta Ahara (Cold, raw foods)", "Divasvapna (Day sleeping)"]
            })
            samprapti_dict = primary_disease.get("samprapti", {
                "1_sanchaya": "Initial doshic accumulation in prime anatomical seat.",
                "2_prakopa": "Aggravation due to persistent dietary & seasonal hetus.",
                "3_prasara": "Systemic circulation of vitiated Doshas via circulatory channels.",
                "4_sthana_samshraya": "Localization in vulnerable tissues (Khavaigunya).",
                "5_vyakti": "Full manifestation of disease-specific signs and symptoms.",
                "6_bheda": "Chronicity, tissue destruction, and complication stage."
            })
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
                f"The clinical presentation strongly aligns with {primary_name} ({sanskrit_name}). "
                f"Key presenting features ({', '.join(list(symptom_set)[:4])}) correspond with classical pathology described in {primary_disease.get('classical_source', 'Charaka Samhita')}. "
                f"The patient exhibits {vikriti_pattern} with {ama_status.value} and {agni_status.value}. "
                f"Dhatu involvement is prominent in {', '.join(dhatu_involved[:2])} manifesting via {', '.join(srotas_involved[:2])}."
            )
        else:
            # Universal Classical Doshic-Srotas Syndromic Diagnosis
            # Grounded in Charaka Samhita Sutrasthana 18:44-46
            clean_pattern = vikriti_pattern.split("(")[0].strip()
            primary_dhatu = dhatu_involved[0] if dhatu_involved else "Rasa Dhatu"
            primary_srotas = srotas_involved[0] if srotas_involved else "Annavaha Srotas"

            dhatu_prefix = "Dhatu-Pradoshaja"
            if "Rasa" in primary_dhatu: dhatu_prefix = "Rasapradoshaja (रसप्रदोषज)"
            elif "Rakta" in primary_dhatu: dhatu_prefix = "Raktapradoshaja (रक्तप्रदोषज)"
            elif "Mamsa" in primary_dhatu: dhatu_prefix = "Mamsapradoshaja (मांसप्रदोषज)"
            elif "Meda" in primary_dhatu: dhatu_prefix = "Medopradoshaja (मेदःप्रदोषज)"
            elif "Shukra" in primary_dhatu: dhatu_prefix = "Shukrapradoshaja (शुक्रप्रदोषज)"
            elif "Asthi" in primary_dhatu: dhatu_prefix = "Asthipradoshaja (अस्थिप्रदोषज)"
            elif "Majja" in primary_dhatu: dhatu_prefix = "Majjapradoshaja (मज्जाप्रदोषज)"

            primary_name = f"Syndromic Doshic-Srotas Imbalance ({clean_pattern})"
            sanskrit_name = f"{dhatu_prefix} विकार ({clean_pattern})"
            doshic_subtype = vikriti_pattern
            prognosis = Prognosis.KRICHHRA_SADHYA if ama_status == AmaStatus.SAMA else Prognosis.SUKHA_SADHYA
            citations = [
                "Charaka Samhita Sutrasthana 18/44-46 (Axiom: Nahi Sarve Vikaranam Namato'sti Vinishchayah)",
                "Charaka Samhita Vimanasthana 5 (Srotas Vimanadhyaya)",
                "Ashtanga Hridaya Sutrasthana 12 (Doshabhediya Adhyaya)"
            ]
            nidana_list = [
                "Dosha-Hetu Sevana: Diet and habits aggravating the predominant biological humors",
                "Vishamashana: Irregular, conflicting meal timing impairing Agni",
                "Vega-Dharana: Suppression of biological natural reflexes (sleep, voiding, breath)"
            ]
            purvarupa_list = [
                "Alasya and Aruchi (Subtle heaviness and loss of appetite)",
                "Dhatu-Shaithilya (Early systemic fatigue and tissue laxity)"
            ]
            rupa_list = list(symptom_set) if symptom_set else ["Generalized systemic malaise"]
            upashaya_dict = {
                "Upashaya (Alleviating)": ["Deepana-Pachana diet", "Restorative sleep", "Warm hydration"],
                "Anupashaya (Aggravating)": ["Incompatible foods (Viruddha Ahara)", "Cold drafts", "Mental stress"]
            }
            samprapti_dict = {
                "1_sanchaya": f"{clean_pattern} accumulates in primary sites due to dietary errors.",
                "2_prakopa": f"Aggravation occurs, overflowing into micro-circulation with {ama_status.value}.",
                "3_prasara": f"Systemic circulation through {primary_srotas}.",
                "4_sthana_samshraya": f"Localization (Khavaigunya) into {primary_dhatu}.",
                "5_vyakti": f"Eruption of characteristic complaints: {', '.join(list(symptom_set)[:3])}.",
                "6_bheda": "Structural tissue chronicity unless halted by classical Chikitsa."
            }
            reasoning = (
                f"Presenting symptoms ({', '.join(list(symptom_set)[:4])}) manifest as a multi-system complex. "
                f"Per Charaka Samhita Sutrasthana 18:44-46, clinical diagnosis is formulated on the fundamental triad of "
                f"Dosha ({vikriti_pattern}), Dhatu ({', '.join(dhatu_involved[:2])}), and Srotas ({', '.join(srotas_involved[:2])}). "
                f"Metabolic state is {ama_status.value} with {agni_status.value} and {koshtha_status.value} Koshtha."
            )

        # Construct Nidana Panchaka
        np = NidanaPanchaka(
            nidana_etiology=nidana_list,
            purvarupa_prodromes=purvarupa_list,
            rupa_cardinal_symptoms=rupa_list,
            upashaya_anupashaya=upashaya_dict,
            samprapti_pathogenesis=samprapti_dict
        )

        
        # Inject Allopathic Mapping
        mapped_precautions = []
        if comorbidities:
            reasoning += f" Comorbidities noted: {comorbidities}."
            for term, data in ALLOPATHIC_MAPPING.items():
                if term.lower() in comorbidities.lower():
                    reasoning += f" Patient has {term.title()} ({data['ayurvedic_correlation']}), mapped to pathology: {data['pathology']}."
                    mapped_precautions.extend(data['treatment_precautions'])
                    
        # Append precautions to purvarupa to forcibly push it into the AI's generation context if needed.
        if mapped_precautions:
            np.upashaya_anupashaya["Anupashaya (Aggravating)"] = list(set(np.upashaya_anupashaya.get("Anupashaya (Aggravating)", []) + mapped_precautions))

        return DiseaseDiagnosis(
            primary_condition=primary_name,
            sanskrit_name=sanskrit_name,
            doshic_subtype=doshic_subtype,
            secondary_conditions=secondary_conditions,
            dhatu_involved=dhatu_involved,
            srotas_involved=srotas_involved,
            ama_status=ama_status,
            agni_status=agni_status,
            koshtha_status=koshtha_status,
            prognosis=prognosis,
            nidana_panchaka=np,
            clinical_reasoning=reasoning,
            classical_citations=citations
        )
