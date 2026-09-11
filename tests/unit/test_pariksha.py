"""Unit tests for Ashta Sthana and Dashavidha Pariksha clinical evaluation modules.
Validates the 8-fold and 10-fold diagnostic methodologies based on Yogaratnakara and Charaka Vimanasthana 8.
"""
import pytest
from ayurnidana.core.models import AshtaSthanaPariksha, DashavidhaPariksha
from ayurnidana.core.ashta_sthana import ASHTA_STHANA_CATALOG, AshtaSthanaEvaluator
from ayurnidana.core.dashavidha import DASHAVIDHA_CRITERIA, DashavidhaEvaluator

class TestPariksha:

    def test_ashta_sthana_catalog_completeness(self):
        required_sthanas = ["nadi", "jihva", "mutra", "mala", "shabda", "sparsha", "druk", "akruti"]
        for sthana in required_sthanas:
            assert sthana in ASHTA_STHANA_CATALOG
            assert "title" in ASHTA_STHANA_CATALOG[sthana]
            assert "options" in ASHTA_STHANA_CATALOG[sthana]
            assert len(ASHTA_STHANA_CATALOG[sthana]["options"]) >= 3

    def test_ashta_sthana_evaluator(self):
        exam = AshtaSthanaPariksha(
            nadi_pulse="Sarpa Gati (Serpentine / Quick / Light / Thread-like) - Vata Pradhana",
            jihva_tongue="Dry, rough, dark/brownish coating with central fissures - Vataja",
            mutra_urine="Pale, clear, scanty, frequent with slight astringency - Vataja",
            mala_stool="Dry, hard, dark, scybalous, painful evacuation (Krura Koshtha) - Vataja",
            shabda_voice="Hoarse, broken, feeble, rapid, dry raspy voice - Vataja",
            sparsha_skin="Cold, dry, rough, cracked texture - Vataja",
            druk_eyes="Dry, dull, lusterless, sunken eyes, frequent involuntary blinking - Vataja",
            akruti_appearance="Ectomorphic, thin, prominent veins & tendons, restless gait - Vataja"
        )
        res = AshtaSthanaEvaluator.evaluate(exam)
        assert res["weights"]["Vata"] >= 3.0
        assert "pulse" in res

    def test_dashavidha_criteria_completeness(self):
        required_criteria = ["sara", "samhanana", "pramana", "satmya", "sattva", "ahara_shakti", "vyayama_shakti", "vaya"]
        for crit in required_criteria:
            assert crit in DASHAVIDHA_CRITERIA
            assert "title" in DASHAVIDHA_CRITERIA[crit]
            assert "options" in DASHAVIDHA_CRITERIA[crit]

    def test_dashavidha_evaluator_bala_calculation(self):
        exam_pravara = DashavidhaPariksha(
            prakriti="Pitta-Kapha",
            vikriti="Pitta Pradhana",
            sara_tissue_excellence="Pravara Sara (Superior Vitality / High Tissue Strength)",
            samhanana_compactness="Su-samhata (Well-compacted, dense, robust skeletal frame)",
            sattva_mental_strength="Pravara Sattva (High emotional resilience)",
            ahara_shakti_digestive_power="Pravara Ahara Shakti",
            vyayama_shakti_physical_stamina="Pravara Vyayama Shakti (High endurance)",
            vaya_age_stage="Madhyamavastha"
        )
        eval_res = DashavidhaEvaluator.evaluate_bala(exam_pravara)
        assert "Pravara" in eval_res["bala_grade"]
        assert eval_res["panchakarma_eligible"] is True

        exam_avara = DashavidhaPariksha(
            prakriti="Vata",
            vikriti="Vata Pradhana",
            sara_tissue_excellence="Avara Sara (Deficient / Vulnerable Tissue Tone)",
            samhanana_compactness="Hina Samhanana (Loose joint architecture, fragile)",
            sattva_mental_strength="Avara / Heena Sattva (Low pain threshold, anxious)",
            ahara_shakti_digestive_power="Avara Ahara Shakti (Poor appetite, sluggish)",
            vyayama_shakti_physical_stamina="Avara (Low stamina)",
            vaya_age_stage="Vriddhavastha"
        )
        eval_res_avara = DashavidhaEvaluator.evaluate_bala(exam_avara)
        assert "Avara" in eval_res_avara["bala_grade"]
        assert eval_res_avara["panchakarma_eligible"] is False
