"""UI and Component tests for AyurNidana.
Validates case sheet rendering, chart dataframe transformations,
Streamlit app module integrity, and live server responsiveness.
"""
import pytest
import urllib.request
from ayurnidana.core.models import (
    Gender, AmaStatus, AgniType, KoshthaType, Prognosis,
    PatientDemographics, AshtaSthanaPariksha, DashavidhaPariksha,
    ClinicalCase, DiagnosisResult, TreatmentPlan, NidanaPanchaka,
    Formulation, PanchakarmaPrescription, PathyaApathya
)
from ayurnidana.ui.components.case_sheet import generate_markdown_case_sheet
from ayurnidana.ui.components.charts import get_dosha_df
from ayurnidana.ui.components.style import CUSTOM_CSS

class TestUIComponents:

    @pytest.fixture
    def mock_case(self):
        patient = PatientDemographics(
            name="Aarav Sharma",
            age=34,
            gender=Gender.MALE,
            occupation="Engineer",
            current_season="Varsha"
        )
        ashta = AshtaSthanaPariksha(
            nadi_pulse="Manduka Gati - Pitta",
            jihva_tongue="Sama Jihva",
            mutra_urine="Pittaja",
            mala_stool="Mridu Koshtha",
            shabda_voice="Normal",
            sparsha_skin="Warm",
            druk_eyes="Clear",
            akruti_appearance="Medium"
        )
        dashavidha = DashavidhaPariksha(
            prakriti="Pitta-Kapha",
            vikriti="Pitta Pradhana",
            sara_tissue_excellence="Madhyama Sara",
            samhanana_compactness="Madhyama Samhanana",
            sattva_mental_strength="Pravara Sattva",
            ahara_shakti_digestive_power="Pravara Ahara Shakti",
            vyayama_shakti_physical_stamina="Madhyama",
            vaya_age_stage="Madhyamavastha"
        )
        np = NidanaPanchaka(
            nidana_etiology=["Spicy food", "Irregular sleep"],
            purvarupa_prodromes=["Mild burning in throat"],
            rupa_cardinal_symptoms=["Heartburn", "Acid regurgitation"],
            upashaya_anupashaya={"Upashaya": ["Cold milk"], "Anupashaya": ["Spicy food"]},
            samprapti_pathogenesis={"Sanchaya": "Pitta accumulation"}
        )
        diag = DiagnosisResult(
            primary_condition="Acid Peptic Disorder / GERD",
            sanskrit_name="Amlapitta (अम्लपित्त)",
            primary_dosha="Pitta",
            doshic_subtype="Pachaka Pitta Aggravation",
            dhatu_involved=["Rasa Dhatu"],
            srotas_involved=["Annavaha Srotas", "Purishavaha Srotas"],
            ama_status=AmaStatus.NIRAMA,
            agni_status=AgniType.TIKSHNAGNI,
            koshtha_status=KoshthaType.MRIDU,
            prognosis=Prognosis.SUKHA_SADHYA,
            nidana_panchaka=np,
            clinical_reasoning="Classical presentation of Vidagdha Amlapitta.",
            classical_citations=["Madhava Nidana, Amlapitta Adhyaya"]
        )
        formulation = Formulation(
            name="Avipattikara Churna",
            category="Churna",
            classical_indication="Sovereign remedy for Amlapitta and Vibandha",
            dosage="3-5 grams twice daily",
            anupana_vehicle="Luke-warm water or coconut water",
            aushadha_sevana_kala="Pragbhakta (Before meals)",
            duration_weeks=4,
            classical_reference="Bhaishajya Ratnavali, Amlapitta Chikitsa"
        )
        pk = PanchakarmaPrescription(
            eligible=True,
            recommended_therapy="Mridu Virechana (Therapeutic Purgation)",
            reasoning="Pitta dosha is best eliminated through the anorectal route (Virechana).",
            purvakarma=["Deepana with Shunthi", "Snehapana with Kalyanaka Ghrita"],
            pradhanakarma="Trivrit Lehyam 20g with warm milk",
            paschatkarma=["Samsarjana Krama for 3 days"],
            contraindications_checked=[]
        )
        pathya = PathyaApathya(
            pathya_ahara_wholesome_diet=["Old rice", "Moong dal", "Pomegranate"],
            apathya_ahara_unwholesome_diet=["Fermented foods", "Pickles", "Chili"],
            pathya_vihara_recommended_lifestyle=["Gentle evening walks", "Moonlight exposure (Sheetala Vihara)"],
            apathya_vihara_contraindicated_habits=["Excessive anger (Krodha)", "Sun exposure"],
            viruddha_ahara_warnings=["Never mix milk with sour citrus or salt"],
            yoga_and_pranayama=["Sheetali Pranayama", "Vajrasana after meals"]
        )
        treatment = TreatmentPlan(
            deepana_pachana_protocol=["Panchakola Churna 1g before meals"],
            shamana_formulations=[formulation],
            panchakarma_guidance=pk,
            dietary_and_lifestyle_regimen=pathya,
            rasayana_recovery_plan=["Amalaki Rasayana 3g daily with honey and ghee"],
            red_flag_warnings=["Hematemesis (vomiting blood) requires emergency endoscopy"],
            follow_up_recommendation="Review after 14 days"
        )
        return ClinicalCase(
            patient=patient,
            ashta_sthana=ashta,
            dashavidha=dashavidha,
            chief_complaints=["Severe heartburn", "Sour belching"],
            onset_and_duration="3 weeks, aggravated after dinner",
            dosha_scores={"Vata": 20.0, "Pitta": 65.0, "Kapha": 15.0},
            diagnosis=diag,
            treatment=treatment
        )

    def test_case_sheet_generation_integrity(self, mock_case):
        md = generate_markdown_case_sheet(mock_case)
        assert "# AYURNIDANA CLINICAL CASE SHEET" in md
        assert "Aarav Sharma" in md
        assert "Amlapitta" in md
        assert "Avipattikara Churna" in md
        assert "Mridu Virechana" in md
        assert "| Drug Name | Form | Dosage |" in md
        assert "Hematemesis" in md

    def test_dosha_df_transformation(self):
        scores = {"Vata": 50.0, "Pitta": 30.0, "Kapha": 20.0}
        df = get_dosha_df(scores)
        assert len(df) == 3
        assert list(df.columns) == ["Dosha", "Percentage (%)", "Color"]
        assert df.loc[df["Dosha"] == "Vata", "Percentage (%)"].values[0] == 50.0

    def test_theme_css_generation(self):
        css = CUSTOM_CSS
        assert "<style>" in css
        assert "</style>" in css

    def test_app_module_imports_cleanly(self):
        import ayurnidana.ui.app
        assert hasattr(ayurnidana.ui.app, "main") or hasattr(ayurnidana.ui.app, "st")

    def test_live_streamlit_server_running(self):
        """Validates that the live Streamlit application responds with HTTP 200 OK."""
        try:
            req = urllib.request.Request("http://localhost:8501", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status == 200
                html = response.read().decode("utf-8", errors="ignore")
                assert "Streamlit" in html or "ayurnidana" in html.lower() or "<!DOCTYPE html>" in html
        except Exception as e:
            pytest.fail(f"Streamlit server on port 8501 is not responding: {e}")

    def test_diagnosis_and_treatment_attributes_match_ui(self, mock_case):
        """Validates that Tab 2 and Tab 3 UI attributes are safely accessible without AttributeError."""
        diag = mock_case.diagnosis
        treatment = mock_case.treatment
        
        # Tab 2 attributes
        secondary = getattr(diag, "secondary_conditions", getattr(diag, "secondary_differential_conditions", []))
        assert isinstance(secondary, list)
        
        samprapti = getattr(diag.nidana_panchaka, "samprapti_pathogenesis", getattr(diag.nidana_panchaka, "samprapti", {}))
        assert isinstance(samprapti, dict)
        
        assert diag.primary_condition is not None
        assert diag.sanskrit_name is not None
        assert diag.doshic_subtype is not None
        assert diag.prognosis.value is not None
        assert diag.agni_status.value is not None
        assert diag.ama_status.value is not None
        
        # Tab 3 attributes
        for form in treatment.shamana_formulations:
            cat = getattr(form, 'category', getattr(form, 'formulation_type', 'Formulation'))
            anupana = getattr(form, 'anupana_vehicle', getattr(form, 'anupana', 'Warm water'))
            timing = getattr(form, 'aushadha_sevana_kala', getattr(form, 'timing', 'After meals'))
            action = getattr(form, 'classical_indication', getattr(form, 'therapeutic_action', ''))
            assert cat is not None
            assert anupana is not None
            assert timing is not None
            assert action is not None

        wholesome_foods = getattr(treatment.dietary_and_lifestyle_regimen, 'pathya_ahara_wholesome_diet', getattr(treatment.dietary_and_lifestyle_regimen, 'pathya_ahara_beneficial_foods', []))
        unwholesome_foods = getattr(treatment.dietary_and_lifestyle_regimen, 'apathya_ahara_unwholesome_diet', getattr(treatment.dietary_and_lifestyle_regimen, 'apathya_ahara_contraindicated_foods', []))
        wholesome_habits = getattr(treatment.dietary_and_lifestyle_regimen, 'pathya_vihara_recommended_lifestyle', getattr(treatment.dietary_and_lifestyle_regimen, 'pathya_vihara_beneficial_lifestyle', []))
        unwholesome_habits = getattr(treatment.dietary_and_lifestyle_regimen, 'apathya_vihara_contraindicated_habits', [])

        assert len(wholesome_foods) > 0
        assert len(unwholesome_foods) > 0
        assert len(wholesome_habits) > 0
        assert len(unwholesome_habits) > 0

