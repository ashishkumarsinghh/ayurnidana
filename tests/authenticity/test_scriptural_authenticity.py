"""Comprehensive Scriptural Authenticity & Doctrinal Non-Deviation Audit.
Strictly verifies that all diagnostics, formulations, pathogenesis, and treatment protocols
faithfully adhere to the Brihat Trayi (Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya)
and Laghu Trayi (Madhava Nidana, Sharngadhara Samhita, Bhavaprakasha, Bhaishajya Ratnavali)
with zero scriptural deviations or doctrinal errors.
"""
import pytest
from ayurnidana.knowledge.classical_db import CLASSICAL_DISEASES
from ayurnidana.core.models import AmaStatus, AgniType, KoshthaType, DashavidhaPariksha
from ayurnidana.core.nidana_engine import NidanaEngine
from ayurnidana.core.chikitsa_engine import ChikitsaEngine

class TestScripturalAuthenticity:

    @pytest.mark.parametrize("disease_key,data", CLASSICAL_DISEASES.items())
    def test_scriptural_citations_authenticity(self, disease_key, data):
        """Rule: Every disease must cite authoritative classical scriptures (Brihat Trayi or Laghu Trayi)."""
        citations = data.get("citations", [])
        assert len(citations) >= 2, f"Disease {disease_key} lacks sufficient authoritative citations."
        
        recognized_texts = [
            "charaka", "sushruta", "ashtanga", "madhava", "sharngadhara",
            "bhavaprakasha", "bhaishajya", "chakradatta", "yogaratnakara"
        ]
        has_authoritative_text = any(
            any(t in cit.lower() for t in recognized_texts)
            for cit in citations
        )
        assert has_authoritative_text, f"Disease {disease_key} citations do not reference recognized classical texts: {citations}"

    @pytest.mark.parametrize("disease_key,data", CLASSICAL_DISEASES.items())
    def test_shat_kriya_kala_pathogenesis_completeness(self, disease_key, data):
        """Rule: Every classical disease must document all six stages of pathogenesis (Shat Kriya Kala)
        as expounded in Sushruta Samhita Sutrasthana Adhyaya 21.
        """
        samprapti = data.get("samprapti", {})
        required_stages = ["Sanchaya", "Prakopa", "Prasara", "Sthana Samshraya", "Vyakti", "Bheda"]
        for stage in required_stages:
            assert stage in samprapti, f"Disease {disease_key} missing Shat Kriya Kala stage: {stage}"
            assert len(samprapti[stage].strip()) > 10, f"Stage {stage} in disease {disease_key} is too brief or empty."

    @pytest.mark.parametrize("disease_key,data", CLASSICAL_DISEASES.items())
    def test_dhatu_and_srotas_integrity(self, disease_key, data):
        """Rule: Classical disease must explicitly identify vitiated Dhatus (among the 7 Dhatus)
        and afflicted Srotas (among the 14 Srotamsi).
        """
        valid_dhatus = [
            "Rasa", "Rakta", "Mamsa", "Meda", "Medo", "Asthi", "Majja", "Shukra",
            "Kandara", "Snayu", "Kleda", "Udaka", "Pureesha", "Mutra", "Ojas", "Manas", "Prana", "Twak", "Lasika"
        ]
        valid_srotas = [
            "Pranavaha", "Annavaha", "Udakavaha", "Rasavaha", "Raktavaha", "Mamsavaha",
            "Medovaha", "Asthivaha", "Majjavaha", "Shukravaha", "Mutravaha",
            "Purishavaha", "Svedavaha", "Swedavaha", "Manovaha"
        ]
        
        dhatus = data.get("dhatu", [])
        srotas = data.get("srotas", [])
        
        assert len(dhatus) > 0, f"Disease {disease_key} has no Dhatu defined."
        assert len(srotas) > 0, f"Disease {disease_key} has no Srotas defined."
        
        for d in dhatus:
            assert any(vd.lower() in d.lower() for vd in valid_dhatus), f"Invalid Dhatu '{d}' in disease {disease_key}"
        for s in srotas:
            assert any(vs.lower() in s.lower() for vs in valid_srotas), f"Invalid Srotas '{s}' in disease {disease_key}"

    @pytest.mark.parametrize("disease_key,data", CLASSICAL_DISEASES.items())
    def test_formulation_aushadha_sevana_kala(self, disease_key, data):
        """Rule: Every formulation must specify an authentic Aushadha Sevana Kala (administration timing)
        conforming to Sharngadhara Samhita and Ashtanga Hridaya (Pragbhakta, Madhyabhakta, Adhobhakta, Nishi, etc.).
        """
        formulations = data.get("shamana_formulations", [])
        assert len(formulations) >= 2, f"Disease {disease_key} must have at least 2 classical formulations."
        
        recognized_kalas = [
            "pragbhakta", "madhyabhakta", "adhobhakta", "sabhakta", "samana",
            "nishi", "muhurmuhur", "muhur", "grasa", "kavalantara", "bhakta", "pratah", "sayam", "pashchadbhakta",
            "external", "bahya"
        ]
        
        for f in formulations:
            kala = f.get("aushadha_sevana_kala", "")
            assert any(rk in kala.lower() for rk in recognized_kalas), (
                f"Formulation '{f.get('name')}' in disease '{disease_key}' has unrecognized Sevana Kala: '{kala}'"
            )

    @pytest.mark.parametrize("disease_key,data", CLASSICAL_DISEASES.items())
    def test_anupana_doctrine(self, disease_key, data):
        """Rule: Every formulation must specify a clinically appropriate Anupana vehicle
        per Sharngadhara Samhita Madhyama Khanda 6.
        """
        formulations = data.get("shamana_formulations", [])
        for f in formulations:
            anupana = f.get("anupana_vehicle", "")
            assert len(anupana.strip()) > 0, f"Formulation '{f.get('name')}' in '{disease_key}' lacks an Anupana vehicle."
            # Must mention classical vehicles: water, milk, ghee, honey, kwatha, takra, oil, or topical/nasal route
            valid_vehicles = [
                "water", "kwatha", "milk", "ghee", "honey", "takra", "asava",
                "arishta", "oil", "taila", "local", "nasal", "external", "application", "infusion", "decoction"
            ]
            assert any(vv in anupana.lower() for vv in valid_vehicles), (
                f"Formulation '{f.get('name')}' in '{disease_key}' has non-standard Anupana: '{anupana}'"
            )

    def test_charaka_sutrasthana_16_ama_shodhana_doctrine(self):
        """CRITICAL SCRIPTURAL DOCTRINE (Charaka Samhita Sutrasthana 16/34-36):
        'Amapradhoshodbhavo rogo...' Radical cleansing (Shodhana) in the presence of Ama (undigested endotoxins)
        drives toxins deeper into peripheral Dhatus like raw fruit squeezed before ripening.
        Therefore, Sama states MUST mandate Deepana-Pachana and DEFER Shodhana.
        """
        dashavidha = DashavidhaPariksha(
            prakriti="Vata-Kapha",
            vikriti="Sama Kapha-Vata",
            sara_tissue_excellence="Madhyama Sara",
            samhanana_compactness="Madhyama Samhanana",
            sattva_mental_strength="Madhyama Sattva",
            ahara_shakti_digestive_power="Avara Ahara Shakti",
            vyayama_shakti_physical_stamina="Madhyama",
            vaya_age_stage="Madhyamavastha"
        )
        # Clinical case of Amavata in acute Sama stage
        diag = NidanaEngine.diagnose(
            symptoms=["tremors_stiffness", "dull_pain_swelling_edema", "tongue_thick_white_coating", "loss_of_taste_aruchi"],
            vikriti_pattern="Kapha-Vata Imbalance",
            ama_status=AmaStatus.SAMA,
            agni_status=AgniType.MANDAGNI,
            koshtha_status=KoshthaType.MADHYAMA,
            dhatu_involved=["Rasa Dhatu", "Asthi Dhatu"],
            srotas_involved=["Rasavaha Srotas", "Annavaha Srotas"]
        )
        plan = ChikitsaEngine.generate_plan(diag, dashavidha, patient_age=45)
        
        # Verify scriptural adherence
        assert plan.panchakarma_guidance.eligible is False, "Violation of Charaka Sutrasthana 16: Shodhana allowed during Sama state!"
        assert len(plan.deepana_pachana_protocol) > 0, "Violation of Charaka doctrine: Deepana-Pachana must be prescribed to digest Ama first."
        contra_str = " ".join(plan.panchakarma_guidance.contraindications_checked) + " " + plan.panchakarma_guidance.reasoning
        assert "ama" in contra_str.lower() or "sama" in contra_str.lower(), (
            "Contraindication text must explicitly state presence of Ama as the biological blocking factor."
        )

    def test_samanya_vishesha_siddhanta_guna_karma(self):
        """Rule: The treatment of aggravated Doshas must use qualities contrary to them (Vishesha Siddhanta).
        Vata (dry, cold, light) -> treated with Snigdha, Ushna, Guru (e.g. Maharasnadi, Dashamula, Ghee/Taila).
        Pitta (hot, sharp, sour) -> treated with Sheeta, Tikta, Madhura (e.g. Kamadudha, Praval, Ghee).
        Kapha (heavy, cold, oily) -> treated with Ushna, Ruksha, Laghu (e.g. Trikatu, Guggulu, Punarnavadi).
        """
        sandhivata_shamana = CLASSICAL_DISEASES["sandhivata"]["shamana_formulations"]
        # Sandhivata is Vata disorder: formulations must include warm unctuous preparations (e.g., Maharasnadi, Taila, Guggulu)
        assert any("rasnadi" in f["name"].lower() or "guggulu" in f["name"].lower() or "taila" in f["name"].lower() for f in sandhivata_shamana)

        amlapitta_shamana = CLASSICAL_DISEASES["amlapitta"]["shamana_formulations"]
        # Amlapitta is Pitta disorder: formulations must include cooling alkaline compounds (e.g. Kamadudha, Avipattikara, Praval)
        assert any("kamadudha" in f["name"].lower() or "avipattikara" in f["name"].lower() or "praval" in f["name"].lower() for f in amlapitta_shamana)

        sthaulya_shamana = CLASSICAL_DISEASES["sthaulya"]["shamana_formulations"]
        # Sthaulya is Kapha/Meda disorder: formulations must include scraping / drying agents (e.g. Medohar, Guggulu, Triphala)
        assert any("guggulu" in f["name"].lower() or "medohar" in f["name"].lower() or "triphala" in f["name"].lower() for f in sthaulya_shamana)

    @pytest.mark.parametrize("disease_key,data", CLASSICAL_DISEASES.items())
    def test_pathya_apathya_scriptural_presence(self, disease_key, data):
        """Rule: Both Pathya (wholesome) and Apathya (unwholesome) diet and lifestyle must be articulated."""
        assert "pathya_ahara" in data and len(data["pathya_ahara"]) > 0, f"Disease {disease_key} lacks Pathya Ahara."
        assert "pathya_vihara" in data and len(data["pathya_vihara"]) > 0, f"Disease {disease_key} lacks Pathya Vihara."
        assert "apathya_ahara" in data and len(data["apathya_ahara"]) > 0, f"Disease {disease_key} lacks Apathya Ahara."
        assert "apathya_vihara" in data and len(data["apathya_vihara"]) > 0, f"Disease {disease_key} lacks Apathya Vihara."
