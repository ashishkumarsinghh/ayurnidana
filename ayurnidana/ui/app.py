"""AyurNidana v3 — Phased, Intuitive, Beautiful.

UX Flow:
  AUTH  →  INPUT (describe + 3 body checks)  →  RESULTS (scroll)
                                                   └→ Ask AyurVaidya (inline)
                                                   └→ Save / Download (inline)

No tabs. No sidebar. No checkboxes. Just a guided conversation.
"""

import hashlib
import json
import os
import sqlite3
import hashlib as _hs

import streamlit as st

from ayurnidana.core.models import (
    Gender, AmaStatus, AgniType, KoshthaType,
    PatientDemographics, AshtaSthanaPariksha, DashavidhaPariksha, ClinicalCase
)
from ayurnidana.core.dosha_engine import DoshaEngine
from ayurnidana.core.nidana_engine import NidanaEngine
from ayurnidana.core.chikitsa_engine import ChikitsaEngine
from ayurnidana.core.layman_mapper import (
    get_symptom_label,
    get_symptoms_by_category,
    SYMPTOM_DEFINITIONS,
    extract_symptoms_with_ai,
)
from ayurnidana.knowledge.local_library import LocalAyurvedaLibrary
from ayurnidana.knowledge.ai_consultant import AIConsultant
from ayurnidana.ui.components.style import CUSTOM_CSS
from ayurnidana.ui.components.case_sheet import generate_markdown_case_sheet


# ─────────────────────────────────────────────────────────────────
# BODY CHECK OPTION MAPS
# ─────────────────────────────────────────────────────────────────

TONGUE_OPTS = [
    ("👅", "Clean & Pink",   "clean"),
    ("🌫️", "White Coated", "white"),
    ("🔴", "Red / Inflamed", "red"),
    ("🏜️", "Dry & Cracked", "dry"),
]
STOOL_OPTS = [
    ("✅", "Regular",         "normal"),
    ("🪨", "Hard & Dry",     "hard"),
    ("💧", "Loose / Watery", "loose"),
    ("🟫", "Sticky & Heavy", "sticky"),
]
HUNGER_OPTS = [
    ("⚖️", "Normal",          "normal"),
    ("⚡", "Intense / Urgent","intense"),
    ("🎲", "Irregular",       "irregular"),
    ("😴", "Weak / Sluggish", "weak"),
]

TONGUE_STR = {
    "clean": "Clean — healthy pink, no coating",
    "white": "Thick white coating (Ama / Kapha)",
    "red":   "Red, yellow, or inflamed (Pitta)",
    "dry":   "Dry, rough, or cracked (Vata)",
}
STOOL_STR = {
    "normal": "Normal, regular, easy to pass",
    "hard":   "Hard, dry, pebble-like (Vata/constipation)",
    "loose":  "Loose, watery, urgent (Pitta/Kapha)",
    "sticky": "Sticky, heavy, foul-smelling (Ama)",
}
HUNGER_STR = {
    "normal":    "Normal and steady",
    "intense":   "Intense & sharp (get irritable if meal delayed)",
    "irregular": "Irregular (sometimes starving, sometimes not hungry)",
    "weak":      "Weak / sluggish — rarely feel hungry",
}


# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────

def _tag(category: str) -> str:
    c = category.lower()
    if "vati" in c or "guggulu" in c: return "tag-vati",   "Vati"
    if "kwatha" in c or "kashaya" in c: return "tag-kwatha","Kwatha"
    if "churna" in c:   return "tag-churna",  "Churna"
    if "asava" in c or "arishta" in c: return "tag-asava", "Asava"
    if "ghrita" in c or "ghee" in c:  return "tag-ghrita", "Ghrita"
    if "taila" in c or "oil" in c:    return "tag-taila",  "Taila"
    if "rasayana" in c: return "tag-rasayana","Rasayana"
    return "tag-herbal", "Herbal"

def _dosha_color(d: str) -> tuple:
    """Returns (text_color, fill_color, bg_color) all high-contrast."""
    return {
        "Vata":  ("#1E3A8A", "#2563EB", "#DBEAFE"),
        "Pitta": ("#7F1D1D", "#DC2626", "#FEE2E2"),
        "Kapha": ("#14532D", "#16A34A", "#DCFCE7"),
    }.get(d, ("#3D1F08", "#9C3B12", "#FEF6EF"))

def _ama_html(ama) -> str:
    if ama == AmaStatus.SAMA:
        return "<span style='color:#991B1B;font-weight:700;'>⚠ High Ama — Toxin Load</span>"
    if ama == AmaStatus.MILD_AMA:
        return "<span style='color:#92400E;font-weight:700;'>〜 Mild Ama Present</span>"
    return "<span style='color:#14532D;font-weight:700;'>✓ Nirama — Channels Clear</span>"

def _agni_html(agni) -> str:
    m = {
        AgniType.MANDAGNI:   ("<span style='color:#991B1B;font-weight:700;'>Mandagni</span>", "Slow / Weak"),
        AgniType.TIKSHNAGNI: ("<span style='color:#92400E;font-weight:700;'>Tikshnagni</span>", "Sharp / Hyper"),
        AgniType.VISHAMAGNI: ("<span style='color:#581C87;font-weight:700;'>Vishamagni</span>", "Irregular"),
        AgniType.SAMAGNI:    ("<span style='color:#14532D;font-weight:700;'>Samagni</span>", "Balanced ✓"),
    }
    v, sub = m.get(agni, ("—", ""))
    return v, sub

def _koshtha_html(k) -> tuple:
    return {
        KoshthaType.KRURA:   ("Krura",   "Constipation-prone"),
        KoshthaType.MRIDU:   ("Mridu",   "Loose / Hyper-sensitive"),
        KoshthaType.MADHYAMA:("Madhyama","Balanced ✓"),
    }.get(k, ("—", ""))

def _body_check_row(label: str, options: list, key: str):
    """Render tap-to-select body check options as styled button cards."""
    st.markdown(f'<div class="an-label" style="margin-top:1.2rem;">{label}</div>', unsafe_allow_html=True)
    current = st.session_state.get(key, options[0][2])
    cols = st.columns(len(options))
    for col, (icon, text, val) in zip(cols, options):
        with col:
            is_sel = current == val
            t = "primary" if is_sel else "secondary"
            if st.button(f"{icon} {text}", key=f"bc_{key}_{val}",
                         use_container_width=True, type=t):
                st.session_state[key] = val
                st.rerun()

def _sync_body_checks():
    """Map body-check selections into the active_symptoms dict."""
    sym = st.session_state.active_symptoms
    tongue = st.session_state.get("tongue_val", "clean")
    stool  = st.session_state.get("stool_val",  "normal")
    hunger = st.session_state.get("hunger_val", "normal")

    # Tongue
    for k in ["tongue_thick_white_coating", "tongue_dry_rough_cracked", "tongue_red_yellow_coating"]:
        sym.pop(k, None)
    if tongue == "white": sym["tongue_thick_white_coating"] = "constant"
    elif tongue == "dry": sym["tongue_dry_rough_cracked"]   = "constant"
    elif tongue == "red": sym["tongue_red_yellow_coating"]  = "constant"

    # Stool
    for k in ["constipation_hard_stools", "loose_stools_diarrhea", "malabsorption_mucus_stools"]:
        sym.pop(k, None)
    if stool == "hard":   sym["constipation_hard_stools"]   = "constant"
    elif stool == "loose":sym["loose_stools_diarrhea"]       = "constant"
    elif stool == "sticky":sym["malabsorption_mucus_stools"] = "constant"

    # Hunger / appetite
    for k in ["irregular_appetite", "intense_sharp_hunger", "loss_of_appetite"]:
        sym.pop(k, None)
    if hunger == "irregular": sym["irregular_appetite"]   = "constant"
    elif hunger == "intense": sym["intense_sharp_hunger"] = "constant"
    elif hunger == "weak":    sym["loss_of_appetite"]     = "constant"


# ─────────────────────────────────────────────────────────────────
# DATABASE (SQLite)
# ─────────────────────────────────────────────────────────────────

_DB_PATH = os.path.join(os.path.dirname(__file__), "../../..", "data", "ayurnidana.db")

def _db():
    os.makedirs(os.path.dirname(_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        age INTEGER DEFAULT 35,
        gender TEXT DEFAULT 'Male',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS consultations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        chief_complaint TEXT,
        symptoms TEXT,
        primary_condition TEXT,
        sanskrit_name TEXT,
        dosha_scores TEXT,
        treatment_summary TEXT,
        case_sheet_md TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    return conn

def authenticate_user(identity: str, password: str):
    try:
        ph = _hs.sha256(password.encode()).hexdigest()
        conn = _db()
        row = conn.execute(
            "SELECT * FROM users WHERE (username=? OR email=?) AND password_hash=?",
            (identity, identity, ph)
        ).fetchone()
        conn.close()
        if row: return True, "OK", dict(row)
        return False, "Incorrect username or password.", None
    except Exception as e:
        return False, f"Error: {e}", None

def register_user(username, email, password, full_name, age, gender):
    try:
        ph = _hs.sha256(password.encode()).hexdigest()
        conn = _db()
        conn.execute(
            "INSERT INTO users (username,email,password_hash,full_name,age,gender) VALUES (?,?,?,?,?,?)",
            (username, email, ph, full_name, age, gender)
        )
        conn.commit()
        row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()
        return True, "Account created!", dict(row)
    except sqlite3.IntegrityError:
        return False, "Username or email already in use.", None
    except Exception as e:
        return False, f"Error: {e}", None

def save_consultation(user_id, chief_complaint, symptoms, primary_condition,
                      sanskrit_name, dosha_scores, treatment_summary, case_sheet_md):
    try:
        conn = _db()
        conn.execute(
            """INSERT INTO consultations
               (user_id,chief_complaint,symptoms,primary_condition,sanskrit_name,
                dosha_scores,treatment_summary,case_sheet_md)
               VALUES (?,?,?,?,?,?,?,?)""",
            (user_id, chief_complaint, json.dumps(symptoms), primary_condition,
             sanskrit_name, json.dumps(dosha_scores), treatment_summary, case_sheet_md)
        )
        conn.commit()
        cid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return cid
    except Exception:
        return None

def get_user_consultations(user_id):
    try:
        conn = _db()
        rows = conn.execute(
            "SELECT * FROM consultations WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
        conn.close()
        result = []
        for r in rows:
            d = dict(r)
            d["symptoms"]     = json.loads(d.get("symptoms") or "[]")
            d["dosha_scores"] = json.loads(d.get("dosha_scores") or "{}")
            result.append(d)
        return result
    except Exception:
        return []


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="AyurNidana — Your Ayurvedic Health Guide",
        page_icon="🌿",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # ── Session defaults ────────────────────────────────────────
    defaults = dict(
        user=None, is_guest=False,
        view="input",          # "input" | "results" | "history"
        active_symptoms={},
        user_story="",
        tongue_val="clean", stool_val="normal", hunger_val="normal",
        last_q_response="",
        _diag_cache_key="",
    )
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if isinstance(st.session_state.active_symptoms, (set, list)):
        st.session_state.active_symptoms = {s: "constant" for s in st.session_state.active_symptoms}

    if "ai_consultant" not in st.session_state:
        st.session_state.ai_consultant = AIConsultant()
    ai: AIConsultant = st.session_state.ai_consultant

    # ── Auth gate ────────────────────────────────────────────────
    if not st.session_state.user and not st.session_state.is_guest:
        _render_auth()
        return

    # ── User vars ────────────────────────────────────────────────
    user      = st.session_state.user
    is_guest  = st.session_state.is_guest
    user_id   = user.get("id", 0)

    if "patient_name"   not in st.session_state: st.session_state.patient_name   = user.get("full_name","Patient")
    if "patient_age"    not in st.session_state: st.session_state.patient_age    = int(user.get("age",35))
    if "patient_gender" not in st.session_state: st.session_state.patient_gender = user.get("gender","Male")

    name   = st.session_state.patient_name
    age    = int(st.session_state.patient_age)
    gender = Gender.FEMALE if st.session_state.patient_gender == "Female" else Gender.MALE
    vaya   = "Bala" if age < 16 else ("Madhyama" if age <= 60 else "Vriddha")

    # ── Render ───────────────────────────────────────────────────
    _render_topbar(name, is_guest, user_id)

    if st.session_state.view == "history":
        _render_history(user_id, is_guest)
    elif st.session_state.view == "results":
        _render_results(name, age, gender, vaya, is_guest, user_id, ai)
    else:
        _render_input(ai)


# ─────────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────────

def _render_auth():
    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        st.markdown("""
        <div class="an-auth-logo">
            <div class="icon">🌿</div>
            <h2>AyurNidana</h2>
            <p>Your personal Ayurvedic diagnostic companion.<br>
               Ancient wisdom, personalized to you.</p>
        </div>
        """, unsafe_allow_html=True)

        tab_in, tab_reg = st.tabs(["Sign In", "Create Account"])

        with tab_in:
            ident = st.text_input("Username or Email", placeholder="you@example.com", key="li_id")
            pwd   = st.text_input("Password", type="password", key="li_pwd")
            if st.button("Sign In →", type="primary", use_container_width=True, key="btn_li"):
                if ident and pwd:
                    ok, msg, ud = authenticate_user(ident, pwd)
                    if ok:
                        st.session_state.user = ud
                        st.session_state.patient_name   = ud.get("full_name","Patient")
                        st.session_state.patient_age    = ud.get("age",35)
                        st.session_state.patient_gender = ud.get("gender","Male")
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Fill in both fields.")

        with tab_reg:
            rc1, rc2 = st.columns(2)
            with rc1:
                rn = st.text_input("Full Name", key="rn", placeholder="Ananya Sharma")
                ru = st.text_input("Username",  key="ru", placeholder="ananya")
                ra = st.number_input("Age", 1, 110, 30, key="ra")
            with rc2:
                re = st.text_input("Email",    key="re", placeholder="you@example.com")
                rp = st.text_input("Password", key="rp", type="password")
                rg = st.selectbox("Gender", ["Male","Female","Other"], key="rg")
            if st.button("Create Account →", type="primary", use_container_width=True, key="btn_reg"):
                if rn and ru and re and rp:
                    ok, msg, ud = register_user(ru, re, rp, rn, ra, rg)
                    if ok:
                        st.session_state.user = ud
                        st.session_state.patient_name   = rn
                        st.session_state.patient_age    = ra
                        st.session_state.patient_gender = rg
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill all fields.")

        st.markdown("<div style='text-align:center;margin:1rem 0 0.5rem;color:#6B4C30;font-size:0.85rem;'>or</div>",
                    unsafe_allow_html=True)
        if st.button("Continue as Guest →", use_container_width=True, key="btn_guest"):
            st.session_state.is_guest = True
            st.session_state.user = {
                "id":0,"username":"guest","email":"","full_name":"Guest","age":35,"gender":"Male"
            }
            st.session_state.patient_name   = "Guest"
            st.session_state.patient_age    = 35
            st.session_state.patient_gender = "Male"
            st.rerun()
        st.caption("Guest sessions are not saved. Create a free account to keep your health history.")


# ─────────────────────────────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────────────────────────────

def _render_topbar(name: str, is_guest: bool, user_id: int):
    c1, c2, c3 = st.columns([2, 3, 2])
    with c1:
        st.markdown("<div style='padding-top:4px;font-family:Lora,serif;font-size:1.15rem;font-weight:600;color:#5C2D0A;'>🌿 AyurNidana</div>",
                    unsafe_allow_html=True)
    with c2:
        # Step dots
        view = st.session_state.view
        step1 = "done"   if view in ("results","history") else "active"
        step2 = "active" if view == "results" else ("done" if view == "history" else "")
        step3 = "active" if view == "history" else ""
        st.markdown(f"""
        <div class="an-steps" style="padding-top:6px;">
            <div class="an-step-dot {step1}" title="Describe"></div>
            <div style="height:1px;width:18px;background:#C9B59A;"></div>
            <div class="an-step-dot {step2}" title="Results"></div>
            <div style="height:1px;width:18px;background:#C9B59A;"></div>
            <div class="an-step-dot {step3}" title="History"></div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        mc1, mc2 = st.columns(2)
        with mc1:
            if view != "history":
                if st.button("📑", use_container_width=True, help="History"):
                    st.session_state.view = "history"
                    st.rerun()
            else:
                if st.button("🏠", use_container_width=True, help="Home"):
                    st.session_state.view = "input"
                    st.rerun()
        with mc2:
            if is_guest:
                if st.button("Login", use_container_width=True):
                    st.session_state.user = None
                    st.session_state.is_guest = False
                    st.rerun()
            else:
                if st.button("Exit", use_container_width=True, help=f"Sign out ({name})"):
                    for k in ["user","is_guest","active_symptoms","user_story",
                              "_diag_cache_key","diagnosis_result","treatment_plan"]:
                        st.session_state.pop(k, None)
                    st.session_state.is_guest = False
                    st.rerun()

    st.markdown("<hr style='margin:0.8rem 0 1.4rem;'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# INPUT VIEW
# ─────────────────────────────────────────────────────────────────

def _render_input(ai: AIConsultant):
    name = st.session_state.patient_name

    st.markdown(f"""
    <div class="an-page-title">How are you feeling, {name.split()[0]}?</div>
    <div class="an-page-sub">
        Describe what's bothering you in your own words — a few sentences is enough.
        We'll identify your symptoms, check your body signals, and build a personalized Ayurvedic healing plan.
    </div>
    """, unsafe_allow_html=True)

    # ── Story textarea ──────────────────────────────────────────
    story = st.text_area(
        "What's troubling you?",
        value=st.session_state.user_story,
        placeholder=(
            "e.g. I've had bloating and gas after every meal for the past 2 weeks. "
            "I also get headaches in the morning and feel tired despite sleeping 8 hours..."
        ),
        height=120,
        label_visibility="collapsed",
        key="story_ta"
    )
    st.session_state.user_story = story

    # ── Active symptoms chips ───────────────────────────────────
    sym = st.session_state.active_symptoms
    if sym:
        st.markdown("<div style='margin:0.6rem 0 0.2rem;'>", unsafe_allow_html=True)
        chips_html = ""
        for sid, freq in sym.items():
            label = get_symptom_label(sid)
            cls = "sym-chip" if freq == "constant" else "sym-chip-mild"
            dot = "🔴" if freq == "constant" else "🟡"
            chips_html += f"<span class='{cls}'>{dot} {label}</span>"
        st.markdown(chips_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Search & add specific symptoms ─────────────────────────
    with st.expander("＋ Add or remove specific symptoms", expanded=False):
        all_opts = {sid: f"{data['label']}" + (" ✓" if sid in sym else "")
                    for sid, data in SYMPTOM_DEFINITIONS.items()}
        sc1, sc2, sc3 = st.columns([3, 1.5, 1])
        with sc1:
            chosen = st.selectbox("Search symptoms", ["— select —"] + list(all_opts.keys()),
                                  format_func=lambda x: all_opts.get(x, x),
                                  key="sym_search", label_visibility="collapsed")
        with sc2:
            freq_opt = st.selectbox("Frequency", ["Mild / Sometimes", "Severe / Constant"],
                                    key="sym_freq", label_visibility="collapsed")
        with sc3:
            is_upd = chosen in sym
            if st.button("Update" if is_upd else "Add", use_container_width=True,
                         type="primary", key="btn_add"):
                if chosen and chosen != "— select —":
                    fv = "sometimes" if "Mild" in freq_opt else "constant"
                    sym[chosen] = fv
                    st.toast(f"✅ {SYMPTOM_DEFINITIONS[chosen]['label']}")
                    st.rerun()

        # Remove chips
        if sym:
            st.markdown("<div style='margin-top:0.8rem;'>", unsafe_allow_html=True)
            remove_cols = st.columns(3)
            items = list(sym.items())
            for i, (sid, freq) in enumerate(items):
                with remove_cols[i % 3]:
                    dot = "🔴" if freq == "constant" else "🟡"
                    if st.button(f"{dot} {get_symptom_label(sid)}", key=f"rm_{sid}",
                                 use_container_width=True):
                        sym.pop(sid, None)
                        st.rerun()
            st.caption("Click a symptom above to remove it.")
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── Body checks ─────────────────────────────────────────────
    st.markdown('<div class="an-label">3 Quick Body Checks</div>', unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.88rem;color:#6B4C30;margin-bottom:0.8rem;'>Tap to select — these take 10 seconds and greatly improve accuracy.</div>",
                unsafe_allow_html=True)

    _body_check_row("👅 How does your tongue look?", TONGUE_OPTS, "tongue_val")
    _body_check_row("🚽 How are your bowel movements?", STOOL_OPTS, "stool_val")
    _body_check_row("🍽️ How is your appetite?", HUNGER_OPTS, "hunger_val")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Profile (collapsible, not required) ─────────────────────
    with st.expander("👤 Patient details (name, age, gender)", expanded=False):
        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            nn = st.text_input("Name", value=st.session_state.patient_name, key="pn")
            if nn != st.session_state.patient_name:
                st.session_state.patient_name = nn
        with pc2:
            na = st.number_input("Age", 1, 115, value=st.session_state.patient_age, step=1, key="pa")
            if na != st.session_state.patient_age:
                st.session_state.patient_age = int(na)
        with pc3:
            gi = ["Male","Female","Other"].index(st.session_state.patient_gender)
            ng = st.selectbox("Gender", ["Male","Female","Other"], index=gi, key="pg")
            if ng != st.session_state.patient_gender:
                st.session_state.patient_gender = ng

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── CTA ─────────────────────────────────────────────────────
    btn_cols = st.columns([1, 2, 1])
    with btn_cols[1]:
        clicked = st.button(
            "✨ Get My Healing Plan",
            type="primary",
            use_container_width=True,
            key="btn_analyze"
        )

    if clicked:
        if not story.strip() and not sym:
            st.warning("Please describe how you're feeling, or select at least one symptom.")
        else:
            with st.spinner("Analyzing your symptoms..."):
                if story.strip():
                    found = extract_symptoms_with_ai(story, ai)
                    for k, v in found.items():
                        if k not in sym:
                            sym[k] = v
            _sync_body_checks()
            st.session_state.active_symptoms = sym
            st.session_state.view = "results"
            st.rerun()


# ─────────────────────────────────────────────────────────────────
# RESULTS VIEW
# ─────────────────────────────────────────────────────────────────

def _render_results(name: str, age: int, gender: Gender, vaya: str,
                    is_guest: bool, user_id: int, ai: AIConsultant):

    sym = dict(st.session_state.active_symptoms)
    tongue_val = st.session_state.get("tongue_val", "clean")
    stool_val  = st.session_state.get("stool_val",  "normal")
    hunger_val = st.session_state.get("hunger_val", "normal")

    tongue_str = TONGUE_STR.get(tongue_val, "")
    stool_str  = STOOL_STR.get(stool_val, "")
    hunger_str = HUNGER_STR.get(hunger_val, "")

    if not sym:
        st.markdown("""<div class="an-empty">
            <div class="ei">🌿</div><h3>No symptoms found</h3>
            <p>Go back and describe how you're feeling, or select your body check options.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("← Describe Again", type="primary"):
            st.session_state.view = "input"
            st.rerun()
        return

    # Back button (inline, unobtrusive)
    bc, _, rc = st.columns([1.5, 3, 1.5])
    with bc:
        if st.button("← Describe Again"):
            st.session_state.view = "input"
            st.rerun()
    with rc:
        sym_count = len(sym)
        st.markdown(f"<div style='text-align:right;font-size:0.83rem;color:#6B4C30;padding-top:6px;'>{sym_count} symptoms tracked</div>",
                    unsafe_allow_html=True)

    # ── Compute diagnostics (cached) ────────────────────────────
    _cache_key = hashlib.md5(
        (str(sorted(sym.items())) + tongue_str + stool_str + hunger_str + str(age)).encode()
    ).hexdigest()

    if st.session_state.get("_diag_cache_key") != _cache_key or "diagnosis_result" not in st.session_state:
        dosha_pct, vikriti = DoshaEngine.calculate_vikriti(sym)
        ama_status, ama_reasons = DoshaEngine.assess_ama(sym, tongue_str)
        dhatus, srotas = DoshaEngine.determine_dhatu_and_srotas(sym)

        if "sharp" in hunger_str.lower() or "intense" in hunger_str.lower():
            agni = AgniType.TIKSHNAGNI
        elif "weak" in hunger_str.lower() or ama_status == AmaStatus.SAMA:
            agni = AgniType.MANDAGNI
        elif "irregular" in hunger_str.lower():
            agni = AgniType.VISHAMAGNI
        else:
            agni = AgniType.SAMAGNI

        if "hard" in stool_str.lower():   koshtha = KoshthaType.KRURA
        elif "loose" in stool_str.lower(): koshtha = KoshthaType.MRIDU
        else:                              koshtha = KoshthaType.MADHYAMA

        dx = NidanaEngine.diagnose(
            symptoms=sym, vikriti_pattern=vikriti,
            ama_status=ama_status, agni_status=agni, koshtha_status=koshtha,
            dhatu_involved=dhatus, srotas_involved=srotas
        )
        dasha = DashavidhaPariksha(
            prakriti=vikriti.split("(")[0].strip(),
            vikriti=vikriti,
            sara_tissue_excellence="Madhyama",
            samhanana_compactness="Madhyama",
            sattva_mental_strength="Madhyama",
            ahara_shakti_digestive_power=hunger_str,
            vyayama_shakti_physical_stamina="Madhyama",
            vaya_age_stage="Madhyamavastha" if age < 60 else "Vriddhavastha"
        )
        tx = ChikitsaEngine.generate_plan(diagnosis=dx, dashavidha=dasha, patient_age=age, season="Current Season")

        st.session_state.update(dict(
            _diag_cache_key=_cache_key,
            diagnosis_result=dx, treatment_plan=tx,
            dosha_pct=dosha_pct, vikriti_pattern=vikriti,
            ama_status=ama_status, ama_reasons=ama_reasons,
            agni_status=agni, koshtha_status=koshtha,
            dhatus=dhatus, srotas=srotas, dasha=dasha,
        ))
    else:
        dx        = st.session_state["diagnosis_result"]
        tx        = st.session_state["treatment_plan"]
        dosha_pct = st.session_state["dosha_pct"]
        vikriti   = st.session_state["vikriti_pattern"]
        ama_status= st.session_state["ama_status"]
        ama_reasons=st.session_state["ama_reasons"]
        agni      = st.session_state["agni_status"]
        koshtha   = st.session_state["koshtha_status"]
        dhatus    = st.session_state["dhatus"]
        srotas    = st.session_state["srotas"]
        dasha     = st.session_state["dasha"]

    # ════════════════════════════════════════
    # SECTION 1: DIAGNOSIS
    # ════════════════════════════════════════
    prognosis = getattr(dx, "prognosis", "Sadhya")
    st.markdown(f"""
    <div class="an-dx-card">
        <div class="condition">{dx.primary_condition}</div>
        <div class="sanskrit">Sanskrit: {dx.sanskrit_name}</div>
        <span class="an-dx-badge">⚖ {dx.doshic_subtype}</span>
        <span class="an-dx-badge">📊 {prognosis}</span>
    </div>
    """, unsafe_allow_html=True)

    # Secondary conditions
    sec = getattr(dx, "secondary_conditions", [])
    if sec:
        st.markdown("<div style='font-size:0.8rem;color:#6B4C30;margin:-0.5rem 0 1rem;'>Also consider: " +
                    " · ".join(f"<em>{s}</em>" for s in sec[:3]) + "</div>", unsafe_allow_html=True)

    # ════════════════════════════════════════
    # SECTION 2: DOSHA BALANCE
    # ════════════════════════════════════════
    st.markdown('<div class="an-section-div"><span class="text">Your Doshic Constitution</span></div>', unsafe_allow_html=True)

    doshas = [
        ("Vata", "💨", "Air & Movement — nerves, joints, elimination"),
        ("Pitta","🔥", "Fire & Metabolism — digestion, skin, intelligence"),
        ("Kapha","🌊", "Water & Structure — immunity, fluids, stability"),
    ]
    for dname, demoji, ddesc in doshas:
        pct = dosha_pct.get(dname, 33.3)
        tc, fc, bc = _dosha_color(dname)
        st.markdown(f"""
        <div class="dosha-row">
            <div class="dosha-row-top">
                <span class="dosha-row-name" style="color:{tc};">{demoji} {dname}</span>
                <span class="dosha-row-pct" style="color:{tc};">{pct:.0f}%</span>
            </div>
            <div class="dosha-track">
                <div class="dosha-fill" style="width:{pct:.1f}%;background:{fc};"></div>
            </div>
            <div style="font-size:0.76rem;color:#6B4C30;margin-top:3px;">{ddesc}</div>
        </div>
        """, unsafe_allow_html=True)

    # ════════════════════════════════════════
    # SECTION 3: INTERNAL STATE
    # ════════════════════════════════════════
    st.markdown('<div class="an-section-div"><span class="text">Internal State Assessment</span></div>', unsafe_allow_html=True)

    agni_v, agni_sub = _agni_html(agni)
    kv, ks = _koshtha_html(koshtha)
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(f"""<div class="an-mini-metric">
            <div class="m-label">Ama (Toxin Level)</div>
            <div class="m-value">{_ama_html(ama_status)}</div>
        </div>""", unsafe_allow_html=True)
    with mc2:
        st.markdown(f"""<div class="an-mini-metric">
            <div class="m-label">Agni (Digestive Fire)</div>
            <div class="m-value">{agni_v}</div>
            <div class="m-sub">{agni_sub}</div>
        </div>""", unsafe_allow_html=True)
    with mc3:
        st.markdown(f"""<div class="an-mini-metric">
            <div class="m-label">Koshtha (Bowel Type)</div>
            <div class="m-value" style="color:#3D1F08;font-weight:700;">{kv}</div>
            <div class="m-sub">{ks}</div>
        </div>""", unsafe_allow_html=True)

    # Affected tissues
    if dhatus or srotas:
        st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
        tc_col, sc_col = st.columns(2)
        with tc_col:
            if dhatus:
                st.markdown(f"<div style='font-size:0.75rem;font-weight:700;color:#7C4A20;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;'>Tissues Affected (Dhatu)</div>"
                            + "".join(f"<span class='sym-chip-mild'>{d}</span>" for d in dhatus[:4]),
                            unsafe_allow_html=True)
        with sc_col:
            if srotas:
                st.markdown(f"<div style='font-size:0.75rem;font-weight:700;color:#7C4A20;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;'>Channels Affected (Srotas)</div>"
                            + "".join(f"<span class='sym-chip-mild'>{s}</span>" for s in srotas[:4]),
                            unsafe_allow_html=True)

    # Ama reasoning
    if ama_reasons:
        with st.expander("Why is Ama present? (Clinical reasoning)", expanded=False):
            for r in ama_reasons:
                st.markdown(f"- {r}")

    # ════════════════════════════════════════
    # SECTION 4: HEALING PLAN
    # ════════════════════════════════════════
    st.markdown('<div class="an-section-div"><span class="text">Your Healing Plan</span></div>', unsafe_allow_html=True)

    # Phase 1: Deepana-Pachana
    deepana = getattr(tx, "deepana_pachana_protocol", [])
    if deepana:
        st.markdown("<div class='an-label'>Phase 1 — Rekindle Digestive Fire First</div>", unsafe_allow_html=True)
        st.markdown("<div class='an-card-warm'>", unsafe_allow_html=True)
        for dp in deepana:
            st.markdown(f"<div style='padding:6px 0;border-bottom:1px solid #EDE5D8;font-size:0.9rem;color:#3D1F08;'>🍵 {dp}</div>",
                        unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Phase 2: Herbal formulations
    formulas = getattr(tx, "shamana_formulations", [])
    if formulas:
        st.markdown("<div class='an-label' style='margin-top:1rem;'>Phase 2 — Classical Herbal Formulations</div>", unsafe_allow_html=True)
        for i, f in enumerate(formulas):
            tag_cls, tag_lbl = _tag(getattr(f,"category",""))
            dosage  = getattr(f,"dosage","")
            anupana = getattr(f,"anupana_vehicle","")
            kala    = getattr(f,"aushadha_sevana_kala","")
            ref     = getattr(f,"classical_reference","")
            ind     = getattr(f,"classical_indication","")
            dur     = getattr(f,"duration_weeks",None)
            st.markdown(f"""
            <div class="an-remedy">
                <div class="an-remedy-name">
                    {i+1}. {f.name}
                    <span class="an-tag {tag_cls}">{tag_lbl}</span>
                    {f'<span style="font-size:0.76rem;color:#6B4C30;margin-left:8px;">{dur} weeks</span>' if dur else ''}
                </div>
                <div class="an-remedy-ind">{ind}</div>
                <div class="an-remedy-meta">
                    <span>💊 {dosage}</span>
                    <span>🥛 {anupana}</span>
                    <span>⏰ {kala}</span>
                </div>
                {f'<div class="an-remedy-ref">📖 {ref}</div>' if ref else ''}
            </div>
            """, unsafe_allow_html=True)

    # Phase 3: Diet
    dietary = getattr(tx, "dietary_and_lifestyle_regimen", None)
    if dietary:
        good_food = (getattr(dietary,"pathya_ahara_wholesome_diet",None)
                     or getattr(dietary,"pathya_ahara_beneficial_foods",[]))
        bad_food  = (getattr(dietary,"apathya_ahara_unwholesome_diet",None)
                     or getattr(dietary,"apathya_ahara_contraindicated_foods",[]))
        good_life = (getattr(dietary,"pathya_vihara_recommended_lifestyle",None)
                     or getattr(dietary,"pathya_vihara_beneficial_lifestyle",[]))
        bad_life  = getattr(dietary,"apathya_vihara_contraindicated_habits",[])

        if good_food or bad_food:
            st.markdown("<div class='an-label' style='margin-top:1rem;'>Phase 3 — Food as Medicine</div>", unsafe_allow_html=True)
            fc1, fc2 = st.columns(2)
            with fc1:
                st.markdown("<div class='an-card-success'><div style='font-weight:700;color:#14532D;margin-bottom:8px;font-size:0.9rem;'>✅ Eat More Of</div>", unsafe_allow_html=True)
                for item in good_food:
                    st.markdown(f"<div class='food-good'><span>✓</span><span>{item}</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with fc2:
                st.markdown("<div class='an-card-danger'><div style='font-weight:700;color:#7F1D1D;margin-bottom:8px;font-size:0.9rem;'>❌ Avoid These</div>", unsafe_allow_html=True)
                for item in bad_food:
                    st.markdown(f"<div class='food-bad'><span>✗</span><span>{item}</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        if good_life or bad_life:
            with st.expander("Daily Routine & Lifestyle (Dinacharya)", expanded=False):
                lc1, lc2 = st.columns(2)
                with lc1:
                    st.markdown("**✅ Recommended Habits**")
                    for h in good_life: st.markdown(f"- {h}")
                with lc2:
                    if bad_life:
                        st.markdown("**❌ Habits to Avoid**")
                        for h in bad_life: st.markdown(f"- {h}")

    # Other phases (collapsed)
    panchakarma = getattr(tx,"panchakarma_roadmap",None)
    if panchakarma:
        with st.expander("🌊 Panchakarma & Detox Roadmap (Phase 4)", expanded=False):
            for k, v in (panchakarma if isinstance(panchakarma,dict) else {}).items():
                st.markdown(f"**{k}:** {v}")

    yoga = getattr(tx,"yoga_pranayama",None)
    if yoga:
        with st.expander("🧘 Yoga & Pranayama (Phase 5)", expanded=False):
            if isinstance(yoga,list):
                for y in yoga: st.markdown(f"- {y}")
            elif isinstance(yoga,dict):
                for k,v in yoga.items(): st.markdown(f"**{k}:** {v}")

    rasayana = getattr(tx,"rasayana_rejuvenation",None)
    if rasayana:
        with st.expander("✨ Rasayana — Rejuvenation (Phase 6)", expanded=False):
            if isinstance(rasayana,list):
                for r in rasayana: st.markdown(f"- {r}")

    # Red flags
    red_flags = getattr(tx,"red_flag_warnings",[])
    if red_flags:
        st.markdown("""<div class="an-card-danger" style="margin-top:1.2rem;">
            <div style="font-weight:700;color:#7F1D1D;margin-bottom:8px;">
                🚨 Seek Emergency Medical Care If You Experience:
            </div>""", unsafe_allow_html=True)
        for rf in red_flags:
            st.markdown(f"<div style='padding:4px 0;font-size:0.88rem;color:#991B1B;'>• {rf}</div>",
                        unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ════════════════════════════════════════
    # SECTION 5: ASK AYURVAIDYA
    # ════════════════════════════════════════
    st.markdown('<div class="an-section-div"><span class="text">Ask AyurVaidya</span></div>', unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.88rem;color:#6B4C30;margin-bottom:0.8rem;'>Have questions about your diet, remedies, or daily routine? Ask below.</div>",
                unsafe_allow_html=True)

    # Quick questions as buttons
    quick_qs = [
        f"Best breakfast and dinner for {dx.primary_condition}?",
        "What kitchen remedies can I use daily at home?",
        "How long will it take to see improvement?",
        "What should I avoid doing or eating right now?",
    ]
    qc1, qc2 = st.columns(2)
    for i, q in enumerate(quick_qs):
        with (qc1 if i % 2 == 0 else qc2):
            if st.button(q, key=f"qq_{i}", use_container_width=True):
                st.session_state["prefill_q"] = q

    prefill = st.session_state.pop("prefill_q", None) or ""
    user_q  = st.text_area(
        "Your question",
        value=prefill if prefill else st.session_state.get("_last_q",""),
        placeholder="Ask anything about your condition, remedies, foods, or lifestyle...",
        height=80,
        key="aq_input",
        label_visibility="collapsed"
    )

    ac1, ac2 = st.columns([2,1])
    with ac1:
        if st.button("✨ Get Guidance", type="primary", use_container_width=True, key="btn_ask"):
            if user_q.strip():
                st.session_state["_last_q"] = user_q
                with st.spinner("AyurVaidya is consulting the classical texts..."):
                    name_s  = st.session_state.patient_name
                    age_s   = st.session_state.patient_age
                    gender_s= st.session_state.patient_gender
                    p_sum = f"{name_s}, {age_s} yrs, {gender_s}."
                    d_sum = f"{dx.primary_condition} ({dx.sanskrit_name}) — {dx.doshic_subtype}"
                    t_sum = ", ".join([f.name for f in formulas[:3]]) if formulas else "—"
                    try:
                        resp = ai.synthesize_consultation(
                            patient_summary=p_sum,
                            diagnosis_summary=d_sum,
                            treatment_summary=t_sum,
                            user_question=user_q,
                            mode="layman"
                        )
                    except Exception:
                        resp = "AyurVaidya is currently unavailable. Please check your API key configuration."
                    st.session_state.last_q_response = resp
    with ac2:
        if st.session_state.last_q_response:
            if st.button("Clear", use_container_width=True):
                st.session_state.last_q_response = ""
                st.session_state["_last_q"] = ""
                st.rerun()

    if st.session_state.last_q_response:
        st.markdown(f"""
        <div class="chat-q">{st.session_state.get('_last_q','Your question')}</div>
        <div class="chat-a">{st.session_state.last_q_response}</div>
        """, unsafe_allow_html=True)

    # ════════════════════════════════════════
    # SECTION 6: SAVE & DOWNLOAD
    # ════════════════════════════════════════
    st.markdown('<div class="an-section-div"><span class="text">Save Your Plan</span></div>', unsafe_allow_html=True)

    # Build case sheet
    patient_demo = PatientDemographics(
        name=st.session_state.patient_name,
        age=int(st.session_state.patient_age),
        gender=gender,
        current_season="Current Season"
    )
    ashta = AshtaSthanaPariksha(
        nadi_pulse="Pulse matching primary dosha",
        jihva_tongue=tongue_str,
        mutra_urine="Normal",
        mala_stool=stool_str,
        shabda_voice="Normal",
        sparsha_skin="Normal",
        druk_eyes="Clear",
        akruti_appearance="Moderate"
    )
    case_obj = ClinicalCase(
        patient=patient_demo, ashta_sthana=ashta, dashavidha=dasha,
        chief_complaints=list(sym.keys())[:8],
        onset_and_duration="Recent weeks",
        dosha_scores=dosha_pct, diagnosis=dx, treatment=tx
    )
    case_md = generate_markdown_case_sheet(case_obj)

    sv1, sv2 = st.columns(2)
    with sv1:
        if is_guest:
            st.info("💡 Sign in to save consultations to your account.")
        else:
            if st.button("💾 Save to My Records", type="primary", use_container_width=True):
                story = st.session_state.get("user_story","")
                cid = save_consultation(
                    user_id=user_id,
                    chief_complaint=story[:300] if story else ", ".join(list(sym.keys())[:4]),
                    symptoms=list(sym.keys()),
                    primary_condition=dx.primary_condition,
                    sanskrit_name=dx.sanskrit_name,
                    dosha_scores=dosha_pct,
                    treatment_summary=", ".join([f.name for f in formulas[:2]]) if formulas else "",
                    case_sheet_md=case_md
                )
                if cid:
                    st.success("✅ Saved to your health records!")
                else:
                    st.error("Failed to save. Please try again.")
    with sv2:
        st.download_button(
            "📥 Download Health Plan (.md)",
            data=case_md,
            file_name=f"AyurNidana_{st.session_state.patient_name.replace(' ','_')}_HealthPlan.md",
            mime="text/markdown",
            use_container_width=True
        )

    with st.expander("📄 Preview Clinical Case Sheet", expanded=False):
        st.markdown(case_md)


# ─────────────────────────────────────────────────────────────────
# HISTORY VIEW
# ─────────────────────────────────────────────────────────────────

def _render_history(user_id: int, is_guest: bool):
    st.markdown('<div class="an-page-title">My Health Records</div>', unsafe_allow_html=True)
    st.markdown('<div class="an-page-sub">All your saved consultations, sorted most recent first.</div>', unsafe_allow_html=True)

    if is_guest:
        st.markdown("""<div class="an-empty">
            <div class="ei">🔒</div><h3>Sign In to See History</h3>
            <p>Guest consultations are not stored. Create a free account to track your Ayurvedic health journey.</p>
        </div>""", unsafe_allow_html=True)
        return

    records = get_user_consultations(user_id)
    if not records:
        st.markdown("""<div class="an-empty">
            <div class="ei">📋</div><h3>No Records Yet</h3>
            <p>Complete a consultation and save it — it will appear here.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Start a Consultation →", type="primary"):
            st.session_state.view = "input"
            st.rerun()
        return

    st.markdown(f"**{len(records)} saved consultation{'s' if len(records)!=1 else ''}**")
    st.markdown("")

    for rec in records:
        date_str  = rec["created_at"][:10]
        d_scores  = rec.get("dosha_scores",{})
        dominant  = max(d_scores, key=d_scores.get) if d_scores else "—"
        dom_tc, dom_fc, _ = _dosha_color(dominant)

        with st.expander(f"🩺 {rec['primary_condition']} — {date_str}", expanded=False):
            hc1, hc2 = st.columns([3,2])
            with hc1:
                st.markdown(f"**{rec['primary_condition']}**")
                st.caption(f"*{rec['sanskrit_name']}*")
                if rec.get("chief_complaint"):
                    st.markdown(f"<div style='font-size:0.87rem;color:#3D1F08;margin-top:6px;'>{rec['chief_complaint'][:200]}</div>",
                                unsafe_allow_html=True)
                if rec.get("treatment_summary"):
                    st.markdown(f"<div style='font-size:0.83rem;color:#5C3D20;margin-top:5px;'>💊 {rec['treatment_summary']}</div>",
                                unsafe_allow_html=True)
            with hc2:
                if d_scores:
                    for d, v in d_scores.items():
                        tc2, fc2, _ = _dosha_color(d)
                        st.markdown(f"""
                        <div style='display:flex;align-items:center;gap:8px;margin-bottom:5px;'>
                            <span style='font-size:0.8rem;font-weight:700;color:{tc2};width:46px;'>{d}</span>
                            <div style='flex:1;background:#EDE5D8;border-radius:4px;height:7px;'>
                                <div style='width:{v:.0f}%;background:{fc2};height:7px;border-radius:4px;'></div>
                            </div>
                            <span style='font-size:0.78rem;color:#6B4C30;width:30px;text-align:right;'>{v:.0f}%</span>
                        </div>
                        """, unsafe_allow_html=True)
            if rec.get("case_sheet_md"):
                st.download_button(
                    "📥 Download Case Sheet",
                    data=rec["case_sheet_md"],
                    file_name=f"AyurNidana_{rec['primary_condition'].replace(' ','_')}_{date_str}.md",
                    mime="text/markdown",
                    key=f"dl_{rec['id']}"
                )


# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        main()
    except Exception as _e:
        import traceback
        st.error("🌿 AyurNidana encountered an issue. Please refresh.")
        with st.expander("Technical details"):
            st.code(traceback.format_exc())
