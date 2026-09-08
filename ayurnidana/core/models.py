from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Gender(str, Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'

class Dosha(str, Enum):
    VATA = 'Vata'
    PITTA = 'Pitta'
    KAPHA = 'Kapha'

class PrakritiType(str, Enum):
    VATA = 'Vata Dominant'
    PITTA = 'Pitta Dominant'
    KAPHA = 'Kapha Dominant'
    VATA_PITTA = 'Vata-Pitta'
    PITTA_KAPHA = 'Pitta-Kapha'
    VATA_KAPHA = 'Vata-Kapha'
    SAMA_TRIDOSHA = 'Sama Doshaja (Balanced Tridosha)'

class AgniType(str, Enum):
    SAMAGNI = 'Samagni (Balanced Digestive Fire)'
    VISHAMAGNI = 'Vishamagni (Irregular/Fluctuating - Vata)'
    TIKSHNAGNI = 'Tikshnagni (Hyperactive/Intense - Pitta)'
    MANDAGNI = 'Mandagni (Sluggish/Slow - Kapha/Ama)'

class KoshthaType(str, Enum):
    MRIDU = 'Mridu Koshtha (Soft/Fast Bowel - Pitta)'
    MADHYAMA = 'Madhyama Koshtha (Moderate/Regular Bowel - Kapha/Balanced)'
    KRURA = 'Krura Koshtha (Hard/Constipated Bowel - Vata)'

class AmaStatus(str, Enum):
    NIRAMA = 'Nirama (Free of Metabolic Endotoxins)'
    MILD_AMA = 'Alpa-Ama (Mild Endotoxin Accumulation)'
    SAMA = 'Sama (Significant Ama / Toxic Accumulation)'

class Prognosis(str, Enum):
    SUKHA_SADHYA = 'Sukha Sadhya (Easily Curable)'
    KRICHHRA_SADHYA = 'Krichhra Sadhya (Curable with Difficulty)'
    YAPYA = 'Yapya (Manageable / Chronic)'
    PRATYAKHYEYA = 'Pratyakhyeya (Incurable / Advanced)'

class PatientDemographics(BaseModel):
    name: str
    age: int
    gender: Gender
    occupation: Optional[str] = ''
    geographical_region: Optional[str] = ''
    current_season: str = 'Sharad (Autumn)'

class AshtaSthanaPariksha(BaseModel):
    nadi_pulse: str = Field(..., description='Gati (Sarpa/Manduka/Hamsa), rate, rhythm')
    jihva_tongue: str = Field(..., description='Coating, color, dryness, cracks, impressions')
    mutra_urine: str = Field(..., description='Color, clarity, frequency, sensation')
    mala_stool: str = Field(..., description='Consistency, frequency, sinking/floating (ama test)')
    shabda_voice: str = Field(..., description='Tone, clarity, hoarseness, abdominal sounds')
    sparsha_skin: str = Field(..., description='Temperature, texture, dryness, perspiration')
    druk_eyes: str = Field(..., description='Sclera color, luster, dryness, swelling')
    akruti_appearance: str = Field(..., description='Habitus, posture, facial expression, gait')

class DashavidhaPariksha(BaseModel):
    prakriti: str
    vikriti: str
    sara_tissue_excellence: str = 'Madhyama (Moderate)'
    samhanana_compactness: str = 'Madhyama (Moderate)'
    pramana_body_proportions: str = 'Prakrita (Normal)'
    satmya_habituation: str = 'Vyamiara (Mixed)'
    sattva_mental_strength: str = 'Pravara (Strong) / Madhyama (Moderate)'
    ahara_shakti_digestive_power: str
    vyayama_shakti_physical_stamina: str
    vaya_age_stage: str

class NidanaPanchaka(BaseModel):
    nidana_etiology: List[str] = Field(default_factory=list, description='Aharaja, Viharaja, and Manasika causative factors')
    purvarupa_prodromes: List[str] = Field(default_factory=list, description='Premonitory indicators')
    rupa_cardinal_symptoms: List[str] = Field(default_factory=list, description='Manifest clinical signs')
    upashaya_anupashaya: Dict[str, List[str]] = Field(default_factory=dict, description='Alleviating vs aggravating factors')
    samprapti_pathogenesis: Dict[str, str] = Field(default_factory=dict, description='Shat Kriya Kala progression')

class Formulation(BaseModel):
    name: str
    category: str = Field(..., description='Churna, Vati, Kwatha, Asava, Ghrita, Rasayana, Bhasma')
    classical_indication: str
    dosage: str
    anupana_vehicle: str
    aushadha_sevana_kala: str = Field(..., description='Classical timing relative to meals')
    duration_weeks: int
    classical_reference: str

class PanchakarmaPrescription(BaseModel):
    eligible: bool
    recommended_therapy: str
    reasoning: str
    purvakarma: List[str] = Field(default_factory=list, description='Snehana, Swedana, Deepana')
    pradhanakarma: str
    paschatkarma: List[str] = Field(default_factory=list, description='Samsarjana Krama, dietetic schedule')
    contraindications_checked: List[str] = Field(default_factory=list)

class PathyaApathya(BaseModel):
    pathya_ahara_wholesome_diet: List[str]
    apathya_ahara_unwholesome_diet: List[str]
    pathya_vihara_recommended_lifestyle: List[str]
    apathya_vihara_contraindicated_habits: List[str]
    viruddha_ahara_warnings: List[str]
    yoga_and_pranayama: List[str]

class DiagnosisResult(BaseModel):
    primary_condition: str
    sanskrit_name: str
    doshic_subtype: str
    secondary_conditions: List[str] = Field(default_factory=list)
    dhatu_involved: List[str] = Field(default_factory=list)
    srotas_involved: List[str] = Field(default_factory=list)
    ama_status: AmaStatus
    agni_status: AgniType
    koshtha_status: KoshthaType
    prognosis: Prognosis
    nidana_panchaka: NidanaPanchaka
    clinical_reasoning: str
    classical_citations: List[str] = Field(default_factory=list)

class TreatmentPlan(BaseModel):
    deepana_pachana_protocol: List[str]
    shamana_formulations: List[Formulation]
    panchakarma_guidance: PanchakarmaPrescription
    dietary_and_lifestyle_regimen: PathyaApathya
    rasayana_recovery_plan: List[str]
    red_flag_warnings: List[str] = Field(default_factory=list)
    follow_up_recommendation: str

class ClinicalCase(BaseModel):
    patient: PatientDemographics
    ashta_sthana: AshtaSthanaPariksha
    dashavidha: DashavidhaPariksha
    chief_complaints: List[str]
    onset_and_duration: str
    dosha_scores: Dict[str, float]
    diagnosis: DiagnosisResult
    treatment: TreatmentPlan

DiseaseDiagnosis = DiagnosisResult
