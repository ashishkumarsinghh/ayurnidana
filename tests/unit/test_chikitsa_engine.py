"""Unit tests for ChikitsaEngine.
Validates formulation selection, dynamic syndromic synthesis,
biological safety guards (Ama/Sama status, Pediatric, Geriatric, Low Bala),
Aushadha Sevana Kala, Anupana vehicle adherence, and Pathya/Apathya rules.
"""
import pytest
from ayurnidana.core.models import (
    AmaStatus, AgniType, KoshthaType, Prognosis,
    DashavidhaPariksha, DiagnosisResult
)
from ayurnidana.core.dosha_engine import DoshaEngine
from ayurnidana.core.nidana_engine import NidanaEngine
from ayurnidana.core.chikitsa_engine import ChikitsaEngine

@pytest.fixture
def default_dashavidha():
    return DashavidhaPariksha(
        prakriti="Vata-Pitta",
        vikriti="Vata Pradhana",
        sara_tissue_excellence="Madhyama Sara",
        samhanana_compactness="Madhyama Samhanana",
        sattva_mental_strength="Madhyama Sattva",
        ahara_shakti_digestive_power="Madhyama Ahara Shakti",
        vyayama_shakti_physical_stamina="Madhyama",
        vaya_age_stage="Madhyamavastha"
    )

class TestChikitsaEngine:

    def test_canonical_chikitsa_generation(self, default_dashavidha):
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
        plan = ChikitsaEngine.generate_plan(diag, default_dashavidha, patient_age=45)
        
        assert len(plan.shamana_formulations) >= 3
        # Check classic Sandhivata drugs
        formulation_names = [f.name for f in plan.shamana_formulations]
        assert any("Guggulu" in name for name in formulation_names)
        assert any("Kwatha" in name or "Taila" in name for name in formulation_names)
        
        # Check Panchakarma guidance
        assert plan.panchakarma_guidance.eligible is True
        assert "Basti" in plan.panchakarma_guidance.recommended_therapy

    def test_ama_sama_state_contraindication(self, default_dashavidha):
        """CRITICAL: If patient is in Sama state, radical Shodhana MUST be deferred."""
        symptoms = ["tremors_stiffness", "dull_pain_swelling_edema", "tongue_thick_white_coating"]
        diag = NidanaEngine.diagnose(
            symptoms=symptoms,
            vikriti_pattern="Kapha-Vata Imbalance",
            ama_status=AmaStatus.SAMA,
            agni_status=AgniType.MANDAGNI,
            koshtha_status=KoshthaType.MADHYAMA,
            dhatu_involved=["Rasa Dhatu", "Asthi Dhatu"],
            srotas_involved=["Rasavaha Srotas"]
        )
        plan = ChikitsaEngine.generate_plan(diag, default_dashavidha, patient_age=42)
        
        # In Sama state, radical Shodhana is contraindicated
        assert plan.panchakarma_guidance.eligible is False
        assert "DEFERRED" in plan.panchakarma_guidance.recommended_therapy.upper() or "CONTRAINDICATED" in plan.panchakarma_guidance.recommended_therapy.upper()
        contra_str = " ".join(plan.panchakarma_guidance.contraindications_checked) + " " + plan.panchakarma_guidance.reasoning
        assert "ama" in contra_str.lower() or "sama" in contra_str.lower()
        # Deepana-Pachana must be present
        assert len(plan.deepana_pachana_protocol) > 0

    def test_pediatric_age_guard(self, default_dashavidha):
        """Pediatric patients (< 12 years) must be spared harsh purification."""
        diag = NidanaEngine.diagnose(
            symptoms=["acid_reflux_heartburn", "burning_sensation"],
            vikriti_pattern="Pitta Pradhana",
            ama_status=AmaStatus.NIRAMA,
            agni_status=AgniType.TIKSHNAGNI,
            koshtha_status=KoshthaType.MRIDU,
            dhatu_involved=["Rasa Dhatu"],
            srotas_involved=["Annavaha Srotas"]
        )
        plan = ChikitsaEngine.generate_plan(diag, default_dashavidha, patient_age=8)
        
        assert plan.panchakarma_guidance.eligible is False
        contra_str = " ".join(plan.panchakarma_guidance.contraindications_checked) + " " + plan.panchakarma_guidance.reasoning
        assert "age" in contra_str.lower() or "pediatric" in contra_str.lower() or "balya" in contra_str.lower()

    def test_geriatric_age_guard(self, default_dashavidha):
        """Geriatric patients (> 75 years) must be protected from radical Shodhana."""
        diag = NidanaEngine.diagnose(
            symptoms=["joint_pain_cracking", "pain_sharp_throbbing"],
            vikriti_pattern="Vata Pradhana",
            ama_status=AmaStatus.NIRAMA,
            agni_status=AgniType.VISHAMAGNI,
            koshtha_status=KoshthaType.KRURA,
            dhatu_involved=["Asthi Dhatu"],
            srotas_involved=["Asthivaha Srotas"]
        )
        plan = ChikitsaEngine.generate_plan(diag, default_dashavidha, patient_age=82)
        
        assert plan.panchakarma_guidance.eligible is False
        contra_str = " ".join(plan.panchakarma_guidance.contraindications_checked) + " " + plan.panchakarma_guidance.reasoning
        assert "age" in contra_str.lower() or "geriatric" in contra_str.lower() or "elderly" in contra_str.lower() or "vriddha" in contra_str.lower()

    def test_low_bala_contraindication(self):
        """Patients with Avara / Hina Bala must not undergo aggressive cleansing."""
        low_bala_dashavidha = DashavidhaPariksha(
            prakriti="Vata-Pitta",
            vikriti="Vata Pradhana",
            sara_tissue_excellence="Avara Sara (Poor)",
            samhanana_compactness="Avara Samhanana",
            sattva_mental_strength="Avara Sattva (Fragile)",
            ahara_shakti_digestive_power="Avara Ahara Shakti",
            vyayama_shakti_physical_stamina="Avara",
            vaya_age_stage="Madhyamavastha"
        )
        diag = NidanaEngine.diagnose(
            symptoms=["burning_sensation", "skin_rashes_inflammation_acne"],
            vikriti_pattern="Pitta Pradhana",
            ama_status=AmaStatus.NIRAMA,
            agni_status=AgniType.TIKSHNAGNI,
            koshtha_status=KoshthaType.MRIDU,
            dhatu_involved=["Rakta Dhatu"],
            srotas_involved=["Raktavaha Srotas"]
        )
        plan = ChikitsaEngine.generate_plan(diag, low_bala_dashavidha, patient_age=35)
        assert plan.panchakarma_guidance.eligible is False
        contra_str = " ".join(plan.panchakarma_guidance.contraindications_checked) + " " + plan.panchakarma_guidance.reasoning
        assert "bala" in contra_str.lower() or "strength" in contra_str.lower()

    def test_aushadha_sevana_kala_validity(self, default_dashavidha):
        """Formulations must prescribe authentic classical timings."""
        valid_kalas = [
            "Pragbhakta", "Madhyabhakta", "Adhobhakta", "Sabhakta",
            "Samana", "Nishi", "Muhurmuhur", "Grasa", "Grasantara"
        ]
        diag = NidanaEngine.diagnose(
            symptoms=["acid_reflux_heartburn", "burning_sensation"],
            vikriti_pattern="Pitta Pradhana",
            ama_status=AmaStatus.NIRAMA,
            agni_status=AgniType.TIKSHNAGNI,
            koshtha_status=KoshthaType.MRIDU,
            dhatu_involved=["Rasa Dhatu"],
            srotas_involved=["Annavaha Srotas"]
        )
        plan = ChikitsaEngine.generate_plan(diag, default_dashavidha, patient_age=35)
        for f in plan.shamana_formulations:
            kala = f.aushadha_sevana_kala
            assert any(vk.lower() in kala.lower() for vk in valid_kalas)

    def test_anupana_validity(self, default_dashavidha):
        """Prescriptions must have legitimate Ayurvedic vehicles (Anupana)."""
        diag = NidanaEngine.diagnose(
            symptoms=["joint_pain_cracking", "pain_sharp_throbbing"],
            vikriti_pattern="Vata Pradhana",
            ama_status=AmaStatus.NIRAMA,
            agni_status=AgniType.VISHAMAGNI,
            koshtha_status=KoshthaType.KRURA,
            dhatu_involved=["Asthi Dhatu"],
            srotas_involved=["Asthivaha Srotas"]
        )
        plan = ChikitsaEngine.generate_plan(diag, default_dashavidha, patient_age=45)
        for f in plan.shamana_formulations:
            assert f.anupana_vehicle is not None
            assert len(f.anupana_vehicle.strip()) > 3

    def test_pathya_and_apathya_rules(self, default_dashavidha):
        """Pathya (wholesome) and Apathya (unwholesome) lists must be defined."""
        diag = NidanaEngine.diagnose(
            symptoms=["wheezing_shortness_of_breath", "cough_chronic"],
            vikriti_pattern="Kapha-Vata Imbalance",
            ama_status=AmaStatus.NIRAMA,
            agni_status=AgniType.MANDAGNI,
            koshtha_status=KoshthaType.MADHYAMA,
            dhatu_involved=["Pranavaha Srotas"],
            srotas_involved=["Pranavaha Srotas"]
        )
        plan = ChikitsaEngine.generate_plan(diag, default_dashavidha, patient_age=40)
        regimen = plan.dietary_and_lifestyle_regimen
        assert len(regimen.pathya_ahara_wholesome_diet) > 0
        assert len(regimen.apathya_ahara_unwholesome_diet) > 0
        assert len(regimen.pathya_vihara_recommended_lifestyle) > 0
        assert len(regimen.apathya_vihara_contraindicated_habits) > 0
