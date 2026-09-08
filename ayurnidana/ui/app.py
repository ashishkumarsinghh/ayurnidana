"""AyurNidana - Interactive Ayurvedic Clinical Diagnostic & Treatment Expert System.
Integrates classical Ayurvedic methodology with Google NotebookLM and local treatise knowledge base.
"""
import sys
import os

# Ensure the root project directory is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import json

from ayurnidana.core.models import (
    PatientDemographics, AshtaSthanaPariksha, DashavidhaPariksha,
    Gender, AgniType, KoshthaType, AmaStatus, Prognosis, PrakritiType, ClinicalCase
)
from ayurnidana.core.dosha_engine import DoshaEngine
from ayurnidana.core.ashta_sthana import ASHTA_STHANA_CATALOG, AshtaSthanaEvaluator
from ayurnidana.core.dashavidha import DASHAVIDHA_CRITERIA, DashavidhaEvaluator
from ayurnidana.core.nidana_engine import NidanaEngine
from ayurnidana.core.chikitsa_engine import ChikitsaEngine
from ayurnidana.knowledge.notebook_bridge import NotebookBridge
from ayurnidana.knowledge.local_library import LocalAyurvedaLibrary
from ayurnidana.knowledge.ai_consultant import AIConsultant
from ayurnidana.ui.components.style import CUSTOM_CSS
from ayurnidana.ui.components.charts import get_dosha_df
from ayurnidana.ui.components.case_sheet import generate_markdown_case_sheet

st.set_page_config(
    page_title="AyurNidana - Ayurvedic Clinical Expert System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize singletons in session state
if "notebook_bridge" not in st.session_state:
    st.session_state.notebook_bridge = NotebookBridge(target_notebook_name="ayurveda")
if "library" not in st.session_state:
    st.session_state.library = LocalAyurvedaLibrary()
if "ai_consultant" not in st.session_state:
    st.session_state.ai_consultant = AIConsultant()

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("<h2 style='color:#8C4318; font-family:serif;'>🌿 AyurNidana</h2>", unsafe_allow_html=True)
    st.caption("रोगमादौ परीक्षेत ततोऽनन्तरमौषधम्")
    st.markdown("---")

    # NotebookLM Connection Widget
    st.subheader("📓 NotebookLM Status")
    bridge = st.session_state.notebook_bridge
    auth_status = bridge.check_auth()
    
    if auth_status["authenticated"]:
        st.success("Google NotebookLM: Session Active")
        conn_res = bridge.connect_to_ayurveda_notebook()
        if conn_res["connected"]:
            st.info(f"Target: **{conn_res['title']}** (ID: `{conn_res['notebook_id'][:8]}...`)")
        else:
            st.warning("Notebook 'ayurveda' ready for sync")
    else:
        st.warning("NotebookLM CLI: Not signed in")
        st.caption("Run `notebooklm login` in terminal to sync with cloud notebooks.")

    # Local Library Status
    st.markdown("---")
    st.subheader("📚 Classical Treatises")
    lib = st.session_state.library
    lib_stat = lib.get_library_status()
    if lib_stat["available"]:
        st.success(f"{lib_stat['total_treatises']} Texts Indexed ({lib_stat['uploaded_count']} uploaded)")
        with st.expander("Key Samhitas Detected"):
            for s in lib_stat["key_samhitas"]:
                st.write(f"• {s}")
    else:
        st.info("Local library path configured")

    # Preset Patient Case Loader
    st.markdown("---")
    st.subheader("⚡ Load Clinical Presets")
    preset = st.selectbox(
        "Select Clinical Archetype:",
        [
            "Custom Patient Case",
            "Sandhivata (Degenerative Joint Osteoarthritis)",
            "Amavata (Autoimmune Rheumatoid Arthritis with Ama)",
            "Amlapitta (Hyperacidity & Esophageal Reflux)",
            "Prameha (Type 2 Diabetes & Metabolic Syndrome)"
        ]
    )

# ----------------- MAIN TITLE -----------------
st.markdown("<div class='main-title'>AYURNIDANA EXPERT SYSTEM</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Systematic Ayurvedic Clinical Examination, Nidana Panchaka & Chikitsa Protocol</div>", unsafe_allow_html=True)

# Preset logic
default_name = "Rajesh Kumar"
default_age = 54
default_gender = Gender.MALE
default_complaints = "Severe right knee joint pain with crepitus and early morning stiffness."
default_duration = "8 months, worsening during cold weather"
default_symptoms = ["joint_pain_cracking", "pain_sharp_throbbing", "tremors_stiffness", "dryness_skin_hair"]
default_nadi = ASHTA_STHANA_CATALOG["nadi"]["options"][0][0]
default_jihva = ASHTA_STHANA_CATALOG["jihva"]["options"][0][0]
default_mala = ASHTA_STHANA_CATALOG["mala"]["options"][0][0]
default_agni = AgniType.VISHAMAGNI
default_koshtha = KoshthaType.KRURA

if "Amavata" in preset:
    default_name = "Sunita Verma"
    default_age = 42
    default_gender = Gender.FEMALE
    default_complaints = "Severe symmetrical pain and swelling in wrists, fingers, and knees. Extreme morning stiffness lasting >1 hour, lethargy, feverish feeling."
    default_duration = "4 months"
    default_symptoms = ["joint_pain_cracking", "dull_pain_swelling_edema", "heaviness_body_limbs", "fever", "tongue_thick_white_coating", "loss_of_taste_aruchi"]
    default_nadi = ASHTA_STHANA_CATALOG["nadi"]["options"][3][0]
    default_jihva = ASHTA_STHANA_CATALOG["jihva"]["options"][3][0]
    default_mala = ASHTA_STHANA_CATALOG["mala"]["options"][2][0]
    default_agni = AgniType.MANDAGNI
    default_koshtha = KoshthaType.MADHYAMA
elif "Amlapitta" in preset:
    default_name = "Amit Sharma"
    default_age = 35
    default_gender = Gender.MALE
    default_complaints = "Retrosternal burning sensation, sour water brash, nausea after meals, epigastric discomfort, and irritability."
    default_duration = "6 months"
    default_symptoms = ["burning_sensation", "acid_reflux_heartburn", "intense_sharp_hunger", "yellowish_eyes_urine", "irritability_anger"]
    default_nadi = ASHTA_STHANA_CATALOG["nadi"]["options"][1][0]
    default_jihva = ASHTA_STHANA_CATALOG["jihva"]["options"][1][0]
    default_mala = ASHTA_STHANA_CATALOG["mala"]["options"][1][0]
    default_agni = AgniType.TIKSHNAGNI
    default_koshtha = KoshthaType.MRIDU
elif "Prameha" in preset:
    default_name = "Vikram Singh"
    default_age = 49
    default_gender = Gender.MALE
    default_complaints = "Frequent urination especially at night, profuse turbid urine, excessive thirst, lethargy, sweet taste in mouth, weight gain."
    default_duration = "1 year"
    default_symptoms = ["excessive_thirst_sweating", "heaviness_body_limbs", "weight_gain_slow_metabolism", "tongue_thick_white_coating", "burning_sensation"]
    default_nadi = ASHTA_STHANA_CATALOG["nadi"]["options"][2][0]
    default_jihva = ASHTA_STHANA_CATALOG["jihva"]["options"][2][0]
    default_mala = ASHTA_STHANA_CATALOG["mala"]["options"][3][0]
    default_agni = AgniType.MANDAGNI
    default_koshtha = KoshthaType.MADHYAMA

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌿 1. Rogi Pariksha (Clinical Intake)",
    "🔍 2. Nidana (Diagnosis & Pathology)",
    "💊 3. Chikitsa (Treatment Blueprint)",
    "📚 4. NotebookLM & Library Explorer",
    "📋 5. Case Sheet & Prescription"
])

# ----------------- TAB 1: CLINICAL INTAKE -----------------
with tab1:
    st.markdown("### I. Patient Demographics & Presenting Complaints")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        patient_name = st.text_input("Patient Name", value=default_name)
    with col2:
        patient_age = st.number_input("Age (Years)", min_value=1, max_value=110, value=default_age)
    with col3:
        patient_gender = st.selectbox("Gender", [Gender.MALE, Gender.FEMALE, Gender.OTHER], index=0 if default_gender == Gender.MALE else 1)
    with col4:
        season = st.selectbox("Current Season (Ritu)", ["Sharad (Autumn)", "Hemanta (Late Autumn)", "Shishira (Winter)", "Vasanta (Spring)", "Grishma (Summer)", "Varsha (Monsoon)"])

    colA, colB = st.columns([2, 1])
    with colA:
        chief_complaints = st.text_area("Chief Complaints (Pradhana Vedana)", value=default_complaints, height=80)
    with colB:
        duration = st.text_input("Onset & Duration (Kala)", value=default_duration)
        region = st.text_input("Geographical Region / Desha", value="Sadharana Desha (Temperate)")

    st.markdown("---")
    st.markdown("### II. Rupa & Lakshana (Systemic Symptoms Checklist)")
    
    symptom_options = {
        "Vata Provocation": [
            ("joint_pain_cracking", "Joint Pain with Crepitus & Cracking (Sandhishoola & Atopa)"),
            ("pain_sharp_throbbing", "Severe Sharp / Radiating Pain (Toda / Bheda)"),
            ("tremors_stiffness", "Stiffness, Spasms, or Tremors (Stambha & Kampa)"),
            ("constipation_hard_stools", "Dry, Hard, Constipated Bowels (Vibandha)"),
            ("bloating_flatulence", "Abdominal Distension & Flatulence (Adhmana)"),
            ("insomnia_disturbed_sleep", "Insomnia / Fragmented Sleep (Anidra)"),
            ("anxiety_restlessness", "Anxiety, Restlessness & Racing Thoughts (Chittodvega)"),
            ("dryness_skin_hair", "Dry Rough Skin and Brittle Hair (Rookshata)")
        ],
        "Pitta Provocation": [
            ("burning_sensation", "Burning Sensation in Palms, Soles, or Chest (Daha)"),
            ("acid_reflux_heartburn", "Acid Reflux, Sour Eructations (Amlodgara)"),
            ("intense_sharp_hunger", "Hyperactive Intense Hunger (Tikshnagni)"),
            ("skin_rashes_inflammation_acne", "Skin Rashes, Acne, or Erythema (Rakta Pitta)"),
            ("loose_stools_diarrhea", "Frequent Loose Stools with Burning (Atisara)"),
            ("yellowish_eyes_urine", "Yellowish Tint in Sclera or Urine (Peetatva)"),
            ("irritability_anger", "Excessive Irritability, Anger, & Short Temper (Krodha)")
        ],
        "Kapha & Ama Provocation": [
            ("heaviness_body_limbs", "Profound Heaviness in Head and Limbs (Gaurava)"),
            ("excess_mucus_congestion", "Productive Cough or Nasal Congestion (Kaphotklesha)"),
            ("dull_pain_swelling_edema", "Dull Deep Swelling or Effusion (Shotha)"),
            ("weight_gain_slow_metabolism", "Weight Gain / Adiposity (Medovriddhi)"),
            ("fever", "Feverishness / Elevated Temperature (Jwara)"),
            ("tongue_thick_white_coating", "Thick White Greasy Tongue Coating (Sama Jihva)"),
            ("loss_of_taste_aruchi", "Total Anorexia / Bad Taste in Mouth (Aruchi)")
        ]
    }

    selected_symptoms = []
    scol1, scol2, scol3 = st.columns(3)
    
    with scol1:
        st.markdown("**Vata Lakshanas**")
        for sym_id, label in symptom_options["Vata Provocation"]:
            checked = sym_id in default_symptoms
            if st.checkbox(label, value=checked, key=f"v_{sym_id}"):
                selected_symptoms.append(sym_id)

    with scol2:
        st.markdown("**Pitta Lakshanas**")
        for sym_id, label in symptom_options["Pitta Provocation"]:
            checked = sym_id in default_symptoms
            if st.checkbox(label, value=checked, key=f"p_{sym_id}"):
                selected_symptoms.append(sym_id)

    with scol3:
        st.markdown("**Kapha & Ama Lakshanas**")
        for sym_id, label in symptom_options["Kapha & Ama Provocation"]:
            checked = sym_id in default_symptoms
            if st.checkbox(label, value=checked, key=f"k_{sym_id}"):
                selected_symptoms.append(sym_id)

    st.markdown("---")
    st.markdown("### III. Ashta Sthana Pariksha (Eight-Fold Clinical Examination)")
    
    c_nadi, c_jihva = st.columns(2)
    with c_nadi:
        nadi_val = st.selectbox(
            "1. Nadi Pariksha (Pulse Examination)",
            [opt[0] for opt in ASHTA_STHANA_CATALOG["nadi"]["options"]],
            index=0 if "Sarpa" in default_nadi else 3
        )
    with c_jihva:
        jihva_val = st.selectbox(
            "2. Jihva Pariksha (Tongue Examination)",
            [opt[0] for opt in ASHTA_STHANA_CATALOG["jihva"]["options"]],
            index=0 if "Dry" in default_jihva else (3 if "greasy" in default_jihva or "Heavy" in default_jihva else 1)
        )

    c_mutra, c_mala = st.columns(2)
    with c_mutra:
        mutra_val = st.selectbox(
            "3. Mutra Pariksha (Urine Examination)",
            [opt[0] for opt in ASHTA_STHANA_CATALOG["mutra"]["options"]],
            index=0
        )
    with c_mala:
        mala_val = st.selectbox(
            "4. Mala Pariksha (Stool & Ama Float Test)",
            [opt[0] for opt in ASHTA_STHANA_CATALOG["mala"]["options"]],
            index=0 if "Krura" in default_mala else (2 if "Sama" in default_mala else 1)
        )

    c_shabda, c_sparsha = st.columns(2)
    with c_shabda:
        shabda_val = st.selectbox(
            "5. Shabda Pariksha (Voice & Sounds)",
            [opt[0] for opt in ASHTA_STHANA_CATALOG["shabda"]["options"]],
            index=0
        )
    with c_sparsha:
        sparsha_val = st.selectbox(
            "6. Sparsha Pariksha (Skin Touch & Temp)",
            [opt[0] for opt in ASHTA_STHANA_CATALOG["sparsha"]["options"]],
            index=0
        )

    c_druk, c_akruti = st.columns(2)
    with c_druk:
        druk_val = st.selectbox(
            "7. Druk Pariksha (Eyes & Vision)",
            [opt[0] for opt in ASHTA_STHANA_CATALOG["druk"]["options"]],
            index=0
        )
    with c_akruti:
        akruti_val = st.selectbox(
            "8. Akruti Pariksha (Body Habitus & Gait)",
            [opt[0] for opt in ASHTA_STHANA_CATALOG["akruti"]["options"]],
            index=0
        )

    st.markdown("---")
    st.markdown("### IV. Dashavidha Pariksha (Constitutional & Functional Reserves)")
    dcol1, dcol2, dcol3 = st.columns(3)
    with dcol1:
        sara_val = st.selectbox("Sara (Tissue Excellence)", DASHAVIDHA_CRITERIA["sara"]["options"], index=1)
        samhanana_val = st.selectbox("Samhanana (Body Compactness)", DASHAVIDHA_CRITERIA["samhanana"]["options"], index=1)
    with dcol2:
        sattva_val = st.selectbox("Sattva (Mental Resilience)", DASHAVIDHA_CRITERIA["sattva"]["options"], index=1)
        ahara_val = st.selectbox("Ahara Shakti (Digestive Capacity)", DASHAVIDHA_CRITERIA["ahara_shakti"]["options"], index=1)
    with dcol3:
        vyayama_val = st.selectbox("Vyayama Shakti (Physical Stamina)", DASHAVIDHA_CRITERIA["vyayama_shakti"]["options"], index=1)
        koshtha_val = st.selectbox("Koshtha (Bowel Habit)", [k.value for k in KoshthaType], index=2 if default_koshtha == KoshthaType.KRURA else 1)

# Construct data models
patient_demo = PatientDemographics(
    name=patient_name,
    age=patient_age,
    gender=patient_gender,
    occupation="Professional",
    geographical_region=region,
    current_season=season
)

ashta_findings = AshtaSthanaPariksha(
    nadi_pulse=nadi_val,
    jihva_tongue=jihva_val,
    mutra_urine=mutra_val,
    mala_stool=mala_val,
    shabda_voice=shabda_val,
    sparsha_skin=sparsha_val,
    druk_eyes=druk_val,
    akruti_appearance=akruti_val
)

dashavidha_findings = DashavidhaPariksha(
    prakriti="Vata-Pitta",
    vikriti="Pending Evaluation",
    sara_tissue_excellence=sara_val,
    samhanana_compactness=samhanana_val,
    sattva_mental_strength=sattva_val,
    ahara_shakti_digestive_power=ahara_val,
    vyayama_shakti_physical_stamina=vyayama_val,
    vaya_age_stage="Madhyamavastha"
)

# Run Diagnostic Engine
dosha_percentages, vikriti_pattern = DoshaEngine.calculate_vikriti(selected_symptoms)
ama_status, ama_findings = DoshaEngine.assess_ama(selected_symptoms, jihva_val)
dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(selected_symptoms)

# Determine Agni
if "Tikshnagni" in ahara_val or "burning" in " ".join(selected_symptoms):
    agni_status = AgniType.TIKSHNAGNI
elif "Mandagni" in ahara_val or ama_status == AmaStatus.SAMA:
    agni_status = AgniType.MANDAGNI
elif "Vishamagni" in ahara_val or "bloating" in " ".join(selected_symptoms):
    agni_status = AgniType.VISHAMAGNI
else:
    agni_status = AgniType.SAMAGNI

# Determine Koshtha
koshtha_enum = KoshthaType.MADHYAMA
if "Krura" in koshtha_val or "constipation" in " ".join(selected_symptoms):
    koshtha_enum = KoshthaType.KRURA
elif "Mridu" in koshtha_val or "loose" in " ".join(selected_symptoms):
    koshtha_enum = KoshthaType.MRIDU

# Run Roga Diagnosis
diagnosis_result = NidanaEngine.diagnose(
    symptoms=selected_symptoms,
    vikriti_pattern=vikriti_pattern,
    ama_status=ama_status,
    agni_status=agni_status,
    koshtha_status=koshtha_enum,
    dhatu_involved=dhatus,
    srotas_involved=srotas
)

# Run Treatment Engine
treatment_plan = ChikitsaEngine.generate_plan(
    diagnosis=diagnosis_result,
    dashavidha=dashavidha_findings,
    patient_age=patient_age,
    season=season
)

# ----------------- TAB 2: NIDANA (DIAGNOSIS) -----------------
with tab2:
    st.markdown("### I. Comprehensive Diagnostic Summary")
    
    r_col1, r_col2 = st.columns([2, 1])
    with r_col1:
        st.markdown(f"""
        <div class='ayur-card-gold'>
            <h3 style='margin:0; color:#B45309;'>{diagnosis_result.primary_condition} ({diagnosis_result.sanskrit_name})</h3>
            <p style='margin:4px 0 0 0; font-size:1.05rem; color:#4B5563;'>
                <strong>Doshic Profile:</strong> {diagnosis_result.doshic_subtype} &bull; 
                <strong>Ama Status:</strong> {diagnosis_result.ama_status.value} &bull; 
                <strong>Agni:</strong> {diagnosis_result.agni_status.value}
            </p>
            <p style='margin:8px 0 0 0; font-size:0.95rem; color:#374151;'>{diagnosis_result.clinical_reasoning}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Classical Treatises Citations:**")
        for cit in diagnosis_result.classical_citations:
            st.markdown(f"📖 *{cit}*")

    with r_col2:
        st.markdown("#### Doshic Provocation Ratio")
        df_dosha = get_dosha_df(dosha_percentages)
        st.bar_chart(df_dosha.set_index("Dosha")["Percentage (%)"])
        
        v_pct = dosha_percentages.get("Vata", 0)
        p_pct = dosha_percentages.get("Pitta", 0)
        k_pct = dosha_percentages.get("Kapha", 0)
        st.markdown(f"""
        <span class='dosha-badge-vata'>Vata: {v_pct}%</span>
        <span class='dosha-badge-pitta'>Pitta: {p_pct}%</span>
        <span class='dosha-badge-kapha'>Kapha: {k_pct}%</span>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### II. Nidana Panchaka (The Five Diagnostic Pillars)")
    
    np1, np2, np3 = st.columns(3)
    with np1:
        st.markdown("#### 1. Nidana (Etiology / Hetu)")
        for n in diagnosis_result.nidana_panchaka.nidana_etiology:
            st.markdown(f"• {n}")
        st.markdown("#### 2. Purvarupa (Prodromes)")
        for pr in diagnosis_result.nidana_panchaka.purvarupa_prodromes:
            st.markdown(f"• {pr}")

    with np2:
        st.markdown("#### 3. Rupa (Manifest Cardinal Signs)")
        for r in diagnosis_result.nidana_panchaka.rupa_cardinal_symptoms:
            st.markdown(f"• **{r.replace('_', ' ').title()}**")
        st.markdown("#### 4. Upashaya / Anupashaya")
        for u_type, u_items in diagnosis_result.nidana_panchaka.upashaya_anupashaya.items():
            st.markdown(f"**{u_type}:**")
            for item in u_items:
                st.markdown(f"- {item}")

    with np3:
        st.markdown("#### 5. Samprapti (Shat Kriya Kala)")
        for stage, desc in diagnosis_result.nidana_panchaka.samprapti_pathogenesis.items():
            st.markdown(f"**{stage}:** {desc}")

    st.markdown("---")
    st.markdown("### III. Dhatus, Srotas & Prognosis")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("**Vitiated Dhatus:**")
        for dh in diagnosis_result.dhatu_involved:
            st.markdown(f"<span class='pill-tag'>{dh}</span>", unsafe_allow_html=True)
    with d2:
        st.markdown("**Vitiated Srotas (Channels):**")
        for sr in diagnosis_result.srotas_involved:
            st.markdown(f"<span class='pill-tag'>{sr}</span>", unsafe_allow_html=True)
    with d3:
        st.markdown("**Prognosis (Sadhya-Asadhyata):**")
        st.info(f"**{diagnosis_result.prognosis.value}**")

# ----------------- TAB 3: CHIKITSA (TREATMENT) -----------------
with tab3:
    st.markdown("### I. Systematic Multi-Tier Ayurvedic Treatment Blueprint")
    
    # Phase 1: Deepana & Pachana
    with st.expander("🔥 Phase 1: Deepana & Pachana Protocol (Metabolic Correction)", expanded=True):
        st.markdown("<div class='ayur-card-gold'>", unsafe_allow_html=True)
        st.markdown("**Primary Objective:** Kindle Jatharagni and digest circulating Ama before administering heavy tonics or radical Shodhana.")
        for item in treatment_plan.deepana_pachana_protocol:
            st.markdown(f"• {item}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Phase 2: Shamana Formulations Table
    st.markdown("### 🌿 Phase 2: Shamana Chikitsa (Prescribed Formulations)")
    f_data = []
    for f in treatment_plan.shamana_formulations:
        f_data.append({
            "Medicine Name": f.name,
            "Form / Category": f.category,
            "Classical Indication": f.classical_indication,
            "Dosage": f.dosage,
            "Anupana (Vehicle)": f.anupana_vehicle,
            "Aushadha Kala (Timing)": f.aushadha_sevana_kala,
            "Duration": f"{f.duration_weeks} Weeks",
            "Classical Reference": f.classical_reference
        })
    st.dataframe(pd.DataFrame(f_data), use_container_width=True, hide_index=True)

    # Phase 3: Panchakarma Guidance
    with st.expander("💧 Phase 3: Shodhana / Panchakarma Protocol & Eligibility", expanded=True):
        pk = treatment_plan.panchakarma_guidance
        if pk.eligible:
            st.success(f"**Patient Eligible for Shodhana:** {pk.recommended_therapy}")
            st.markdown(f"**Therapeutic Rationale:** {pk.reasoning}")
            
            pcol1, pcol2, pcol3 = st.columns(3)
            with pcol1:
                st.markdown("**Purvakarma (Preparation):**")
                for item in pk.purvakarma:
                    st.write(f"• {item}")
            with pcol2:
                st.markdown("**Pradhanakarma (Main Procedure):**")
                st.write(f"**{pk.pradhanakarma}**")
            with pcol3:
                st.markdown("**Paschatkarma (Aftercare):**")
                for item in pk.paschatkarma:
                    st.write(f"• {item}")
        else:
            st.warning(f"**Shodhana Deferred / Ineligible:** {pk.recommended_therapy}")
            st.markdown(f"**Contraindication Factors Checked:** {pk.reasoning}")

    # Phase 4: Pathya & Apathya (Diet & Lifestyle)
    st.markdown("### 🥗 Phase 4: Pathya & Apathya Regimen")
    pcol_a, pcol_b = st.columns(2)
    with pcol_a:
        st.markdown("<div class='ayur-card-green'>", unsafe_allow_html=True)
        st.markdown("#### Wholesome Regimen (Pathya)")
        st.markdown("**Wholesome Diet (Pathya Ahara):**")
        for item in treatment_plan.dietary_and_lifestyle_regimen.pathya_ahara_wholesome_diet:
            st.write(f"✓ {item}")
        st.markdown("**Recommended Lifestyle (Pathya Vihara):**")
        for item in treatment_plan.dietary_and_lifestyle_regimen.pathya_vihara_recommended_lifestyle:
            st.write(f"✓ {item}")
        st.markdown("</div>", unsafe_allow_html=True)

    with pcol_b:
        st.markdown("<div class='ayur-card-red'>", unsafe_allow_html=True)
        st.markdown("#### Prohibited Regimen (Apathya)")
        st.markdown("**Unwholesome Diet (Apathya Ahara):**")
        for item in treatment_plan.dietary_and_lifestyle_regimen.apathya_ahara_unwholesome_diet:
            st.write(f"✗ {item}")
        st.markdown("**Harmful Lifestyle Habits (Apathya Vihara):**")
        for item in treatment_plan.dietary_and_lifestyle_regimen.apathya_vihara_contraindicated_habits:
            st.write(f"✗ {item}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Viruddha Ahara Warnings
    st.markdown("#### ⚠️ Viruddha Ahara (Strict Incompatible Food Combinations)")
    for warning in treatment_plan.dietary_and_lifestyle_regimen.viruddha_ahara_warnings:
        st.markdown(f"• **Alert:** {warning}")

    # Yoga & Pranayama
    st.markdown("#### 🧘 Prescribed Yoga & Pranayama Therapy")
    for y in treatment_plan.dietary_and_lifestyle_regimen.yoga_and_pranayama:
        st.markdown(f"• {y}")

    # Red Flags & Triage
    if treatment_plan.red_flag_warnings:
        st.markdown("<div class='ayur-card-red'>", unsafe_allow_html=True)
        st.markdown("#### 🚨 Modern Clinical Red Flags & Emergency Referral Criteria")
        st.markdown("If the patient presents with any of the following acute symptoms, immediately refer to emergency allopathic medical facilities:")
        for rf in treatment_plan.red_flag_warnings:
            st.markdown(f"• **[EMERGENCY ALERT]** {rf}")
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 4: NOTEBOOKLM & TREATISE EXPLORER -----------------
with tab4:
    st.markdown("### 📓 Google NotebookLM & Classical Treatises Co-Pilot")
    st.markdown("Ask deep clinical questions directly to your **'ayurveda'** notebook and 100+ classical treatises.")

    nb_col1, nb_col2 = st.columns([1, 2])
    with nb_col1:
        st.markdown("#### Connection Dashboard")
        st.write(f"**Target Notebook:** `ayurveda`")
        if auth_status["authenticated"]:
            st.success("✅ Google NotebookLM: Connected")
            conn = bridge.connect_to_ayurveda_notebook()
            if conn["connected"]:
                st.info(f"Active: **{conn['title']}** (`{conn['notebook_id'][:8]}...`)")
            else:
                st.warning("Notebook 'ayurveda' ready for queries")
        else:
            st.warning("⚠️ Google NotebookLM: Login Required")
            if st.button("🔑 Launch Google Sign-In Window", type="primary"):
                import subprocess
                try:
                    subprocess.Popen([
                        "cmd.exe", "/c", "start", "powershell", "-NoExit", "-Command",
                        "python -m notebooklm login"
                    ])
                    st.info("Opened login terminal on your desktop. Complete sign-in, then click 'Refresh Status'.")
                except Exception as e:
                    st.error(f"Error launching login: {e}")

            if st.button("🔄 Refresh Status"):
                st.rerun()

        custom_nb_id = st.text_input("Or enter Notebook ID directly (optional):", value=bridge.active_notebook_id or "")
        if custom_nb_id:
            bridge.active_notebook_id = custom_nb_id
            st.caption(f"Target Notebook ID set to: `{custom_nb_id}`")

        st.markdown("#### Search Local Classical Treatises")
        search_kw = st.text_input("Search Charaka, Sushruta, Madhava Nidana, etc.:", value="Sandhivata")
        if search_kw:
            hits = lib.search_treatises(search_kw)
            if hits:
                st.write(f"Found {len(hits)} matching files:")
                for h in hits:
                    st.caption(f"📖 **{h['filename']}** ({h['folder']})")
            else:
                st.caption("No direct filename matches found.")

    with nb_col2:
        st.markdown("#### Clinical Inquiry & Treatise Synthesis")
        sample_query = f"Provide classical Chikitsa Sutra and Samprapti breakdown for {diagnosis_result.primary_condition} ({diagnosis_result.sanskrit_name}) with specific shloka citations from Charaka and Madhava Nidana."
        user_query = st.text_area("Enter your clinical query for NotebookLM / Classical AI:", value=sample_query, height=100)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            ask_nb_btn = st.button("Query NotebookLM 'ayurveda'")
        with btn_col2:
            ask_ai_btn = st.button("Consult AI Vaidya (Gemini 2.5 Grounded)", type="primary")

        if ask_nb_btn:
            with st.spinner("Querying Google NotebookLM 'ayurveda'..."):
                res = bridge.ask_notebook(user_query)
                if res.get("success"):
                    st.success(f"Response from {res.get('source')}:")
                    st.markdown(res.get("answer"))
                else:
                    st.warning(f"NotebookLM CLI response: {res.get('error')}")
                    st.info("Falling back to Grounded AI Vaidya...")
                    ai = st.session_state.ai_consultant
                    ans = ai.synthesize_consultation(
                        patient_summary=f"{patient_name}, {patient_age} yrs, {chief_complaints}",
                        diagnosis_summary=diagnosis_result.clinical_reasoning,
                        treatment_summary=f"{len(treatment_plan.shamana_formulations)} formulations prescribed",
                        user_question=user_query
                    )
                    st.markdown(ans)

        if ask_ai_btn:
            with st.spinner("AI Vaidya analyzing classical Brihat Trayi & Laghu Trayi doctrine..."):
                ai = st.session_state.ai_consultant
                ans = ai.synthesize_consultation(
                    patient_summary=f"Patient: {patient_name}, {patient_age} yrs, Gender: {patient_gender.value}. Chief Complaints: {chief_complaints}. Duration: {duration}.",
                    diagnosis_summary=f"{diagnosis_result.primary_condition} ({diagnosis_result.sanskrit_name}). Dosha: {diagnosis_result.doshic_subtype}. Ama: {diagnosis_result.ama_status.value}. Agni: {diagnosis_result.agni_status.value}.",
                    treatment_summary=f"Deepana: {'; '.join(treatment_plan.deepana_pachana_protocol)}. Formulations: {', '.join([f.name for f in treatment_plan.shamana_formulations])}. Panchakarma: {treatment_plan.panchakarma_guidance.recommended_therapy}.",
                    user_question=user_query
                )
                st.markdown("<div class='ayur-card-gold'>", unsafe_allow_html=True)
                st.markdown("### 🪔 Classical Clinical Vaidya Consultation")
                st.markdown(ans)
                st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 5: CASE SHEET & EXPORT -----------------
with tab5:
    st.markdown("### 📋 Formal Ayurvedic Clinical Case Sheet & Prescription")
    
    current_case = ClinicalCase(
        patient=patient_demo,
        ashta_sthana=ashta_findings,
        dashavidha=dashavidha_findings,
        chief_complaints=[chief_complaints],
        onset_and_duration=duration,
        dosha_scores=dosha_percentages,
        diagnosis=diagnosis_result,
        treatment=treatment_plan
    )

    markdown_sheet = generate_markdown_case_sheet(current_case)
    
    col_dl1, col_dl2 = st.columns([1, 4])
    with col_dl1:
        st.download_button(
            label="📥 Download Case Sheet (.md)",
            data=markdown_sheet,
            file_name=f"AyurNidana_{patient_name.replace(' ', '_')}_CaseSheet.md",
            mime="text/markdown"
        )
    with col_dl2:
        st.caption("Click to export the complete clinical examination, Nidana Panchaka, and formal prescription.")

    st.markdown("---")
    st.markdown(markdown_sheet)

def main():
    pass

if __name__ == "__main__":
    main()
