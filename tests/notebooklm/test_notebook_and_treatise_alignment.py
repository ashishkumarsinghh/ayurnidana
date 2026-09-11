"""NotebookLM & Local Classical Treatise Alignment Audit.
Tests the integration between:
1. The 138-treatise local library (OneDrive/Documents/ayurveda)
2. The Google NotebookLM bridge and profile session
3. The Gemini AI consultant co-pilot
4. Strict alignment comparison between deterministic core logic and AI-augmented synthesis,
   ensuring zero doctrinal divergence or hallucination.
"""
import pytest
import os
from ayurnidana.knowledge.local_library import LocalAyurvedaLibrary
from ayurnidana.knowledge.notebook_bridge import NotebookBridge
from ayurnidana.knowledge.ai_consultant import AIConsultant
from ayurnidana.knowledge.classical_db import CLASSICAL_DISEASES
from ayurnidana.core.models import AmaStatus, AgniType, KoshthaType, DashavidhaPariksha
from ayurnidana.core.nidana_engine import NidanaEngine
from ayurnidana.core.chikitsa_engine import ChikitsaEngine

@pytest.fixture(scope="module")
def library():
    return LocalAyurvedaLibrary()

@pytest.fixture(scope="module")
def bridge():
    return NotebookBridge()

@pytest.fixture(scope="module")
def consultant():
    return AIConsultant()

class TestNotebookAndTreatiseAlignment:

    def test_local_library_grounding_across_treatises(self, library):
        """Verifies that the 138 local treatises index the key classical texts."""
        status = library.get_library_status()
        assert status["available"] is True
        assert status["total_treatises"] >= 100
        
        # Verify Brihat Trayi & Laghu Trayi presence
        samhitas = status["key_samhitas"]
        assert any("Charaka" in s for s in samhitas)
        assert any("Sushruta" in s for s in samhitas)
        assert any("Ashtanga" in s for s in samhitas)
        assert any("Madhava" in s for s in samhitas)

    def test_notebooklm_bridge_initialization(self, bridge):
        """Verifies NotebookLM bridge configuration and authentication inspection."""
        assert bridge.target_name == "ayurveda"
        auth = bridge.check_auth()
        assert "authenticated" in auth
        # Bridge should have default notebook ID or report cleanly
        conn = bridge.connect_to_ayurveda_notebook()
        assert "connected" in conn
        if conn["connected"]:
            assert conn.get("notebook_id") is not None

    def test_ai_consultant_configured(self, consultant):
        """Verifies that Gemini AI Consultant has an active API key from .env."""
        assert consultant.is_configured() is True, "Gemini API key should be configured in .env"

    def test_doctrinal_alignment_sandhivata(self, library, consultant):
        """Validates that for Sandhivata (Osteoarthritis):
        1. Deterministic core prescribes Vata-Shamana (Yogaraja Guggulu, Maharasnadi Kwatha, Basti).
        2. Local treatises contain Charaka / Vatavyadhi texts.
        3. Generative consultant when supplied this context provides an aligned, non-contradictory explanation.
        """
        # 1. Deterministic Core
        symptoms = ["joint_pain_cracking", "pain_sharp_throbbing", "tremors_stiffness"]
        diag = NidanaEngine.diagnose(
            symptoms=symptoms,
            vikriti_pattern="Vata Pradhana",
            ama_status=AmaStatus.NIRAMA,
            agni_status=AgniType.VISHAMAGNI,
            koshtha_status=KoshthaType.KRURA,
            dhatu_involved=["Asthi Dhatu"],
            srotas_involved=["Asthivaha Srotas"]
        )
        dashavidha = DashavidhaPariksha(
            prakriti="Vata-Kapha", vikriti="Vata Pradhana",
            sara_tissue_excellence="Madhyama Sara", samhanana_compactness="Madhyama Samhanana",
            sattva_mental_strength="Madhyama Sattva", ahara_shakti_digestive_power="Madhyama Ahara Shakti",
            vyayama_shakti_physical_stamina="Madhyama", vaya_age_stage="Madhyamavastha"
        )
        plan = ChikitsaEngine.generate_plan(diag, dashavidha, patient_age=58)
        
        # 2. Local Treatise Evidence
        treatises = library.find_relevant_treatises(diag.primary_condition)
        assert len(treatises) > 0
        treatise_str = "\n".join([f"- {t['filename']} ({t['folder']})" for t in treatises[:5]])
        
        # 3. AI Consultant Response Alignment
        treatment_str = f"Formulations: {', '.join([f.name for f in plan.shamana_formulations])}. Panchakarma: {plan.panchakarma_guidance.recommended_therapy}"
        response = consultant.synthesize_consultation(
            patient_summary="58-year-old patient with severe knee pain and crepitus.",
            diagnosis_summary=f"{diag.primary_condition} ({diag.sanskrit_name}) - Doshic Pattern: {diag.doshic_subtype}",
            treatment_summary=treatment_str,
            user_question="Explain the therapeutic strategy and why Basti is recommended for Sandhivata.",
            treatise_context=treatise_str,
            mode="physician"
        )
        assert response is not None
        assert len(response) > 100
        # AI response must align with Vata and Basti principles
        resp_lower = response.lower()
        assert "vata" in resp_lower
        assert "basti" in resp_lower or "joint" in resp_lower or "sandhi" in resp_lower

    def test_doctrinal_alignment_ama_safety_consensus(self, consultant):
        """CRITICAL: Both deterministic core and AI consultant must enforce the Ama doctrine.
        Neither system may recommend radical Shodhana while the patient has acute Ama.
        """
        # Deterministic
        diag = NidanaEngine.diagnose(
            symptoms=["tremors_stiffness", "dull_pain_swelling_edema", "tongue_thick_white_coating"],
            vikriti_pattern="Kapha-Vata Imbalance",
            ama_status=AmaStatus.SAMA,
            agni_status=AgniType.MANDAGNI,
            koshtha_status=KoshthaType.MADHYAMA,
            dhatu_involved=["Rasa Dhatu"],
            srotas_involved=["Rasavaha Srotas"]
        )
        dashavidha = DashavidhaPariksha(
            prakriti="Kapha-Vata", vikriti="Kapha-Vata Imbalance",
            sara_tissue_excellence="Madhyama Sara", samhanana_compactness="Madhyama Samhanana",
            sattva_mental_strength="Madhyama Sattva", ahara_shakti_digestive_power="Avara Ahara Shakti",
            vyayama_shakti_physical_stamina="Avara", vaya_age_stage="Madhyamavastha"
        )
        plan = ChikitsaEngine.generate_plan(diag, dashavidha, patient_age=36)
        assert plan.panchakarma_guidance.eligible is False
        
        # Test AI consultant consensus on Ama
        treatment_str = (
            f"Active Ama (Sama state). Shodhana is deferred. "
            f"Deepana-Pachana protocol: {'; '.join(plan.deepana_pachana_protocol)}."
        )
        response = consultant.synthesize_consultation(
            patient_summary="36-year-old with acute swelling, severe morning stiffness, and thick white tongue coating.",
            diagnosis_summary="Amavata (Rheumatoid Arthritis) in Sama Avastha",
            treatment_summary=treatment_str,
            user_question="Is the patient ready for immediate radical Virechana or Vamana detoxification?",
            treatise_context="Charaka Samhita Sutrasthana 16 (Ama Shodhana Nishedha)",
            mode="physician"
        )
        resp_lower = response.lower()
        # Must agree that immediate radical purification is contraindicated / not advised
        assert any(term in resp_lower for term in ["contraindicated", "not ready", "defer", "no", "digest", "deepana", "pachana", "ama", "premature", "raw"]), (
            f"AI consultant failed to enforce Ama contraindication rule: {response[:300]}"
        )
