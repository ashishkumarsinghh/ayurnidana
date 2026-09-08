"""Prescription and Clinical Case Sheet Report Generator."""
from typing import Dict, Any
from ...core.models import ClinicalCase

def generate_markdown_case_sheet(case: ClinicalCase) -> str:
    p = case.patient
    d = case.diagnosis
    t = case.treatment
    
    lines = [
        "# AYURNIDANA CLINICAL CASE SHEET & PRESCRIPTION",
        "**Ayurvedic Diagnostic and Systemic Treatment Record**",
        "---",
        f"**Patient Name:** {p.name} | **Age/Gender:** {p.age} yrs / {p.gender.value} | **Season:** {p.current_season}",
        f"**Chief Complaints:** {', '.join(case.chief_complaints)}",
        f"**Onset & Duration:** {case.onset_and_duration}",
        "",
        "## I. ASHTA STHANA & ROGI PARIKSHA",
        f"- **Nadi (Pulse):** {case.ashta_sthana.nadi_pulse}",
        f"- **Jihva (Tongue):** {case.ashta_sthana.jihva_tongue}",
        f"- **Mala (Stool):** {case.ashta_sthana.mala_stool}",
        f"- **Mutra (Urine):** {case.ashta_sthana.mutra_urine}",
        f"- **Sparsha (Skin):** {case.ashta_sthana.sparsha_skin}",
        f"- **Druk (Eyes):** {case.ashta_sthana.druk_eyes}",
        f"- **Agni / Koshtha:** {d.agni_status.value} / {d.koshtha_status.value}",
        f"- **Ama Status:** {d.ama_status.value}",
        "",
        "## II. ROGA NIDANA (DIAGNOSIS)",
        f"### **Primary Condition:** {d.primary_condition} ({d.sanskrit_name})",
        f"- **Doshic Pattern:** {d.doshic_subtype} (V: {case.dosha_scores.get('Vata')}%, P: {case.dosha_scores.get('Pitta')}%, K: {case.dosha_scores.get('Kapha')}%)",
        f"- **Dhatus Involved:** {', '.join(d.dhatu_involved)}",
        f"- **Srotas Involved:** {', '.join(d.srotas_involved)}",
        f"- **Prognosis (Sadhya-Asadhyata):** {d.prognosis.value}",
        "",
        "### **Nidana Panchaka Summary:**",
        f"- **Hetu (Etiology):** {'; '.join(d.nidana_panchaka.nidana_etiology[:3])}",
        f"- **Purvarupa (Prodromes):** {'; '.join(d.nidana_panchaka.purvarupa_prodromes[:3])}",
        f"- **Rupa (Cardinal Signs):** {'; '.join(d.nidana_panchaka.rupa_cardinal_symptoms[:4])}",
        "",
        "## III. CHIKITSA PLAN (TREATMENT BLUEPRINT)",
        "### 1. Deepana & Pachana (Metabolic Kindling):"
    ]

    for dp in t.deepana_pachana_protocol:
        lines.append(f"- {dp}")

    lines.append("\n### 2. Shamana Formulations (Prescription):")
    lines.append("| Drug Name | Form | Dosage | Anupana (Vehicle) | Kala (Timing) | Duration |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for f in t.shamana_formulations:
        lines.append(f"| **{f.name}** | {f.category} | {f.dosage} | {f.anupana_vehicle} | {f.aushadha_sevana_kala} | {f.duration_weeks} wks |")

    lines.append("\n### 3. Panchakarma Guidance:")
    lines.append(f"- **Eligibility:** {'Eligible' if t.panchakarma_guidance.eligible else 'Contraindicated / Deferred'}")
    lines.append(f"- **Therapy:** {t.panchakarma_guidance.recommended_therapy}")
    lines.append(f"- **Rationale:** {t.panchakarma_guidance.reasoning}")

    lines.append("\n### 4. Pathya - Apathya (Diet & Lifestyle):")
    lines.append(f"- **Wholesome Foods (Pathya Ahara):** {'; '.join(t.dietary_and_lifestyle_regimen.pathya_ahara_wholesome_diet[:4])}")
    lines.append(f"- **Foods to Avoid (Apathya Ahara):** {'; '.join(t.dietary_and_lifestyle_regimen.apathya_ahara_unwholesome_diet[:4])}")
    lines.append(f"- **Viruddha Ahara Warnings:** {'; '.join(t.dietary_and_lifestyle_regimen.viruddha_ahara_warnings[:2])}")
    lines.append(f"- **Yoga & Pranayama:** {'; '.join(t.dietary_and_lifestyle_regimen.yoga_and_pranayama)}")

    if t.red_flag_warnings:
        lines.append("\n### 5. Modern Red Flags & Emergency Precautions:")
        for rf in t.red_flag_warnings:
            lines.append(f"- [!] {rf}")

    lines.append(f"\n**Follow-up:** {t.follow_up_recommendation}")
    lines.append("\n*Certified Classical Ayurvedic System - AyurNidana*")
    return "\n".join(lines)
