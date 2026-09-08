"""AyurNidana - Layman-Friendly Ayurvedic Health Assistant.
Simple, intuitive interface designed for everyday patients to understand their body and heal systematically.
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
from ayurnidana.core.ashta_sthana import ASHTA_STHANA_CATALOG
from ayurnidana.core.dashavidha import DASHAVIDHA_CRITERIA
from ayurnidana.core.nidana_engine import NidanaEngine
from ayurnidana.core.chikitsa_engine import ChikitsaEngine
from ayurnidana.core.layman_mapper import extract_symptoms_from_text
from ayurnidana.knowledge.notebook_bridge import NotebookBridge
from ayurnidana.knowledge.local_library import LocalAyurvedaLibrary
from ayurnidana.knowledge.ai_consultant import AIConsultant
from ayurnidana.ui.components.style import CUSTOM_CSS
from ayurnidana.ui.components.case_sheet import generate_markdown_case_sheet

st.set_page_config(
    page_title="AyurNidana - Personal Ayurvedic Health Guide",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Custom layman CSS tweaks
st.markdown("""
<style>
    .patient-hero {
        background: linear-gradient(135deg, #FBF8F3 0%, #F5EFEB 100%);
        border-radius: 14px;
        padding: 1.6rem 2rem;
        border: 1px solid #EAD8C7;
        margin-bottom: 1.5rem;
    }
    .question-box {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 1.2rem;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .badge-plain {
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize singletons in session state
if "notebook_bridge" not in st.session_state:
    st.session_state.notebook_bridge = NotebookBridge(target_notebook_name="ayurveda")
if "library" not in st.session_state:
    st.session_state.library = LocalAyurvedaLibrary()
if "ai_consultant" not in st.session_state:
    st.session_state.ai_consultant = AIConsultant()
if "symptom_text_input" not in st.session_state:
    st.session_state.symptom_text_input = ""
if "active_symptoms" not in st.session_state:
    st.session_state.active_symptoms = set(["joint_pain_cracking", "pain_sharp_throbbing", "tremors_stiffness", "dryness_skin_hair"])

bridge = st.session_state.notebook_bridge
auth_status = bridge.check_auth()
lib = st.session_state.library

# ----------------- SIDEBAR: SIMPLE OPTIONS -----------------
with st.sidebar:
    st.markdown("<h2 style='color:#8C4318; font-family:serif;'>🌿 AyurNidana</h2>", unsafe_allow_html=True)
    st.caption("Your Personal Ayurvedic Health & Healing Companion")
    st.markdown("---")

    st.subheader("💡 Choose an Example Patient:")
    example_choice = st.selectbox(
        "Try an example or start fresh:",
        [
            "Custom Case (My Own Symptoms)",
            "Example 1: Cracking Knee Pain, Stiff Joints & Dry Skin",
            "Example 2: Severe Morning Joint Stiffness & Swelling (Toxins)",
            "Example 3: Acid Reflux, Burning Stomach & Irritability",
            "Example 4: Frequent Urination, Sweet Taste & Fatigue"
        ]
    )

    st.markdown("---")
    st.subheader("📓 My Ayurveda Notebook")
    if auth_status["authenticated"]:
        st.success("✅ Connected to Google NotebookLM")
        conn_res = bridge.connect_to_ayurveda_notebook()
        if conn_res["connected"]:
            st.caption(f"Linked: **{conn_res['title']}**")
    else:
        st.info("ℹ️ NotebookLM: Not signed in yet")
        if st.button("🔑 Sign in with Google"):
            import subprocess
            try:
                subprocess.Popen(["cmd.exe", "/c", "start", "powershell", "-NoExit", "-Command", "python -m notebooklm login"])
                st.info("Google sign-in window launched on your screen! Complete login, then click refresh.")
            except Exception as e:
                st.error(f"Error: {e}")
        if st.button("🔄 Refresh Status"):
            st.rerun()

    st.markdown("---")
    lib_stat = lib.get_library_status()
    st.caption(f"📚 {lib_stat.get('total_treatises', 138)} Classical Books & Treatises Linked")

# ----------------- PRESET DATA HANDLING -----------------
default_name = "Alex"
default_age = 45
default_gender = Gender.MALE
default_story = "My knees make clicking sounds when I climb stairs, and they ache a lot in cold weather. My skin is always dry and I get bloated easily."

if "Example 1" in example_choice:
    default_name = "Rajesh"
    default_age = 54
    default_gender = Gender.MALE
    default_story = "My right knee has sharp clicking sounds and pain when I walk. It feels stiff in the morning and hurts more when it's cold. My skin is dry and I get constipated."
    st.session_state.active_symptoms = set(["joint_pain_cracking", "pain_sharp_throbbing", "tremors_stiffness", "dryness_skin_hair", "constipation_hard_stools"])
elif "Example 2" in example_choice:
    default_name = "Sunita"
    default_age = 42
    default_gender = Gender.FEMALE
    default_story = "My finger and wrist joints are swollen and very painful. Every morning I wake up completely stiff for over an hour. My tongue has a thick white coating and I feel heavy and feverish."
    st.session_state.active_symptoms = set(["joint_pain_cracking", "dull_pain_swelling_edema", "heaviness_body_limbs", "fever", "tongue_thick_white_coating", "loss_of_taste_aruchi"])
elif "Example 3" in example_choice:
    default_name = "Amit"
    default_age = 36
    default_gender = Gender.MALE
    default_story = "I get severe burning in my chest and throat after eating, especially with spicy food. I have sour burps, my stomach burns, and I feel hot and easily irritated."
    st.session_state.active_symptoms = set(["burning_sensation", "acid_reflux_heartburn", "intense_sharp_hunger", "yellowish_eyes_urine", "irritability_anger"])
elif "Example 4" in example_choice:
    default_name = "Vikram"
    default_age = 50
    default_gender = Gender.MALE
    default_story = "I need to pee very often especially at night. My mouth tastes sweet, I am constantly thirsty, and I feel tired and heavy with weight gain."
    st.session_state.active_symptoms = set(["excessive_thirst_sweating", "heaviness_body_limbs", "weight_gain_slow_metabolism", "tongue_thick_white_coating", "burning_sensation"])

# ----------------- HERO BANNER -----------------
st.markdown("""
<div class='patient-hero'>
    <h2 style='margin:0 0 8px 0; color:#7C2D12; font-family:serif;'>🌿 Welcome to AyurNidana</h2>
    <p style='margin:0; font-size:1.1rem; color:#431407; line-height:1.5;'>
        No medical jargon needed. Tell us what you're feeling in everyday words, or check off your symptoms below. 
        We will analyze your body's energy balance, explain what is causing your discomfort, and create a tailored Ayurvedic healing and diet plan.
    </p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 1. Tell Us How You Feel",
    "🔍 2. What Is Happening In Your Body?",
    "💊 3. Your Healing & Diet Plan",
    "❓ 4. Ask Any Question",
    "📄 5. Save My Health Plan"
])

# ----------------- TAB 1: HOW YOU FEEL -----------------
with tab1:
    st.markdown("### Step 1: Tell Us About Yourself")
    col1, col2, col3 = st.columns(3)
    with col1:
        patient_name = st.text_input("Your Name / Nickname:", value=default_name)
    with col2:
        patient_age = st.number_input("Your Age:", min_value=5, max_value=105, value=default_age)
    with col3:
        patient_gender = st.selectbox("Gender:", [Gender.MALE, Gender.FEMALE, Gender.OTHER], index=0 if default_gender == Gender.MALE else 1)

    st.markdown("---")
    st.markdown("### Step 2: Describe What You Are Feeling (In Your Own Words)")
    st.caption("You can type naturally, e.g., 'My knees hurt and click when walking, I feel gassy after dinner, and I can't sleep.'")
    
    user_story = st.text_area("Your Health Story / What hurts or bothers you?", value=default_story, height=80)
    
    if st.button("✨ Auto-Detect Symptoms From My Story"):
        found = extract_symptoms_from_text(user_story)
        if found:
            st.session_state.active_symptoms = set(found)
            st.success(f"Recognized {len(found)} symptom markers from your description! Look at the checklist below to adjust.")
        else:
            st.info("We couldn't detect specific symptoms automatically. Please check the boxes below!")

    st.markdown("---")
    st.markdown("### Step 3: Quick Everyday Health Checklist (Tick what applies)")
    
    scol1, scol2 = st.columns(2)
    with scol1:
        st.markdown("<div class='question-box'><h4>🍽️ Digestion & Stomach</h4>", unsafe_allow_html=True)
        c_acid = st.checkbox("Acid reflux, heartburn, or sour liquid rising in throat", value="acid_reflux_heartburn" in st.session_state.active_symptoms)
        c_bloat = st.checkbox("Belly feels bloated, swollen with gas, or distended", value="bloating_flatulence" in st.session_state.active_symptoms)
        c_const = st.checkbox("Hard, dry stools or trouble having a daily bowel movement", value="constipation_hard_stools" in st.session_state.active_symptoms)
        c_loose = st.checkbox("Loose, burning stools or frequent diarrhea", value="loose_stools_diarrhea" in st.session_state.active_symptoms)
        c_loss_app = st.checkbox("No appetite at all / food has no taste", value="loss_of_taste_aruchi" in st.session_state.active_symptoms)
        c_heavy = st.checkbox("Feeling very heavy, sluggish, or like food sits in stomach for hours", value="heaviness_body_limbs" in st.session_state.active_symptoms)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='question-box'><h4>🦴 Joints, Muscles & Pain</h4>", unsafe_allow_html=True)
        c_joint = st.checkbox("Joints hurt, feel stiff, or make cracking/clicking sounds", value="joint_pain_cracking" in st.session_state.active_symptoms)
        c_sharp = st.checkbox("Sharp, shooting, or throbbing pain", value="pain_sharp_throbbing" in st.session_state.active_symptoms)
        c_stiff = st.checkbox("Body feels locked or stiff in the morning when waking up", value="tremors_stiffness" in st.session_state.active_symptoms)
        c_swell = st.checkbox("Joints are swollen, puffy, or warm to touch", value="dull_pain_swelling_edema" in st.session_state.active_symptoms)
        st.markdown("</div>", unsafe_allow_html=True)

    with scol2:
        st.markdown("<div class='question-box'><h4>😴 Sleep, Energy & Mood</h4>", unsafe_allow_html=True)
        c_sleep = st.checkbox("Trouble falling asleep, waking up frequently, or racing thoughts at night", value="insomnia_disturbed_sleep" in st.session_state.active_symptoms)
        c_anx = st.checkbox("Feeling restless, anxious, nervous, or easily worried", value="anxiety_restlessness" in st.session_state.active_symptoms)
        c_anger = st.checkbox("Feeling irritable, impatient, hot-tempered, or stressed", value="irritability_anger" in st.session_state.active_symptoms)
        c_fatigue = st.checkbox("Constant fatigue / wanting to sleep during the day", value="weight_gain_slow_metabolism" in st.session_state.active_symptoms)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='question-box'><h4>🌡️ Body Sensation & Skin</h4>", unsafe_allow_html=True)
        c_dry = st.checkbox("Skin, lips, or hair feel noticeably dry, rough, or flaky", value="dryness_skin_hair" in st.session_state.active_symptoms)
        c_burn = st.checkbox("Burning sensation in palms, soles, or entire body", value="burning_sensation" in st.session_state.active_symptoms)
        c_rash = st.checkbox("Skin rashes, redness, pimples, or acne breakouts", value="skin_rashes_inflammation_acne" in st.session_state.active_symptoms)
        c_fever = st.checkbox("Feverish feeling, mild fever, or body chills", value="fever" in st.session_state.active_symptoms)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Step 4: Simple Mirror & Body Checks")
    
    bcol1, bcol2, bcol3 = st.columns(3)
    with bcol1:
        st.markdown("**👅 What does your tongue look like in the mirror?**")
        tongue_choice = st.radio(
            "Select tongue appearance:",
            [
                "Clean, pink, moist, and healthy",
                "Thick white coating all over (sign of body toxins)",
                "Dry, rough, or has lines/cracks",
                "Reddish with yellowish/brown coating"
            ],
            index=1 if "thick_white" in " ".join(st.session_state.active_symptoms) else (2 if "cracking" in " ".join(st.session_state.active_symptoms) else 0)
        )

    with bcol2:
        st.markdown("**🚽 What are your bowel movements like?**")
        stool_choice = st.radio(
            "Select bowel quality:",
            [
                "Normal, regular, easy to pass without straining",
                "Hard, dry, dark pebbles, or constipated",
                "Loose, watery, urgent, or with burning feeling",
                "Sticky, heavy, foul-smelling, or sinks in water"
            ],
            index=1 if "constipation" in " ".join(st.session_state.active_symptoms) else (2 if "loose" in " ".join(st.session_state.active_symptoms) else (3 if "thick_white" in " ".join(st.session_state.active_symptoms) else 0))
        )

    with bcol3:
        st.markdown("**🔥 How is your appetite & hunger?**")
        hunger_choice = st.radio(
            "Select hunger level:",
            [
                "Normal and steady (hungry around meal times)",
                "Irregular (sometimes starving, sometimes forgetting to eat)",
                "Intense & sharp (get angry or weak if meal is delayed)",
                "Weak / sluggish (rarely feel genuinely hungry)"
            ],
            index=1 if "dryness" in " ".join(st.session_state.active_symptoms) else (2 if "acid" in " ".join(st.session_state.active_symptoms) else 0)
        )

# Collect selected symptoms
current_selected = []
if c_acid: current_selected.append("acid_reflux_heartburn")
if c_bloat: current_selected.append("bloating_flatulence")
if c_const: current_selected.append("constipation_hard_stools")
if c_loose: current_selected.append("loose_stools_diarrhea")
if c_loss_app: current_selected.append("loss_of_taste_aruchi")
if c_heavy: current_selected.append("heaviness_body_limbs")
if c_joint: current_selected.append("joint_pain_cracking")
if c_sharp: current_selected.append("pain_sharp_throbbing")
if c_stiff: current_selected.append("tremors_stiffness")
if c_swell: current_selected.append("dull_pain_swelling_edema")
if c_sleep: current_selected.append("insomnia_disturbed_sleep")
if c_anx: current_selected.append("anxiety_restlessness")
if c_anger: current_selected.append("irritability_anger")
if c_fatigue: current_selected.append("weight_gain_slow_metabolism")
if c_dry: current_selected.append("dryness_skin_hair")
if c_burn: current_selected.append("burning_sensation")
if c_rash: current_selected.append("skin_rashes_inflammation_acne")
if c_fever: current_selected.append("fever")
if "white coating" in tongue_choice: current_selected.append("tongue_thick_white_coating")

if not current_selected:
    current_selected = ["joint_pain_cracking", "dryness_skin_hair"]

# Run engines
dosha_pct, vikriti_pattern = DoshaEngine.calculate_vikriti(current_selected)
ama_status, ama_reasons = DoshaEngine.assess_ama(current_selected, tongue_choice)
dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(current_selected)

if "sharp" in hunger_choice.lower() or c_acid or c_burn:
    agni_status = AgniType.TIKSHNAGNI
elif "weak" in hunger_choice.lower() or ama_status == AmaStatus.SAMA:
    agni_status = AgniType.MANDAGNI
elif "irregular" in hunger_choice.lower():
    agni_status = AgniType.VISHAMAGNI
else:
    agni_status = AgniType.SAMAGNI

if "hard" in stool_choice.lower() or c_const:
    koshtha_status = KoshthaType.KRURA
elif "loose" in stool_choice.lower() or c_loose:
    koshtha_status = KoshthaType.MRIDU
else:
    koshtha_status = KoshthaType.MADHYAMA

diagnosis_result = NidanaEngine.diagnose(
    symptoms=current_selected,
    vikriti_pattern=vikriti_pattern,
    ama_status=ama_status,
    agni_status=agni_status,
    koshtha_status=koshtha_status,
    dhatu_involved=dhatus,
    srotas_involved=srotas
)

dashavidha_mock = DashavidhaPariksha(
    prakriti="Vata-Pitta",
    vikriti=vikriti_pattern,
    sara_tissue_excellence="Madhyama",
    samhanana_compactness="Madhyama",
    sattva_mental_strength="Madhyama",
    ahara_shakti_digestive_power=hunger_choice,
    vyayama_shakti_physical_stamina="Madhyama",
    vaya_age_stage="Madhyamavastha"
)

treatment_plan = ChikitsaEngine.generate_plan(
    diagnosis=diagnosis_result,
    dashavidha=dashavidha_mock,
    patient_age=patient_age,
    season="Current Season"
)

# ----------------- TAB 2: DIAGNOSIS (LAYMAN EXPLANATION) -----------------
with tab2:
    st.markdown("## 🔍 What Is Happening In Your Body?")
    st.markdown("In Ayurveda, your body is powered by three vital energies (Doshas): **Air & Movement (Vata)**, **Fire & Digestion (Pitta)**, and **Water & Structure (Kapha)**. When one gets too high, discomfort begins.")

    v_val = dosha_pct.get("Vata", 33)
    p_val = dosha_pct.get("Pitta", 33)
    k_val = dosha_pct.get("Kapha", 33)

    st.markdown("### Your Body's Energy Balance Right Now:")
    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        st.markdown(f"""
        <div class='question-box' style='border-top: 4px solid #3182CE;'>
            <h4 style='color:#2B6CB0; margin:0;'>💨 Air & Movement Energy (Vata)</h4>
            <h2 style='margin:4px 0; color:#1A365D;'>{v_val}%</h2>
            <p style='color:#4A5568; font-size:0.9rem;'>Controls joints, nerves, flexibility, and dryness.</p>
        </div>
        """, unsafe_allow_html=True)
    with mcol2:
        st.markdown(f"""
        <div class='question-box' style='border-top: 4px solid #DD6B20;'>
            <h4 style='color:#C05621; margin:0;'>🔥 Fire & Heat Energy (Pitta)</h4>
            <h2 style='margin:4px 0; color:#7B341E;'>{p_val}%</h2>
            <p style='color:#4A5568; font-size:0.9rem;'>Controls digestion, acidity, skin heat, and metabolism.</p>
        </div>
        """, unsafe_allow_html=True)
    with mcol3:
        st.markdown(f"""
        <div class='question-box' style='border-top: 4px solid #38A169;'>
            <h4 style='color:#276749; margin:0;'>🌊 Earth & Fluid Energy (Kapha)</h4>
            <h2 style='margin:4px 0; color:#22543D;'>{k_val}%</h2>
            <p style='color:#4A5568; font-size:0.9rem;'>Controls joint lubrication, mucus, stability, and weight.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div class='ayur-card-gold'>
        <h3 style='color:#92400E; margin:0;'>🎯 Summary of What You Are Experiencing:</h3>
        <h2 style='color:#78350F; margin:4px 0 10px 0;'>{diagnosis_result.primary_condition}</h2>
        <p style='font-size:1.05rem; color:#451A03; line-height:1.6;'>
            Based on your answers, your primary issue is caused by <strong>{vikriti_pattern}</strong>. 
            When this happens, your body experiences excess dryness, friction, or heat in the affected areas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧽 Internal Toxin Level (Ama):")
    if ama_status == AmaStatus.SAMA:
        st.warning("⚠️ **High Buildup of Undigested Toxins (Ama)**: Your digestive fire has been weak, leaving behind sticky metabolic waste. This causes heavy morning stiffness, coated tongue, and fatigue. Our first step is a gentle detox.")
    elif ama_status == AmaStatus.MILD_AMA:
        st.info("ℹ️ **Mild Toxin Buildup**: Some minor digestive sluggishness is present. Gentle digestive spices like ginger will clear this up quickly.")
    else:
        st.success("✅ **Clean & Clear**: No significant toxic residue detected in your tongue or bowels.")

    with st.expander("📜 For Doctors & Curious Readers (Classical Sanskrit Details)"):
        st.write(f"**Sanskrit Name:** {diagnosis_result.sanskrit_name}")
        st.write(f"**Dhatu (Tissues Involved):** {', '.join(diagnosis_result.dhatu_involved)}")
        st.write(f"**Srotas (Channels):** {', '.join(diagnosis_result.srotas_involved)}")
        st.write(f"**Classical References:** {', '.join(diagnosis_result.classical_citations)}")

# ----------------- TAB 3: TREATMENT PLAN (LAYMAN) -----------------
with tab3:
    st.markdown(f"## 💊 Your Simple Healing & Recovery Plan for {patient_name}")
    st.markdown("Here is your practical, everyday guide to feeling better naturally.")

    # Step 1: Detox
    st.markdown("<div class='ayur-card-gold'>", unsafe_allow_html=True)
    st.markdown("### 1️⃣ Morning Reset & Digestive Boost")
    st.markdown("Before taking any heavy medicines, we need to ignite your natural digestive fire so your body absorbs nutrients:")
    for dp in treatment_plan.deepana_pachana_protocol:
        st.markdown(f"• **{dp}**")
    st.markdown("</div>", unsafe_allow_html=True)

    # Step 2: Medicines
    st.markdown("### 2️⃣ Recommended Herbal Formulations")
    st.markdown("These classical herbs are selected to calm your specific imbalance:")
    
    for f in treatment_plan.shamana_formulations:
        st.markdown(f"""
        <div class='question-box' style='border-left: 5px solid #2B6CB0;'>
            <h4 style='margin:0; color:#1A365D;'>🌿 {f.name}</h4>
            <p style='margin:4px 0; font-size:1rem;'><strong>Why take it:</strong> {f.classical_indication}</p>
            <p style='margin:2px 0; color:#4A5568;'><strong>How much:</strong> {f.dosage} &bull; <strong>Take with:</strong> {f.anupana_vehicle}</p>
            <p style='margin:2px 0; color:#2B6CB0; font-weight:600;'><strong>When:</strong> {f.aushadha_sevana_kala} (for {f.duration_weeks} weeks)</p>
        </div>
        """, unsafe_allow_html=True)

    # Step 3: Food
    st.markdown("### 3️⃣ Your Kitchen Guide: What to Eat & What to Avoid")
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        st.markdown("<div class='ayur-card-green'>", unsafe_allow_html=True)
        st.markdown("#### 🟢 Enjoy These Foods:")
        for item in treatment_plan.dietary_and_lifestyle_regimen.pathya_ahara_wholesome_diet[:5]:
            st.write(f"✓ {item}")
        st.markdown("</div>", unsafe_allow_html=True)

    with fcol2:
        st.markdown("<div class='ayur-card-red'>", unsafe_allow_html=True)
        st.markdown("#### 🔴 Avoid or Cut Down On:")
        for item in treatment_plan.dietary_and_lifestyle_regimen.apathya_ahara_unwholesome_diet[:5]:
            st.write(f"✗ {item}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Bad Food Combinations
    st.markdown("#### ⚠️ Incompatible Food Habits (Never Do These):")
    for warn in treatment_plan.dietary_and_lifestyle_regimen.viruddha_ahara_warnings[:3]:
        st.markdown(f"• **{warn}**")

    # Yoga & Daily Routine
    st.markdown("### 4️⃣ Simple Habits & Movements")
    ycol1, ycol2 = st.columns(2)
    with ycol1:
        st.markdown("**Daily Habits:**")
        for hab in treatment_plan.dietary_and_lifestyle_regimen.pathya_vihara_recommended_lifestyle[:3]:
            st.write(f"• {hab}")
    with ycol2:
        st.markdown("**Easy Breathing & Gentle Poses:**")
        for yg in treatment_plan.dietary_and_lifestyle_regimen.yoga_and_pranayama:
            st.write(f"• {yg}")

    # Red Flags
    if treatment_plan.red_flag_warnings:
        st.markdown("<div class='ayur-card-red'>", unsafe_allow_html=True)
        st.markdown("#### 🚨 When to See an Emergency Doctor Immediately:")
        st.markdown("If you experience any of these serious signs, please visit a modern hospital immediately:")
        for rf in treatment_plan.red_flag_warnings:
            st.write(f"• {rf}")
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 4: ASK ANY QUESTION -----------------
with tab4:
    st.markdown("## 💬 Ask Any Question in Everyday Language")
    st.markdown("Have a question about what tea to drink, what breakfast to eat, or why your body hurts? Ask here:")

    quick_questions = [
        "What is the best breakfast for my condition?",
        "Can I drink coffee or green tea with my symptoms?",
        "Why do my joints click more when it gets cold?",
        "How do I clear the white coating on my tongue naturally?"
    ]
    
    selected_quick = st.selectbox("Or choose a common question:", ["Type my own question below..."] + quick_questions)
    
    default_q = selected_quick if selected_quick != "Type my own question below..." else f"Explain in simple layman terms what I should do every morning to recover from {diagnosis_result.primary_condition}."
    user_patient_q = st.text_input("Your Question:", value=default_q)

    if st.button("Get My Answer", type="primary"):
        with st.spinner("Analyzing with Ayurvedic knowledge and your notebook..."):
            ai = st.session_state.ai_consultant
            ans = ai.synthesize_consultation(
                patient_summary=f"Patient {patient_name}, Age {patient_age}. Story: {user_story}. Active complaints: {', '.join(current_selected)}.",
                diagnosis_summary=f"Condition: {diagnosis_result.primary_condition}. Dosha: {diagnosis_result.doshic_subtype}. Toxin/Ama: {diagnosis_result.ama_status.value}.",
                treatment_summary=f"Formulations: {', '.join([f.name for f in treatment_plan.shamana_formulations])}",
                user_question=f"Answer in simple, friendly, empathetic layman English without overwhelming medical terms. Focus on practical home remedies and actionable advice: {user_patient_q}"
            )
            st.markdown("<div class='ayur-card-gold'>", unsafe_allow_html=True)
            st.markdown("### 🌿 Ayurvedic Guidance for You:")
            st.markdown(ans)
            st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 5: EXPORT -----------------
with tab5:
    st.markdown("## 📄 Your Complete Health Summary & Prescription")
    
    patient_demo = PatientDemographics(
        name=patient_name,
        age=patient_age,
        gender=patient_gender,
        occupation="General",
        geographical_region="Local",
        current_season="Current"
    )

    ashta_mock = AshtaSthanaPariksha(
        nadi_pulse="Pulse matching primary dosha",
        jihva_tongue=tongue_choice,
        mutra_urine="Urine check",
        mala_stool=stool_choice,
        shabda_voice="Voice clear",
        sparsha_skin="Skin check",
        druk_eyes="Eyes clear",
        akruti_appearance="Habitus check"
    )

    case_obj = ClinicalCase(
        patient=patient_demo,
        ashta_sthana=ashta_mock,
        dashavidha=dashavidha_mock,
        chief_complaints=[user_story],
        onset_and_duration="Recent months",
        dosha_scores=dosha_pct,
        diagnosis=diagnosis_result,
        treatment=treatment_plan
    )

    case_md = generate_markdown_case_sheet(case_obj)
    
    st.download_button(
        label="📥 Download My Health Plan (.md)",
        data=case_md,
        file_name=f"AyurNidana_{patient_name.replace(' ', '_')}_HealthPlan.md",
        mime="text/markdown"
    )

    st.markdown("---")
    st.markdown(case_md)
