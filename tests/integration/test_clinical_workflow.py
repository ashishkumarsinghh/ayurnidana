"""Integration tests for End-to-End Clinical Workflow in AyurNidana.
Simulates real-world clinical patient encounters:
1. Osteoarthritis (Sandhivata) in geriatric patient
2. Acute Rheumatoid Arthritis (Amavata) in Sama condition
3. Acid Peptic / GERD (Amlapitta) with Pitta Tikshnagni
4. Bronchial Asthma (Tamaka Shwasa) with Pranavaha obstruction
5. Novel Multisystem Syndromic presentation (Non-canonical complex)
Validates complete clinical case sheet generation and structural integrity.
"""
import pytest
from ayurnidana.core.models import (
    Gender, AmaStatus, AgniType, KoshthaType, Prognosis,
    PatientDemographics, AshtaSthanaPariksha, DashavidhaPariksha, ClinicalCase
)
from ayurnidana.core.dosha_engine import DoshaEngine
from ayurnidana.core.nidana_engine import NidanaEngine
from ayurnidana.core.chikitsa_engine import ChikitsaEngine
from ayurnidana.core.layman_mapper import extract_symptoms_from_text
from ayurnidana.ui.components.case_sheet import generate_markdown_case_sheet

class TestClinicalIntegration:

    def test_e2e_case_sandhivata_geriatric(self):
        # 1. Narrative Input
        raw_text = "I am a 68 year old grandmother. My knees make severe clicking noises, ache constantly with sharp throbbing pain, and are very stiff in cold weather."
        symptoms = extract_symptoms_from_text(raw_text)
        assert len(symptoms) >= 2
        
        # 2. Examination
        demographics = PatientDemographics(name="Kalyani Devi", age=68, gender=Gender.FEMALE, occupation="Retired")
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        ama_st, _ = DoshaEngine.assess_ama(symptoms, "Clean pink tongue")
        dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(symptoms)
        
        # 3. Nidana
        diag = NidanaEngine.diagnose(
            symptoms=symptoms,
            vikriti_pattern=vikriti,
            ama_status=ama_st,
            agni_status=AgniType.VISHAMAGNI,
            koshtha_status=KoshthaType.KRURA,
            dhatu_involved=dhatus,
            srotas_involved=srotas
        )
        assert "Sandhivata" in diag.sanskrit_name or "Osteoarthritis" in diag.primary_condition
        
        # 4. Chikitsa
        dashavidha = DashavidhaPariksha(
            prakriti="Vata-Kapha",
            vikriti=vikriti,
            sara_tissue_excellence="Madhyama Sara",
            samhanana_compactness="Madhyama Samhanana",
            sattva_mental_strength="Madhyama Sattva",
            ahara_shakti_digestive_power="Madhyama Ahara Shakti",
            vyayama_shakti_physical_stamina="Avara",
            vaya_age_stage="Vriddhavastha"
        )
        plan = ChikitsaEngine.generate_plan(diag, dashavidha, patient_age=68)
        assert len(plan.shamana_formulations) >= 2
        
        # 5. Case Sheet Assembly
        ashta_sthana = AshtaSthanaPariksha(
            nadi_pulse="Sarpa Gati - Vata Pradhana",
            jihva_tongue="Nirama Jihva",
            mutra_urine="Normal",
            mala_stool="Krura Koshtha",
            shabda_voice="Normal",
            sparsha_skin="Cold and rough",
            druk_eyes="Normal",
            akruti_appearance="Lean"
        )
        case = ClinicalCase(
            patient=demographics,
            ashta_sthana=ashta_sthana,
            dashavidha=dashavidha,
            chief_complaints=["Joint pain and cracking", "Morning stiffness"],
            onset_and_duration="6 months, insidious onset",
            dosha_scores=scores,
            diagnosis=diag,
            treatment=plan
        )
        case_md = generate_markdown_case_sheet(case)
        assert "# AYURNIDANA CLINICAL CASE SHEET" in case_md
        assert "Kalyani Devi" in case_md
        assert "ROGA NIDANA" in case_md
        assert "CHIKITSA PLAN" in case_md

    def test_e2e_case_amavata_acute_sama(self):
        # High Ama, feverish heaviness, coated tongue
        symptoms = ["tremors_stiffness", "dull_pain_swelling_edema", "loss_of_taste_aruchi", "tongue_thick_white_coating"]
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        ama_st, ama_reasons = DoshaEngine.assess_ama(symptoms, "Heavy thick white greasy coating")
        assert ama_st == AmaStatus.SAMA
        
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
        assert "Amavata" in diag.sanskrit_name
        
        dashavidha = DashavidhaPariksha(
            prakriti="Kapha-Vata",
            vikriti=vikriti,
            sara_tissue_excellence="Madhyama Sara",
            samhanana_compactness="Madhyama Samhanana",
            sattva_mental_strength="Avara Sattva",
            ahara_shakti_digestive_power="Avara Ahara Shakti",
            vyayama_shakti_physical_stamina="Avara",
            vaya_age_stage="Madhyamavastha"
        )
        plan = ChikitsaEngine.generate_plan(diag, dashavidha, patient_age=38)
        
        # Verify strict Ama protocol: Panchakarma deferred, Deepana-Pachana mandatory
        assert plan.panchakarma_guidance.eligible is False
        assert len(plan.deepana_pachana_protocol) > 0
        assert any("shunthi" in dp.lower() or "panchakola" in dp.lower() or "mudga" in dp.lower() or "langhana" in dp.lower() for dp in plan.deepana_pachana_protocol)

    def test_e2e_case_amlapitta_hyperacidity(self):
        symptoms = ["acid_reflux_heartburn", "burning_sensation", "intense_sharp_hunger"]
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(symptoms)
        
        diag = NidanaEngine.diagnose(
            symptoms=symptoms,
            vikriti_pattern=vikriti,
            ama_status=AmaStatus.NIRAMA,
            agni_status=AgniType.TIKSHNAGNI,
            koshtha_status=KoshthaType.MRIDU,
            dhatu_involved=dhatus,
            srotas_involved=srotas
        )
        assert "Amlapitta" in diag.sanskrit_name
        assert "Pitta" in diag.doshic_subtype

    def test_e2e_case_tamaka_shwasa_respiratory(self):
        symptoms = ["wheezing_shortness_of_breath", "cough_chronic", "excess_mucus_congestion"]
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(symptoms)
        
        diag = NidanaEngine.diagnose(
            symptoms=symptoms,
            vikriti_pattern=vikriti,
            ama_status=AmaStatus.NIRAMA,
            agni_status=AgniType.MANDAGNI,
            koshtha_status=KoshthaType.MADHYAMA,
            dhatu_involved=dhatus,
            srotas_involved=srotas
        )
        assert "Tamaka Shwasa" in diag.sanskrit_name or "Kasa" in diag.sanskrit_name
        assert any("Pranavaha" in s for s in diag.srotas_involved)

    def test_e2e_case_novel_syndromic_sannipataja(self):
        # A combination without matching canonical cardinal cluster
        symptoms = ["burning_painful_urination", "dryness_skin_hair", "loss_of_taste_aruchi"]
        scores, vikriti = DoshaEngine.calculate_vikriti(symptoms)
        dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(symptoms)
        
        diag = NidanaEngine.diagnose(
            symptoms=symptoms,
            vikriti_pattern=vikriti,
            ama_status=AmaStatus.NIRAMA,
            agni_status=AgniType.SAMAGNI,
            koshtha_status=KoshthaType.MADHYAMA,
            dhatu_involved=dhatus,
            srotas_involved=srotas
        )
        # Should cleanly diagnose via Universal Syndromic Engine
        assert diag is not None
        assert diag.primary_condition is not None
        
        dashavidha = DashavidhaPariksha(
            prakriti="Tridosha",
            vikriti=vikriti,
            sara_tissue_excellence="Madhyama Sara",
            samhanana_compactness="Madhyama Samhanana",
            sattva_mental_strength="Madhyama Sattva",
            ahara_shakti_digestive_power="Madhyama Ahara Shakti",
            vyayama_shakti_physical_stamina="Madhyama",
            vaya_age_stage="Madhyamavastha"
        )
        plan = ChikitsaEngine.generate_plan(diag, dashavidha, patient_age=32)
        assert len(plan.shamana_formulations) > 0
