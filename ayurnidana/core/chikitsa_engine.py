"""Chikitsa Engine - Multi-Tier Ayurvedic Systematic Treatment Protocol Generator.
Follows the classical dictum: 'Nidana Parivarjanam, Deepanam Pachanam Shodhanam Shamanam cha'.
"""
from typing import List, Dict, Any
from .models import (
    DiagnosisResult, TreatmentPlan, Formulation, PanchakarmaPrescription,
    PathyaApathya, AmaStatus, AgniType, KoshthaType, DashavidhaPariksha
)
from ..knowledge.classical_db import CLASSICAL_DISEASES

class ChikitsaEngine:
    """Constructs systematic, stage-wise Ayurvedic therapeutic prescriptions."""

    @staticmethod
    def generate_plan(
        diagnosis: DiagnosisResult,
        dashavidha: DashavidhaPariksha,
        patient_age: int,
        season: str
    ) -> TreatmentPlan:
        
        # 1. Fetch template or default classical data
        matched_disease = None
        for k, v in CLASSICAL_DISEASES.items():
            if v["name"].lower() in diagnosis.primary_condition.lower() or k in diagnosis.primary_condition.lower():
                matched_disease = v
                break

        if not matched_disease:
            # Fallback to sandhivata
            matched_disease = CLASSICAL_DISEASES["sandhivata"]

        # 2. Phase 1: Deepana & Pachana Protocol (Metabolic Preparation)
        deepana_protocol = []
        if diagnosis.ama_status == AmaStatus.SAMA:
            deepana_protocol = [
                "Strict Langhana / Laghu Ahara: Light warm mung bean gruel (Mudga Yusha) for 3-5 days.",
                "Shunthi (Dry ginger) + Dhanyaka (Coriander) boiled warm water as primary hydration.",
                "Chitrakadi Vati: 2 tablets twice daily 15 minutes before food with warm water (Charaka Chikitsa 15).",
                "Vaishwanara Churna: 3g with warm water before meals to stimulate Jatharagni and clear Srotas."
            ]
        elif diagnosis.ama_status == AmaStatus.MILD_AMA:
            deepana_protocol = [
                "Panchakola Churna 2g with warm water before lunch and dinner for 5 days.",
                "Ginger-lemon-rock salt appetizer: Fresh ginger slice with pinch of rock salt 10 mins before meals.",
                "Drinking water boiled with cumin and fennel seeds."
            ]
        else:
            deepana_protocol = [
                "Agnideepana: Shunthi Churna 1.5g with ghee/warm water before meals.",
                "Samagni Maintenance: Balanced six-taste meals at regular 4-hour intervals."
            ]

        # 3. Phase 2: Shamana Formulations
        raw_formulations = matched_disease.get("shamana_formulations", [])
        shamana_list = []
        for f in raw_formulations:
            shamana_list.append(Formulation(
                name=f["name"],
                category=f["category"],
                classical_indication=f["classical_indication"],
                dosage=f["dosage"],
                anupana_vehicle=f["anupana_vehicle"],
                aushadha_sevana_kala=f["aushadha_sevana_kala"],
                duration_weeks=f["duration_weeks"],
                classical_reference=f["classical_reference"]
            ))

        # 4. Phase 3: Panchakarma Guidance (Safety & Eligibility check)
        raw_pk = matched_disease.get("panchakarma", {})
        eligible = True
        contra_reasons = []

        # Check age contraindications
        if patient_age < 12 or patient_age > 75:
            eligible = False
            contra_reasons.append(f"Extreme of age ({patient_age} yrs) contraindicates radical Teekshna Shodhana (Balyavastha / Vriddhavastha).")

        # Check Ama contraindications (Shodhana during intense Ama causes Dhatu damage)
        if diagnosis.ama_status == AmaStatus.SAMA:
            eligible = False
            contra_reasons.append("Active presence of Sama state: Shodhana is contraindicated until Ama is digested (Pachana) first.")

        # Check Bala
        if "Avara" in dashavidha.sara_tissue_excellence or "Heena" in dashavidha.samhanana_compactness:
            eligible = False
            contra_reasons.append("Debilitated patient constitution (Hina Bala): Patient cannot tolerate radical Shodhana.")

        pk_prescription = PanchakarmaPrescription(
            eligible=eligible,
            recommended_therapy=raw_pk.get("recommended_therapy", "Mridu Shamana Only") if eligible else "Shodhana Deferred / Shamana Priority",
            reasoning=raw_pk.get("reasoning", "") if eligible else " ; ".join(contra_reasons),
            purvakarma=raw_pk.get("purvakarma", []) if eligible else ["Deepana-Pachana therapy for 7-10 days"],
            pradhanakarma=raw_pk.get("pradhanakarma", "N/A") if eligible else "N/A - Proceed with Gentle Shamana and Anulomana",
            paschatkarma=raw_pk.get("paschatkarma", []) if eligible else ["Follow light warm digestive diet"],
            contraindications_checked=contra_reasons
        )

        # 5. Phase 4: Pathya-Apathya Regimen
        pathya = PathyaApathya(
            pathya_ahara_wholesome_diet=matched_disease.get("pathya_ahara", [
                "Aged red rice (Shashtika Shali), barley, and wheat",
                "Mudga (green gram) and Kulattha (horsegram) soups",
                "Warm cooked seasonal vegetables with cow's A2 ghee"
            ]),
            apathya_ahara_unwholesome_diet=matched_disease.get("apathya_ahara", [
                "Refrigerated, cold, stale, or leftover foods",
                "Heavy, deep-fried snacks, and incompatible food combinations",
                "Excessive dry pulses, carbonated drinks, and refined flours"
            ]),
            pathya_vihara_recommended_lifestyle=matched_disease.get("pathya_vihara", [
                "Brahma Muhurta awakening (around dawn)",
                "Daily Abhyanga (warm oil application) suited to Doshic constitution",
                "Adequate restorative sleep by 10 PM"
            ]),
            apathya_vihara_contraindicated_habits=matched_disease.get("apathya_vihara", [
                "Day sleeping (Divasvapna) which vitiates Kapha and Pitta",
                "Suppression of natural biological urges (Adharaniya Vegas)",
                "Excessive late-night screen time and irregular schedules"
            ]),
            viruddha_ahara_warnings=[
                "Milk and Fish / Seafood (Samyoga Viruddha - causes severe Rakta & Kushtha disorders).",
                "Equal quantities of Honey and Ghee (Matra Viruddha - acts as toxic poison).",
                "Heated or cooked Honey in any form (Kala / Samskara Viruddha).",
                "Fruit consumed with Milk or Yoghurt (e.g. fruit smoothies / banana milkshakes).",
                "Cold iced water immediately following hot greasy meals (Krama Viruddha)."
            ],
            yoga_and_pranayama=matched_disease.get("yoga_pranayama", [
                "Surya Namaskara (Gentle, 4-6 cycles with breath awareness)",
                "Nadi Shodhana Pranayama (15 minutes twice daily)",
                "Bhramari Pranayama (To tranquilize Pranavaha & Manovaha Srotas)"
            ])
        )

        # 6. Phase 5: Rasayana Recovery Plan
        rasayana_plan = [
            "Chyawanprasha Avaleha: 1 teaspoon (10g) in early morning with warm milk for Ojas enhancement.",
            "Ashwagandha Churna 3g + Shatavari Churna 3g with warm milk at bedtime for Dhatu replenishment.",
            "Brahmi Rasayana or Medhya Rasayana for mental clarity and stress reduction."
        ]

        # 7. Phase 6: Red Flags / Modern Emergency Indicators
        red_flags = [
            "Severe unrelenting chest tightness, radiating pain to left arm, or acute shortness of breath (Requires immediate emergency cardiology evaluation).",
            "Acute severe abdominal pain with high fever, vomiting, and rigid abdomen (Acute surgical abdomen rule-out).",
            "Sudden focal neurological deficits: facial droop, arm weakness, slurred speech (Rule out CVA / Stroke - immediate emergency protocol).",
            "High intractable fever >103°F with neck stiffness or altered sensorium.",
            "Severe gastrointestinal bleeding (hematemesis or fresh melena stools)."
        ]

        return TreatmentPlan(
            deepana_pachana_protocol=deepana_protocol,
            shamana_formulations=shamana_list,
            panchakarma_guidance=pk_prescription,
            dietary_and_lifestyle_regimen=pathya,
            rasayana_recovery_plan=rasayana_plan,
            red_flag_warnings=red_flags,
            follow_up_recommendation="Review clinical response, tongue coating, and pulse after 14 days of Shamana."
        )
