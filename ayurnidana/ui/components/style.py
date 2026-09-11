"""AyurNidana v3 — Clean, High-Contrast, Flowing Design.
Design Principles:
  - Pure white body, near-black text (#1C0F05) — maximum readability
  - No tabs, no sidebar, no checkboxes — pure linear flow
  - Two views: INPUT (describe symptoms) → RESULTS (healing plan)
  - Visual tap-to-select body checks (buttons as option cards)
  - Centered layout, mobile-inspired card design
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lora:ital,wght@0,500;0,600;1,400&display=swap');

/* ─── GLOBAL ─────────────────────────────────────── */
html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #F8F4EE !important;
    color: #1C0F05 !important;
}
h1, h2, h3 { font-family: 'Lora', Georgia, serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
}

/* ─── HIDE SIDEBAR ──────────────────────────────── */
[data-testid="stSidebar"],
section[data-testid="stSidebarContent"] {
    display: none !important;
}

/* ─── TABS (auth only) ──────────────────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #EDE5D8 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 0.45rem 1.2rem !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    color: #6B4C30 !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #7C2D12 !important;
    font-weight: 700 !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.1) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {
    padding-top: 1.2rem !important;
}

/* ─── BUTTONS ───────────────────────────────────── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.18s ease !important;
    border: none !important;
    cursor: pointer !important;
}
.stButton > button[kind="primary"] {
    background: #9C3B12 !important;
    color: #FFFFFF !important;
    box-shadow: 0 3px 12px rgba(156,59,18,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #7C2D0E !important;
    box-shadow: 0 5px 18px rgba(156,59,18,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    border: 1.5px solid #C9B59A !important;
    color: #3D1F08 !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #9C3B12 !important;
    color: #9C3B12 !important;
    background: #FEF6EF !important;
}
.stDownloadButton > button {
    background: #FFFFFF !important;
    border: 1.5px solid #C9B59A !important;
    border-radius: 10px !important;
    color: #3D1F08 !important;
    font-weight: 600 !important;
}
.stDownloadButton > button:hover {
    border-color: #9C3B12 !important;
    color: #9C3B12 !important;
}

/* ─── INPUTS ────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: #FFFFFF !important;
    border: 1.5px solid #C9B59A !important;
    border-radius: 10px !important;
    color: #1C0F05 !important;
    font-size: 0.95rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #9C3B12 !important;
    box-shadow: 0 0 0 3px rgba(156,59,18,0.12) !important;
    outline: none !important;
}
.stTextArea > div > div > textarea {
    min-height: 100px !important;
    line-height: 1.65 !important;
}
.stSelectbox > div > div {
    background: #FFFFFF !important;
    border: 1.5px solid #C9B59A !important;
    border-radius: 10px !important;
    color: #1C0F05 !important;
}

/* ─── LABELS ────────────────────────────────────── */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stNumberInput label {
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: #5C3D20 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* ─── EXPANDER ──────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #E0D4C3 !important;
    border-radius: 12px !important;
    background: #FFFFFF !important;
    margin-bottom: 0.6rem !important;
}
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #3D1F08 !important;
    font-size: 0.92rem !important;
    padding: 0.75rem 1rem !important;
}

/* ─── ALERTS ────────────────────────────────────── */
.stSuccess { background:#F0FAF4!important; border-left:3px solid #166534!important; border-radius:10px!important; color:#14532D!important; }
.stWarning { background:#FFFBEB!important; border-left:3px solid #92400E!important; border-radius:10px!important; }
.stError   { background:#FFF5F5!important; border-left:3px solid #991B1B!important; border-radius:10px!important; }
.stInfo    { background:#EFF6FF!important; border-left:3px solid #1D4ED8!important; border-radius:10px!important; }

/* ─── CAPTION ───────────────────────────────────── */
.stCaption { color: #6B4C30 !important; font-size: 0.83rem !important; }

/* ─── HR ────────────────────────────────────────── */
hr { border: none !important; border-top: 1px solid #E0D4C3 !important; margin: 1.4rem 0 !important; }

/* ─── SCROLLBAR ─────────────────────────────────── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: #C4A882; border-radius: 8px; }

/* ════════════════════════════════════════════════════
   COMPONENT CLASSES
════════════════════════════════════════════════════ */

/* Top nav bar */
.an-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 1.4rem 0;
    margin-bottom: 0.2rem;
    border-bottom: 1px solid #E0D4C3;
}
.an-topbar .logo {
    font-family: 'Lora', serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #5C2D0A;
}
.an-topbar .logo span { color: #9C3B12; }

/* Auth screen */
.an-auth-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    border: 1px solid #E0D4C3;
    box-shadow: 0 8px 32px rgba(60,20,5,0.07);
    max-width: 440px;
    margin: 0 auto;
}
.an-auth-logo {
    text-align: center;
    margin-bottom: 1.8rem;
}
.an-auth-logo .icon { font-size: 2.8rem; margin-bottom: 0.5rem; }
.an-auth-logo h2 {
    font-family: 'Lora', serif !important;
    font-size: 1.9rem !important;
    color: #4A1E06 !important;
    margin: 0 0 5px !important;
}
.an-auth-logo p { color: #6B4C30; font-size: 0.92rem; margin: 0; }

/* Page section header */
.an-page-title {
    font-family: 'Lora', serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: #2C1005;
    margin: 0 0 6px;
}
.an-page-sub {
    font-size: 0.92rem;
    color: #6B4C30;
    margin: 0 0 1.6rem;
    line-height: 1.6;
}

/* Section label */
.an-label {
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #7C4A20;
    margin-bottom: 0.5rem;
}

/* Cards */
.an-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    border: 1px solid #E0D4C3;
    box-shadow: 0 2px 8px rgba(60,20,5,0.04);
    margin-bottom: 1rem;
}
.an-card-warm {
    background: #FBF7F2;
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    border: 1px solid #E8DDD0;
    margin-bottom: 1rem;
}
.an-card-success {
    background: #F0FAF4;
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    border: 1px solid #BBD9C5;
    margin-bottom: 1rem;
}
.an-card-danger {
    background: #FFF5F5;
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    border: 1px solid #F5BCBC;
    margin-bottom: 1rem;
}

/* Diagnosis headline card */
.an-dx-card {
    background: linear-gradient(135deg, #3D1A06 0%, #5C2D0A 100%);
    border-radius: 18px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.4rem;
    position: relative;
    overflow: hidden;
}
.an-dx-card::after {
    content: '';
    position: absolute;
    top: -20px; right: -20px;
    width: 140px; height: 140px;
    background: radial-gradient(circle, rgba(255,180,80,0.14) 0%, transparent 70%);
    border-radius: 50%;
}
.an-dx-card .condition {
    font-family: 'Lora', serif;
    font-size: 1.45rem;
    font-weight: 600;
    color: #FDE8CF;
    margin: 0 0 5px;
}
.an-dx-card .sanskrit {
    font-size: 0.88rem;
    color: #C9A07A;
    font-style: italic;
    margin: 0 0 12px;
}
.an-dx-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #F5D5A8;
    border-radius: 20px;
    padding: 4px 13px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 6px;
    margin-top: 2px;
}

/* Dosha progress row */
.dosha-row {
    margin-bottom: 14px;
}
.dosha-row-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
}
.dosha-row-name {
    font-weight: 700;
    font-size: 0.93rem;
}
.dosha-row-pct {
    font-weight: 700;
    font-size: 1rem;
    font-family: 'Lora', serif;
}
.dosha-track {
    background: #EDE5D8;
    border-radius: 6px;
    height: 9px;
    overflow: hidden;
}
.dosha-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.6s ease;
}

/* Metric mini cards */
.an-mini-metric {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    border: 1px solid #E0D4C3;
    height: 100%;
}
.an-mini-metric .m-label {
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #7C4A20;
    margin-bottom: 5px;
}
.an-mini-metric .m-value {
    font-size: 0.9rem;
    font-weight: 700;
    color: #1C0F05;
    line-height: 1.3;
}
.an-mini-metric .m-sub {
    font-size: 0.78rem;
    color: #6B4C30;
    margin-top: 3px;
}

/* Remedy card */
.an-remedy {
    background: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E0D4C3;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    transition: box-shadow 0.2s;
}
.an-remedy:hover { box-shadow: 0 3px 12px rgba(60,20,5,0.07); }
.an-remedy-name {
    font-weight: 700;
    font-size: 0.95rem;
    color: #1C0F05;
    margin-bottom: 3px;
}
.an-remedy-ind {
    font-size: 0.82rem;
    color: #5C3D20;
    font-style: italic;
    margin-bottom: 7px;
}
.an-remedy-meta {
    font-size: 0.82rem;
    color: #3D1F08;
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
}
.an-remedy-ref {
    font-size: 0.73rem;
    color: #8C6040;
    margin-top: 5px;
}

/* Category tag */
.an-tag {
    display: inline-block;
    border-radius: 5px;
    padding: 2px 8px;
    font-size: 0.69rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-left: 6px;
    vertical-align: middle;
}
.tag-vati    { background:#FEF0E4; color:#92400E; }
.tag-kwatha  { background:#ECFDF5; color:#065F46; }
.tag-churna  { background:#FFFBEB; color:#78350F; }
.tag-asava   { background:#EEF2FF; color:#312E81; }
.tag-ghrita  { background:#F5F3FF; color:#4C1D95; }
.tag-taila   { background:#F0FDF4; color:#14532D; }
.tag-rasayana { background:#FDF2F8; color:#701A75; }
.tag-herbal  { background:#F3F4F6; color:#1F2937; }

/* Symptom chip */
.sym-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #FDF0E4;
    border: 1.5px solid #D97706;
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 0.83rem;
    font-weight: 600;
    color: #78350F;
    margin: 3px;
}
.sym-chip-mild {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #FFFBEB;
    border: 1.5px solid #D97706;
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 0.83rem;
    font-weight: 500;
    color: #92400E;
    margin: 3px;
}

/* Food list item */
.food-good { padding: 6px 0; border-bottom: 1px solid #D1FAE5; font-size: 0.88rem; color: #14532D; display: flex; align-items: flex-start; gap: 8px; }
.food-bad  { padding: 6px 0; border-bottom: 1px solid #FEE2E2; font-size: 0.88rem; color: #7F1D1D; display: flex; align-items: flex-start; gap: 8px; }

/* Section divider with text */
.an-section-div {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.8rem 0 1rem;
}
.an-section-div .text {
    font-family: 'Lora', serif;
    font-size: 1rem;
    font-weight: 600;
    color: #2C1005;
    white-space: nowrap;
}
.an-section-div::before,
.an-section-div::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #E0D4C3;
}

/* Empty state */
.an-empty {
    text-align: center;
    padding: 3rem 1rem;
    color: #7C4A20;
}
.an-empty .ei { font-size: 2.8rem; margin-bottom: 0.7rem; }
.an-empty h3 { color: #3D1A06 !important; margin-bottom: 0.4rem; font-size: 1.1rem; }
.an-empty p { font-size: 0.9rem; color: #6B4C30; max-width: 340px; margin: 0 auto; line-height: 1.6; }

/* Step dots */
.an-steps {
    display: flex;
    align-items: center;
    gap: 6px;
    justify-content: center;
}
.an-step-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #C9B59A;
    transition: all 0.3s;
}
.an-step-dot.active {
    width: 22px;
    border-radius: 4px;
    background: #9C3B12;
}
.an-step-dot.done { background: #166534; }

/* Body check option cards */
.bc-grid { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 1.2rem; }
.bc-option {
    flex: 1;
    min-width: 80px;
    background: #FFFFFF;
    border: 2px solid #E0D4C3;
    border-radius: 12px;
    padding: 12px 8px;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s;
}
.bc-option.selected {
    border-color: #9C3B12;
    background: #FEF6EF;
}
.bc-option .bc-icon { font-size: 1.6rem; display: block; margin-bottom: 4px; }
.bc-option .bc-label { font-size: 0.78rem; font-weight: 600; color: #3D1F08; }

/* Chat bubble */
.chat-q {
    background: #FEF6EF;
    border-radius: 12px 12px 12px 3px;
    padding: 0.9rem 1.1rem;
    font-size: 0.9rem;
    color: #2C1005;
    margin-bottom: 1rem;
    border: 1px solid #E8D5C0;
}
.chat-a {
    background: #FFFFFF;
    border-radius: 12px 12px 3px 12px;
    padding: 1rem 1.2rem;
    font-size: 0.9rem;
    color: #1C0F05;
    line-height: 1.7;
    border: 1px solid #E0D4C3;
    margin-bottom: 1rem;
}

/* Toast */
[data-testid="stToast"] {
    background: #2C1005 !important;
    color: #FDE8CF !important;
    border-radius: 12px !important;
}

/* History card */
.an-hist-card {
    background: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E0D4C3;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
    transition: box-shadow 0.2s, border-color 0.2s;
}
.an-hist-card:hover { border-color: #C9B59A; box-shadow: 0 3px 12px rgba(60,20,5,0.07); }

</style>
"""
