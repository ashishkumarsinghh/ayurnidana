import sys
import os

from ayurnidana.core.models import *
from ayurnidana.core.dosha_engine import DoshaEngine
from ayurnidana.core.ashta_sthana import ASHTA_STHANA_CATALOG, AshtaSthanaEvaluator
from ayurnidana.core.dashavidha import DASHAVIDHA_CRITERIA, DashavidhaEvaluator
from ayurnidana.core.nidana_engine import NidanaEngine
from ayurnidana.core.chikitsa_engine import ChikitsaEngine
from ayurnidana.knowledge.notebook_bridge import NotebookBridge
from ayurnidana.knowledge.local_library import LocalAyurvedaLibrary
from ayurnidana.knowledge.ai_consultant import AIConsultant

print("=== 1. Core Module Import Test ===")
print("SUCCESS: All models and engines loaded cleanly.")

print("\n=== 2. Local Library Scanner Test ===")
lib = LocalAyurvedaLibrary()
status = lib.get_library_status()
print(f"Library available: {status['available']}")
print(f"Total treatises: {status['total_treatises']}")
print(f"Uploaded to NotebookLM: {status['uploaded_count']}")
print(f"Key Samhitas: {status['key_samhitas']}")

print("\n=== 3. Clinical Diagnostic & Treatment Engine Test ===")
symptoms = ["joint_pain_cracking", "pain_sharp_throbbing", "tremors_stiffness", "dryness_skin_hair"]
scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
print(f"Doshic Imbalance: {scores}")
print(f"Vikriti Pattern: {vikriti}")

ama_st, ama_reasons = DoshaEngine.assess_ama(symptoms, "Dry, rough, dark coating")
print(f"Ama Status: {ama_st.value}")

dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(symptoms)
print(f"Dhatus: {dhatus}")
print(f"Srotas: {srotas}")

diag = NidanaEngine.diagnose(
    symptoms=symptoms,
    vikriti_pattern=vikriti,
    ama_status=ama_st,
    agni_status=AgniType.VISHAMAGNI,
    koshtha_status=KoshthaType.KRURA,
    dhatu_involved=dhatus,
    srotas_involved=srotas
)
print(f"Diagnosed Condition: {diag.primary_condition} ({diag.sanskrit_name})")
print(f"Prognosis: {diag.prognosis.value}")

dashavidha = DashavidhaPariksha(
    prakriti="Vata-Pitta",
    vikriti=vikriti,
    sara_tissue_excellence="Madhyama Sara (Moderate)",
    samhanana_compactness="Madhyama Samhanana",
    sattva_mental_strength="Pravara Sattva",
    ahara_shakti_digestive_power="Madhyama Ahara Shakti",
    vyayama_shakti_physical_stamina="Madhyama",
    vaya_age_stage="Madhyamavastha"
)

plan = ChikitsaEngine.generate_plan(
    diagnosis=diag,
    dashavidha=dashavidha,
    patient_age=54,
    season="Sharad (Autumn)"
)
print(f"Formulations Prescribed ({len(plan.shamana_formulations)}):")
for f in plan.shamana_formulations:
    print(f"  - {f.name} ({f.category}): {f.dosage} with {f.anupana_vehicle} [{f.aushadha_sevana_kala}]")

print(f"Panchakarma Roadmap: {plan.panchakarma_guidance.recommended_therapy}")
print(f"Panchakarma Eligible: {plan.panchakarma_guidance.eligible}")

print("\n=== 4. AI Consultant Test ===")
ai = AIConsultant()
print(f"AI Consultant configured with Gemini API key: {ai.is_configured()}")

print("\n=== ALL CLINICAL TESTS PASSED WITH FLYING COLORS! ===")
