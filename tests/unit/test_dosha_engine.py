"""Unit tests for DoshaEngine.
Validates Tridosha calculation, Ama assessment, Dhatu and Srotas determination, and edge cases.
"""
import pytest
from ayurnidana.core.models import AmaStatus, AgniType, KoshthaType
from ayurnidana.core.dosha_engine import DoshaEngine

class TestDoshaEngine:

    def test_vata_dominance(self):
        symptoms = [
            "joint_pain_cracking",
            "pain_sharp_throbbing",
            "tremors_stiffness",
            "dryness_skin_hair",
            "constipation_hard_stools"
        ]
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        assert scores["Vata"] > scores["Pitta"]
        assert scores["Vata"] > scores["Kapha"]
        assert "Vata" in vikriti

    def test_pitta_dominance(self):
        symptoms = [
            "burning_sensation",
            "acid_reflux_heartburn",
            "skin_rashes_inflammation_acne",
            "intense_sharp_hunger",
            "loose_stools_diarrhea"
        ]
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        assert scores["Pitta"] > scores["Vata"]
        assert scores["Pitta"] > scores["Kapha"]
        assert "Pitta" in vikriti

    def test_kapha_dominance(self):
        symptoms = [
            "heaviness_body_limbs",
            "excess_mucus_congestion",
            "weight_gain_slow_metabolism",
            "loss_of_taste_aruchi",
            "excessive_sleep_lethargy"
        ]
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        assert scores["Kapha"] > scores["Vata"]
        assert scores["Kapha"] > scores["Pitta"]
        assert "Kapha" in vikriti

    def test_dvandvaja_vata_pitta(self):
        symptoms = [
            "joint_pain_cracking",
            "pain_sharp_throbbing",
            "dryness_skin_hair",
            "burning_sensation",
            "acid_reflux_heartburn",
            "skin_rashes_inflammation_acne"
        ]
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        assert "Dvandvaja" in vikriti
        assert "Vata" in vikriti and "Pitta" in vikriti

    def test_sannipataja_pattern(self):
        # Balanced high symptoms across all 3 doshas
        symptoms = [
            "joint_pain_cracking", "dryness_skin_hair",
            "burning_sensation", "acid_reflux_heartburn",
            "heaviness_body_limbs", "excess_mucus_congestion"
        ]
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        assert "Sannipataja" in vikriti or "Dvandvaja" in vikriti

    def test_ama_assessment_sama_state(self):
        symptoms = [
            "tongue_thick_white_coating",
            "loss_of_taste_aruchi",
            "heaviness_body_limbs",
            "sluggish_digestion_mandagni",
            "malabsorption_mucus_stools"
        ]
        ama_status, reasons = DoshaEngine.assess_ama(symptoms, "Thick white greasy coating")
        assert ama_status == AmaStatus.SAMA
        assert len(reasons) > 0

    def test_ama_assessment_nirama_state(self):
        symptoms = [
            "joint_pain_cracking",
            "pain_sharp_throbbing",
            "dryness_skin_hair"
        ]
        ama_status, reasons = DoshaEngine.assess_ama(symptoms, "Clean pink tongue")
        assert ama_status == AmaStatus.NIRAMA

    def test_dhatu_and_srotas_determination(self):
        symptoms = [
            "joint_pain_cracking",  # Asthi Dhatu, Asthivaha
            "acid_reflux_heartburn", # Annavaha
            "wheezing_shortness_of_breath", # Pranavaha
            "frequent_cloudy_urination" # Meda / Mutravaha
        ]
        dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(symptoms)
        assert any("Asthi" in d for d in dhatus)
        assert any("Annavaha" in s for s in srotas)
        assert any("Pranavaha" in s for s in srotas)
        assert any("Mutravaha" in s for s in srotas)

    def test_empty_symptoms_graceful_handling(self):
        scores, vikriti = DoshaEngine.calculate_vikriti([])
        assert scores == {"Vata": 33.3, "Pitta": 33.3, "Kapha": 33.3}
        assert "Balanced" in vikriti or "Undetermined" in vikriti
        
        ama_status, reasons = DoshaEngine.assess_ama([])
        assert ama_status == AmaStatus.NIRAMA
        
        dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas([])
        assert len(dhatus) > 0  # Falls back to primary Rasa Dhatu
        assert len(srotas) > 0  # Falls back to Annavaha Srotas
