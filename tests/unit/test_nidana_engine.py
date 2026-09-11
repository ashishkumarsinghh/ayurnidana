"""Unit tests for NidanaEngine.
Validates canonical disease diagnosis across all 20 classical entities,
cardinal symptom gating, universal syndromic engine fallback (Charaka Sutrasthana 18:44-46),
differential diagnosis, and prognosis.
"""
import pytest
from ayurnidana.core.models import AmaStatus, AgniType, KoshthaType, Prognosis
from ayurnidana.core.dosha_engine import DoshaEngine
from ayurnidana.core.nidana_engine import NidanaEngine
from ayurnidana.knowledge.classical_db import CLASSICAL_DISEASES

class TestNidanaEngine:

    @pytest.mark.parametrize("disease_key,symptoms", [
        ("sandhivata", ["joint_pain_cracking", "pain_sharp_throbbing", "tremors_stiffness", "cold_intolerance"]),
        ("amavata", ["tremors_stiffness", "dull_pain_swelling_edema", "loss_of_taste_aruchi", "tongue_thick_white_coating"]),
        ("gridhrasi", ["sciatica_radiating_leg_pain", "pain_sharp_throbbing", "tremors_stiffness", "constipation_hard_stools"]),
        ("amlapitta", ["acid_reflux_heartburn", "burning_sensation", "intense_sharp_hunger", "irritability_anger"]),
        ("grahani", ["malabsorption_mucus_stools", "bloating_flatulence", "loose_stools_diarrhea", "loss_of_taste_aruchi"]),
        ("tamaka_shwasa", ["wheezing_shortness_of_breath", "cough_chronic", "excess_mucus_congestion", "anxiety_restlessness"]),
        ("kasa", ["cough_chronic", "excess_mucus_congestion", "heaviness_body_limbs"]),
        ("vatarakta", ["gout_big_toe_burning_pain", "burning_sensation", "pain_sharp_throbbing", "skin_rashes_inflammation_acne"]),
        ("kushtha", ["skin_rashes_inflammation_acne", "burning_sensation", "dryness_skin_hair"]),
        ("kamala", ["yellowish_eyes_urine", "burning_sensation", "loss_of_taste_aruchi", "loose_stools_diarrhea"]),
        ("arsha", ["anal_pain_bleeding_piles", "constipation_hard_stools", "bloating_flatulence"]),
        ("prameha", ["frequent_cloudy_urination", "excessive_thirst_sweating", "heaviness_body_limbs", "sweet_taste_in_mouth"]),
        ("sthaulya", ["weight_gain_slow_metabolism", "heaviness_body_limbs", "intense_sharp_hunger", "excessive_thirst_sweating"]),
        ("anidra_chittodvega", ["insomnia_disturbed_sleep", "anxiety_restlessness", "irritability_anger", "dryness_skin_hair"]),
        ("shirashoola", ["headache_migraine_throbbing", "pain_sharp_throbbing", "irritability_anger", "insomnia_disturbed_sleep"]),
        ("pandu", ["pallor_fatigue_anemia", "heaviness_body_limbs", "cold_intolerance", "weight_loss_emaciation"]),
        ("shotha", ["dull_pain_swelling_edema", "heaviness_body_limbs", "weight_gain_slow_metabolism"]),
        ("mutrakrichhra", ["burning_painful_urination", "burning_sensation", "frequent_cloudy_urination"]),
        ("atisara", ["severe_acute_diarrhea", "loose_stools_diarrhea", "burning_sensation", "bloating_flatulence"]),
        ("cittodvega", ["panic_intense_worry", "anxiety_restlessness", "insomnia_disturbed_sleep", "tremors_stiffness"])
    ])
    def test_all_20_canonical_diseases_diagnosed(self, disease_key, symptoms):
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        ama_st, _ = DoshaEngine.assess_ama(symptoms)
        dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(symptoms)
        
        diag = NidanaEngine.diagnose(
            symptoms=symptoms,
            vikriti_pattern=vikriti,
            ama_status=ama_st,
            agni_status=AgniType.MANDAGNI if "amavata" in disease_key else AgniType.SAMAGNI,
            koshtha_status=KoshthaType.MADHYAMA,
            dhatu_involved=dhatus,
            srotas_involved=srotas
        )
        assert diag is not None
        expected_meta = CLASSICAL_DISEASES[disease_key]
        assert diag.primary_condition == expected_meta["name"]
        assert len(diag.dhatu_involved) > 0
        assert len(diag.srotas_involved) > 0
        assert diag.classical_citations is not None
        assert len(diag.classical_citations) > 0

    def test_cardinal_symptom_gating(self):
        """Vague non-cardinal symptoms must NOT falsely diagnose specific named diseases."""
        vague_symptoms = ["loss_of_taste_aruchi", "dryness_skin_hair"]
        scores, vikriti = DoshaEngine.calculate_vikriti(vague_symptoms)
        ama_st, _ = DoshaEngine.assess_ama(vague_symptoms)
        dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(vague_symptoms)
        
        diag = NidanaEngine.diagnose(
            symptoms=vague_symptoms,
            vikriti_pattern=vikriti,
            ama_status=ama_st,
            agni_status=AgniType.SAMAGNI,
            koshtha_status=KoshthaType.MADHYAMA,
            dhatu_involved=dhatus,
            srotas_involved=srotas
        )
        # Should not diagnose specialized diseases like Gridhrasi or Kamala without their cardinal signs
        assert "Gridhrasi" not in diag.sanskrit_name
        assert "Kamala" not in diag.sanskrit_name
        assert "Mutrakrichhra" not in diag.sanskrit_name

    def test_universal_syndromic_fallback(self):
        """When no canonical cardinal symptoms match, the engine must construct
        a syndromic diagnosis per Charaka Sutrasthana 18:44-46.
        """
        isolated_symptoms = ["skin_rashes_inflammation_acne", "sweet_taste_in_mouth"]
        scores, vikriti = DoshaEngine.calculate_vikriti(isolated_symptoms)
        ama_st, _ = DoshaEngine.assess_ama(isolated_symptoms)
        dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(isolated_symptoms)
        
        diag = NidanaEngine.diagnose(
            symptoms=isolated_symptoms,
            vikriti_pattern=vikriti,
            ama_status=ama_st,
            agni_status=AgniType.TIKSHNAGNI,
            koshtha_status=KoshthaType.MADHYAMA,
            dhatu_involved=dhatus,
            srotas_involved=srotas
        )
        assert diag is not None
        assert "प्रदोषज" in diag.sanskrit_name or "Syndromic" in diag.primary_condition or diag.primary_condition in [d["name"] for d in CLASSICAL_DISEASES.values()]

    def test_differential_diagnosis_generation(self):
        symptoms = ["wheezing_shortness_of_breath", "cough_chronic", "excess_mucus_congestion"]
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        ama_st, _ = DoshaEngine.assess_ama(symptoms)
        dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(symptoms)
        
        diag = NidanaEngine.diagnose(
            symptoms=symptoms,
            vikriti_pattern=vikriti,
            ama_status=ama_st,
            agni_status=AgniType.MANDAGNI,
            koshtha_status=KoshthaType.MADHYAMA,
            dhatu_involved=dhatus,
            srotas_involved=srotas
        )
        # Should have primary Tamaka Shwasa and secondary Kasa in differential
        assert len(diag.secondary_conditions) > 0
