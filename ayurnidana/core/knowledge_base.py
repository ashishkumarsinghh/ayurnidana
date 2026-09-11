from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class NidanaPanchaka(BaseModel):
    """
    The 5-fold clinical framework for disease diagnosis in Ayurveda.
    """
    nidana_etiology: List[str] = Field(description="Causative factors (diet, lifestyle, environment)")
    purvaroopa_prodromal: List[str] = Field(description="Early warning signs before full manifestation")
    roopa_cardinal: List[str] = Field(description="Primary symptoms of the fully manifested disease")
    upashaya_relieving: List[str] = Field(description="Factors that relieve the symptoms (diet, medicine, habits)")
    samprapti_pathogenesis: str = Field(description="Step-by-step disease progression (how doshas vitiate tissues)")

class ClassicalTreatment(BaseModel):
    """
    Systematic stepwise treatment protocol.
    """
    deepana_pachana: List[str] = Field(description="Herbs/formulations for metabolic fire and toxin digestion")
    shodhana_eligibility: str = Field(description="Criteria and specific Panchakarma therapies recommended")
    shamana_aushadhi: List[str] = Field(description="Primary pacifying herbal formulations (Vati, Kashaya, Asava)")
    pathya_wholesome: List[str] = Field(description="Diet and lifestyle to follow")
    apathya_unwholesome: List[str] = Field(description="Diet and lifestyle to avoid")

class AyurvedicDiseaseProfile(BaseModel):
    """
    Complete classical profile of a disease.
    """
    sanskrit_name: str
    english_correlation: Optional[str]
    dosha_involvement: List[str]
    dushya_tissues: List[str]
    srotas_channels: List[str]
    
    clinical_framework: NidanaPanchaka
    treatment_protocol: ClassicalTreatment

class KnowledgeBase(BaseModel):
    """
    Global knowledge graph tying symptoms to classical texts.
    """
    diseases: Dict[str, AyurvedicDiseaseProfile]

# =====================================================================
# This is the primary data structure where you can port the systematized 
# texts from your Gemini Notebook. 
# 
# The AyurVaidya engine will eventually use this dictionary to cross-reference 
# user symptoms (Roopa/Purvaroopa) and strictly generate treatment plans.
# =====================================================================
CLASSICAL_KNOWLEDGE_BASE = KnowledgeBase(
    diseases={
        # Example entry you can fill out based on your Gemini notebook queries
        "Amlapitta": AyurvedicDiseaseProfile(
            sanskrit_name="Amlapitta",
            english_correlation="Hyperacidity / GERD",
            dosha_involvement=["Pitta", "Vata"],
            dushya_tissues=["Rasa"],
            srotas_channels=["Annavaha Srotas"],
            clinical_framework=NidanaPanchaka(
                nidana_etiology=["Spicy food", "Late nights", "Stress"],
                purvaroopa_prodromal=["Indigestion", "Fatigue"],
                roopa_cardinal=["Heartburn", "Sour belching", "Nausea"],
                upashaya_relieving=["Cold milk", "Sweet tastes"],
                samprapti_pathogenesis="Vitiated Pitta accumulates in the Amashaya..."
            ),
            treatment_protocol=ClassicalTreatment(
                deepana_pachana=["Musta", "Shunthi"],
                shodhana_eligibility="Vamana (Therapeutic emesis) if Kapha is dominant",
                shamana_aushadhi=["Kamadugha Rasa", "Avipattikara Churna"],
                pathya_wholesome=["Ghee", "Amalaki", "Cooling foods"],
                apathya_unwholesome=["Fermented foods", "Chili", "Alcohol"]
            )
        )
    }
)
ALLOPATHIC_MAPPING = {
    "diabetes": {
        "ayurvedic_correlation": "Prameha / Madhumeha",
        "pathology": "Kapha and Medas (fat tissue) aggravation leading to Ojo-kshaya (depletion of immunity and vitality).",
        "treatment_precautions": ["Avoid all forms of sugar and heavy carbohydrates", "Prioritize Tikta (bitter) and Kashaya (astringent) herbs", "Vigorous exercise (Vyayama) is critical"]
    },
    "hypothyroidism": {
        "ayurvedic_correlation": "Kapha-Vata systemic imbalance with Dhatvagni Mandya (Galaganda context)",
        "pathology": "Severe depression of metabolic fire at the tissue level (Dhatvagni) causing systemic Kapha accumulation (weight gain, lethargy) and Vata blockage (dry skin).",
        "treatment_precautions": ["Require strong Deepana-Pachana (Kanchanara Guggulu)", "Avoid cold, heavy, and raw foods", "Focus on Ushna (hot) and Teekshna (penetrating) herbs"]
    },
    "hypertension": {
        "ayurvedic_correlation": "Rakta Gata Vata / Vyana Vayu Dusti",
        "pathology": "Vitiation of Vyana Vata affecting the Rakta Dhatu and circulatory channels (Sira/Dhamani). Often associated with Pitta/Ama blockage.",
        "treatment_precautions": ["Avoid excess Lavana (salt) and Katu (pungent) tastes", "Stress-relieving (Medhya) herbs are mandatory (e.g., Jatamansi, Brahmi)", "Mild Shodhana (Virechana) is highly beneficial"]
    },
    "pcos": {
        "ayurvedic_correlation": "Artava Kshaya / Pushpaghni Jataharini",
        "pathology": "Kapha and Vata blocking the Artavavaha Srotas (female reproductive channels) leading to cyst formation and irregular cycles.",
        "treatment_precautions": ["Avoid dairy and heavy sweets", "Vata-anulomana and Kapha-lekhana therapy", "Use herbs like Shatavari, Aloe Vera, and Varuna"]
    }
}
