import streamlit as st
from database import Database
from menu_parser import extract_menu_items
from ai_chatbot import AIChatbot
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GrabEats Senior Helper",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Lora:wght@500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    font-size: 18px;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(160deg, #F2FFF5 0%, #FFFFFF 50%, #F7FFF9 100%);
    min-height: 100vh;
}

/* ══════════════════════════════════════════════
   SIDEBAR
   ══════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #00B14F 0%, #00622E 100%) !important;
    padding: 0.5rem 0.75rem !important;
}

/* Every text node inside sidebar → white */
[data-testid="stSidebar"],
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stMarkdown p {
    color: white !important;
}

/* Sidebar selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.18) !important;
    border: 1.5px solid rgba(255,255,255,0.35) !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: white !important;
}
[data-testid="stSidebar"] [data-baseweb="popover"] {
    background: #00833E !important;
}
[data-testid="stSidebar"] [role="option"] {
    background: #00833E !important;
    color: white !important;
}
[data-testid="stSidebar"] [role="option"]:hover {
    background: rgba(255,255,255,0.2) !important;
}

/* ── SIDEBAR NAVIGATION BUTTONS ── */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: rgba(255, 255, 255, 0.32) !important;
    border: 2px solid rgba(255, 255, 255, 0.6) !important;
    color: white !important;
    font-weight: 800 !important;
    font-size: 17px !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    text-align: left !important;
    width: 100% !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    transform: translateX(6px) !important;
    transition: all 0.3s ease !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: rgba(255, 255, 255, 0.38) !important;
    transform: translateX(6px) !important;
}

[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.13) !important;
    border: 1.5px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 17px !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    text-align: left !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255, 255, 255, 0.26) !important;
    transform: translateX(4px) !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

[data-testid="stSidebar"] .stButton > button:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.4) !important;
}

/* Sidebar dividers */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.3) !important;
    margin: 10px 0 !important;
}

/* Stats box */
.sidebar-stats {
    background: rgba(255,255,255,0.16);
    border-radius: 14px;
    padding: 14px 16px;
    margin-top: 8px;
    border: 1px solid rgba(255,255,255,0.2);
}
.sidebar-stats p { margin: 0 0 4px !important; font-size: 15px !important; opacity: 0.85; }
.sidebar-stats .stat-line { margin: 0 0 3px !important; font-size: 17px !important; font-weight: 800 !important; }

/* ── MOBILE: Hide sidebar on nav click ── */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        transition: transform 0.3s ease;
    }
}

/* ── Headings ── */
h1 {
    font-family: 'Lora', serif !important;
    font-size: clamp(28px, 5vw, 52px) !important;
    font-weight: 700 !important;
    color: #166534 !important;
    line-height: 1.15 !important;
}
h2 {
    font-family: 'Lora', serif !important;
    font-size: clamp(22px, 3.5vw, 38px) !important;
    color: #2C2C2C !important;
    font-weight: 600 !important;
}
h3 {
    font-size: clamp(20px, 2.5vw, 28px) !important;
    font-weight: 700 !important;
    color: #333 !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Nunito', sans-serif !important;
    font-size: clamp(16px, 2vw, 22px) !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #2E9E5B, #1F8048) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 14px 24px !important;
    height: auto !important;
    min-height: 56px !important;
    box-shadow: 0 4px 16px rgba(46,158,91,0.35) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(46,158,91,0.45) !important;
    background: linear-gradient(135deg, #3DB86E, #2E9E5B) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    font-size: 18px !important;
    border-radius: 12px !important;
    border: 2px solid #A7D7B8 !important;
    padding: 12px 16px !important;
    background: white !important;
    color: #1a1a1a !important;
    transition: border-color 0.2s;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #2E9E5B !important;
    box-shadow: 0 0 0 3px rgba(46,158,91,0.15) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stMultiSelect label, .stFileUploader label, .stSlider label {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #2C2C2C !important;
}

/* ── FIX: File uploader hover/focus green ── */
[data-testid="stFileUploadDropzone"]:hover {
    border-color: #2E9E5B !important;
    background: #E0FBE8 !important;
}
[data-testid="stFileUploadDropzone"]:focus-within {
    border-color: #2E9E5B !important;
    box-shadow: 0 0 0 3px rgba(46,158,91,0.15) !important;
}

/* ── FIX: Multiselect hover/focus green ── */
[data-baseweb="select"]:hover {
    border-color: #2E9E5B !important;
}

/* ── FIX: Button focus outline green ── */
.stButton > button:focus {
    outline: 2px solid #2E9E5B !important;
    outline-offset: 2px !important;
}
.stButton > button:focus:not(:active) {
    outline: 2px solid #2E9E5B !important;
    outline-offset: 2px !important;
}

/* ── FIX: Select slider hover/focus green ── */
[data-baseweb="slider"]:hover [role="slider"] {
    background-color: #2E9E5B !important;
}
[data-baseweb="slider"] [role="slider"]:focus {
    box-shadow: 0 0 0 3px rgba(46,158,91,0.3) !important;
    background-color: #2E9E5B !important;
}
/* ── Multiselect tags ── */
[data-baseweb="tag"] {
    background-color: #2E9E5B !important;
    border-radius: 8px !important;
    font-size: 16px !important;
}
[data-baseweb="tag"] span { color: white !important; }

/* ── Alerts ── */
.stAlert { font-size: 18px !important; border-radius: 14px !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] {
    font-size: clamp(16px, 2vw, 22px) !important;
    font-weight: 700 !important;
    padding: 12px 20px !important;
    color: #2C2C2C !important;
}
.stTabs [aria-selected="true"] {
    color: #2E9E5B !important;
    border-bottom: 3px solid #2E9E5B !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-size: 18px !important;
    font-weight: 700 !important;
    background: #F0FDF4 !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    color: #166534 !important;
}
.streamlit-expanderHeader:hover {
    background: #E0FBE8 !important;
    color: #166534 !important;
}
.streamlit-expanderHeader:focus {
    background: #D0F8DC !important;
    outline: 2px solid #2E9E5B !important;
    color: #166534 !important;
}
.streamlit-expanderHeader p,
.streamlit-expanderHeader span,
.streamlit-expanderHeader div {
    color: #166534 !important;
}
.streamlit-expanderHeader svg {
    fill: #166534 !important;
}
/* ── Expander Content Text Color Fix ── */
.streamlit-expanderContent {
    color: #1a1a1a !important;
}
.streamlit-expanderContent p,
.streamlit-expanderContent span,
.streamlit-expanderContent div,
.streamlit-expanderContent li,
.streamlit-expanderContent h1,
.streamlit-expanderContent h2,
.streamlit-expanderContent h3,
.streamlit-expanderContent h4,
.streamlit-expanderContent strong,
.streamlit-expanderContent em,
.streamlit-expanderContent b {
    color: #1a1a1a !important;
}
/* Fix markdown text inside expanders */
details .stMarkdown p,
details .stMarkdown span,
details .stMarkdown div,
details .stMarkdown li,
details .stMarkdown h1,
details .stMarkdown h2,
details .stMarkdown h3,
details .stMarkdown h4,
details .stMarkdown strong,
details .stMarkdown em,
details .stMarkdown b {
    color: #1a1a1a !important;
}
/* Fix badge text inside expanders */
details .badge {
    color: #166534 !important;
}
/* Fix paragraph text inside details */
details p {
    color: #1a1a1a !important;
}
details span {
    color: #1a1a1a !important;
}
details div {
    color: #1a1a1a !important;
}
/* ── Divider ── */
hr { border-color: #A7D7B8 !important; margin: 1.5rem 0 !important; }

/* ── Spinner ── */
/* ── Spinner ── */
.stSpinner > div { 
    border-top-color: #2E9E5B !important; 
}
.stSpinner {
    color: #1a1a1a !important;
}
.stSpinner p,
.stSpinner span,
.stSpinner div {
    color: #1a1a1a !important;
}
/* ── File uploader ── */
[data-testid="stFileUploadDropzone"] {
    border: 2px dashed #2E9E5B !important;
    border-radius: 16px !important;
    background: #F0FDF4 !important;
    font-size: 18px !important;
    padding: 24px !important;
}

/* ════════════════════════════════════════
   HERO BANNER
   ════════════════════════════════════════ */
.hero-banner {
    background: linear-gradient(135deg, #2E9E5B 0%, #166534 100%);
    border-radius: 24px;
    padding: clamp(24px, 4vw, 40px) clamp(20px, 4vw, 44px);
    margin-bottom: 28px;
    color: white;
    box-shadow: 0 8px 32px rgba(22,101,52,0.3);
}
.hero-banner h1 {
    color: white !important;
    font-size: clamp(26px, 4vw, 48px) !important;
    margin: 0 0 10px !important;
}
.hero-banner p {
    font-size: clamp(16px, 2vw, 22px) !important;
    opacity: 0.93;
    margin: 0;
    font-weight: 600;
    color: white !important;
}

/* ════════════════════════════════════════
   FEATURE CARDS — responsive grid
   ════════════════════════════════════════ */
.feature-card {
    background: white;
    border-radius: 20px;
    padding: clamp(18px, 2.5vw, 28px) clamp(14px, 2vw, 24px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.07);
    border: 1.5px solid #BBF0D0;
    border-top: 4px solid #2E9E5B;
    text-align: center;
    height: 100%;
    margin-bottom: 16px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.feature-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 26px rgba(46,158,91,0.15);
}
.feature-card .icon { font-size: clamp(36px, 5vw, 52px); margin-bottom: 10px; }
.feature-card h4 {
    font-size: clamp(17px, 2vw, 24px) !important;
    font-weight: 800;
    color: #166534 !important;
    margin: 0 0 8px;
}
.feature-card p {
    font-size: clamp(14px, 1.5vw, 18px) !important;
    color: #555 !important;
    line-height: 1.5;
    margin: 0;
}

/* ════════════════════════════════════════
   HOW-TO-USE STEPS — text always dark
   ════════════════════════════════════════ */
.step-row {
    display: flex;
    align-items: flex-start;
    margin-bottom: 14px;
    background: white;
    border-radius: 14px;
    padding: 14px 18px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    border: 1.5px solid #BBF0D0;
}
.step-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    min-width: 40px;
    background: #2E9E5B;
    color: white !important;
    border-radius: 50%;
    font-size: 20px;
    font-weight: 800;
    margin-right: 14px;
    flex-shrink: 0;
}
.step-row p {
    margin: 0 !important;
    font-size: clamp(15px, 1.8vw, 20px) !important;
    color: #1a1a1a !important;
    padding-top: 8px;
    line-height: 1.5;
}

/* ════════════════════════════════════════
   RESTAURANT CARDS
   ════════════════════════════════════════ */
.restaurant-card {
    background: white;
    border-radius: 18px;
    padding: clamp(16px, 2vw, 22px) clamp(14px, 1.8vw, 20px);
    box-shadow: 0 3px 14px rgba(0,0,0,0.08);
    border: 1.5px solid #BBF0D0;
    border-top: 5px solid #2E9E5B;
    height: 100%;
    margin-bottom: 16px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.restaurant-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 26px rgba(0,0,0,0.13);
}
.restaurant-card .r-name {
    font-size: clamp(17px, 2vw, 24px) !important;
    font-weight: 800;
    color: #166534 !important;
    margin: 0 0 8px;
}
.restaurant-card .r-loc {
    font-size: clamp(14px, 1.5vw, 18px) !important;
    color: #555 !important;
    margin: 0 0 10px;
}
.restaurant-card .r-items {
    font-size: clamp(13px, 1.4vw, 16px) !important;
    color: #2E9E5B !important;
    font-weight: 700;
}

/* ════════════════════════════════════════
   SENIOR CARD (History page)
   ════════════════════════════════════════ */
.senior-card {
    background: white;
    border-radius: 20px;
    padding: clamp(18px, 2.5vw, 28px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border: 1.5px solid #BBF0D0;
    border-left: 6px solid #2E9E5B;
    margin-bottom: 18px;
    transition: box-shadow 0.2s;
}
.senior-card:hover { box-shadow: 0 8px 30px rgba(0,0,0,0.12); }
.senior-card h3 {
    margin-top: 0 !important;
    color: #166534 !important;
    font-size: clamp(18px, 2vw, 26px) !important;
}
.senior-card p {
    font-size: clamp(15px, 1.6vw, 20px) !important;
    color: #333 !important;
    margin: 6px 0;
}

/* ════════════════════════════════════════
   BADGE
   ════════════════════════════════════════ */
.badge {
    display: inline-block;
    background: #F0FDF4;
    color: #166534 !important;
    border: 1px solid #86EFAC;
    border-radius: 30px;
    padding: 5px 14px;
    font-size: clamp(13px, 1.4vw, 17px) !important;
    font-weight: 700;
    margin: 4px 4px 4px 0;
}
/* ════════════════════════════════════════
   CHAT BUBBLES
   ════════════════════════════════════════ */
.chat-bubble-user {
    background: linear-gradient(135deg, #2E9E5B, #1F8048);
    color: white !important;
    border-radius: 18px 18px 4px 18px;
    padding: clamp(14px, 2vw, 18px) clamp(16px, 2vw, 22px);
    margin: 10px 0 10px clamp(20px, 8vw, 60px);
    font-size: clamp(15px, 1.6vw, 20px) !important;
    line-height: 1.6;
    box-shadow: 0 3px 12px rgba(46,158,91,0.25);
}
.chat-bubble-user p,
.chat-bubble-user span,
.chat-bubble-user div,
.chat-bubble-user li,
.chat-bubble-user h1,
.chat-bubble-user h2,
.chat-bubble-user h3,
.chat-bubble-user h4,
.chat-bubble-user strong,
.chat-bubble-user em {
    color: white !important;
}
.chat-bubble-bot {
    background: white;
    color: #1a1a1a !important;
    border-radius: 18px 18px 18px 4px;
    padding: clamp(14px, 2vw, 20px) clamp(16px, 2vw, 24px);
    margin: 10px clamp(20px, 8vw, 60px) 10px 0;
    font-size: clamp(15px, 1.6vw, 20px) !important;
    line-height: 1.7;
    box-shadow: 0 3px 12px rgba(0,0,0,0.09);
    border: 1.5px solid #BBF0D0;
    border-left: 5px solid #2E9E5B;
}
.chat-bubble-bot p,
.chat-bubble-bot span,
.chat-bubble-bot div,
.chat-bubble-bot li,
.chat-bubble-bot h1,
.chat-bubble-bot h2,
.chat-bubble-bot h3,
.chat-bubble-bot h4,
.chat-bubble-bot strong,
.chat-bubble-bot em {
    color: #1a1a1a !important;
}
.chat-label {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
    color: #888 !important;
}
.chat-label p,
.chat-label span,
.chat-label div {
    color: #888 !important;
}
.chat-label.user-label { 
    text-align: right; 
    color: #2E9E5B !important; 
}
.chat-label.user-label p,
.chat-label.user-label span,
.chat-label.user-label div {
    color: #2E9E5B !important;
}
            
/* ════════════════════════════════════════
   PAGE HEADER
   ════════════════════════════════════════ */
.page-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 24px;
    padding-bottom: 18px;
    border-bottom: 3px solid #A7D7B8;
}
.page-header .ph-icon { font-size: clamp(32px, 5vw, 48px); }
.page-header h2 { margin: 0 !important; }

/* ════════════════════════════════════════
   TIP BOX
   ════════════════════════════════════════ */
.tip-box {
    background: #FFFBF0;
    border: 2px solid #86EFAC;
    border-radius: 16px;
    padding: 16px 20px;
    margin: 14px 0;
    font-size: clamp(15px, 1.6vw, 19px) !important;
    color: #1a4a2e !important;
}
.tip-box strong { color: #15803D !important; }

/* ════════════════════════════════════════
   BUDGET DISPLAY BOX
   ════════════════════════════════════════ */
.budget-display {
    background: #F0FDF4;
    border-radius: 10px;
    padding: 10px 14px;
    text-align: center;
    font-size: clamp(17px, 2vw, 22px) !important;
    font-weight: 800;
    color: #166534 !important;
    margin-top: 8px;
    border: 1.5px solid #BBF0D0;
}

/* ════════════════════════════════════════
   RESPONSIVE — small screens
   ════════════════════════════════════════ */
@media (max-width: 768px) {
    .hero-banner { padding: 20px 18px; border-radius: 16px; }
    .feature-card { margin-bottom: 12px; }
    .restaurant-card { margin-bottom: 12px; }
    .step-row { padding: 12px 14px; }
    .step-badge { width: 34px; height: 34px; min-width: 34px; font-size: 17px; margin-right: 10px; }
    .chat-bubble-user { margin-left: 12px; }
    .chat-bubble-bot { margin-right: 12px; }
}

/* ── Hide Streamlit chrome ── */
footer { display: none !important; }
#MainMenu { visibility: hidden !important; }
.viewerBadge_container__1QSob { display: none !important; }
/* ════════════════════════════════════════
   FIX: Expander hover/focus - green text
   ════════════════════════════════════════ */
details summary {
    color: #166534 !important;
}
details summary p,
details summary span,
details summary div {
    color: #166534 !important;
}
details summary:hover {
    background-color: #E0FBE8 !important;
    color: #166534 !important;
}
details summary:focus {
    outline-color: #2E9E5B !important;
    background-color: #D0F8DC !important;
    color: #166534 !important;
}
details[open] summary {
    background-color: #D0F8DC !important;
    border-bottom: 2px solid #2E9E5B !important;
    color: #166534 !important;
}
            /* ── Fix Add Restaurant success & expander text ── */
.stAlert {
    color: #1a1a1a !important;
}
.stAlert p,
.stAlert span,
.stAlert div,
.stAlert strong,
.stAlert b {
    color: #1a1a1a !important;
}
/* Success alert specific */
.stAlert [data-testid="stSuccess"] p,
.stAlert [data-testid="stSuccess"] span {
    color: #1a1a1a !important;
}
/* Info alert */
.stAlert [data-testid="stInfo"] p,
.stAlert [data-testid="stInfo"] span {
    color: #1a1a1a !important;
}
/* Warning alert */
.stAlert [data-testid="stWarning"] p,
.stAlert [data-testid="stWarning"] span {
    color: #1a1a1a !important;
}
/* Fix expander content in Add Restaurant */
.streamlit-expanderContent .stMarkdown p {
    color: #1a1a1a !important;
}
.streamlit-expanderContent .stMarkdown span {
    color: #1a1a1a !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Mobile Sidebar Hide Script ──────────────────────────────────────────────────
st.markdown("""
<script>
// Hide sidebar on mobile when navigation occurs
const mediaQuery = window.matchMedia('(max-width: 768px)');
function handleMobileSidebar() {
    if (mediaQuery.matches) {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            // Listen for button clicks in sidebar
            const buttons = sidebar.querySelectorAll('button');
            buttons.forEach(button => {
                button.addEventListener('click', function() {
                    // Small delay to let Streamlit process the click
                    setTimeout(() => {
                        const closeButton = document.querySelector('[data-testid="stSidebarCollapseButton"]');
                        if (closeButton && !sidebar.classList.contains('collapsed')) {
                            closeButton.click();
                        }
                    }, 300);
                });
            });
        }
    }
}
// Run on load
handleMobileSidebar();
// Re-run on resize
window.addEventListener('resize', handleMobileSidebar);
</script>
""", unsafe_allow_html=True)

# ─── Init DB & Chatbot ───────────────────────────────────────────────────────────
db = Database('grab_helper.db')
api_key = os.getenv('GOOGLE_API_KEY')
chatbot = None
if api_key:
    chatbot = AIChatbot(api_key)

# ─── Session State ───────────────────────────────────────────────────────────────
if 'restaurants_loaded' not in st.session_state:
    st.session_state.restaurants_loaded = False

if not st.session_state.restaurants_loaded:
    st.session_state.restaurants = {}
    for r in db.get_restaurants():
        res_id, res_name, res_loc = r[0], r[1], r[2]
        all_items = []
        for m in db.get_menus(res_id):
            for d in db.get_dishes(m[0]):
                all_items.append(f"{d[2]} (${d[3]:.2f})")
        st.session_state.restaurants[res_name] = {
            'id': res_id, 'location': res_loc, 'items': all_items
        }
    st.session_state.restaurants_loaded = True

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'active_page' not in st.session_state:
    st.session_state.active_page = 'home'

# ─── Language Config ─────────────────────────────────────────────────────────────
LANGUAGES = {
    '🇬🇧  English': 'English',
    '🇨🇳  中文 (Chinese)': 'Simplified Chinese',
    '🇲🇾  Bahasa Melayu': 'Malay',
    '🇮🇳  தமிழ் (Tamil)': 'Tamil'
}

NAV_KEYS = ['home', 'food_assistant', 'add_restaurant', 'history']

NAV_LABELS = {
    'English': {
        'home': '🏠  Home',
        'food_assistant': '🤖  Food Assistant',
        'add_restaurant': '📄  Add Restaurant',
        'history': '📋  History & Restaurants'
    },
    'Simplified Chinese': {
        'home': '🏠  首页',
        'food_assistant': '🤖  美食助手',
        'add_restaurant': '📄  添加餐厅',
        'history': '📋  历史与餐厅'
    },
    'Malay': {
        'home': '🏠  Laman Utama',
        'food_assistant': '🤖  Pembantu Makanan',
        'add_restaurant': '📄  Tambah Restoran',
        'history': '📋  Sejarah & Restoran'
    },
    'Tamil': {
        'home': '🏠  முகப்பு',
        'food_assistant': '🤖  உணவு உதவியாளர்',
        'add_restaurant': '📄  உணவகம் சேர்க்கவும்',
        'history': '📋  வரலாறு & உணவகங்கள்'
    }
}

PAGE_TITLES = {
    'English': {
        'home': 'Home',
        'food_assistant': 'Food Assistant',
        'add_restaurant': 'Add Restaurant',
        'history': 'History & Restaurants'
    },
    'Simplified Chinese': {
        'home': '首页',
        'food_assistant': '美食助手',
        'add_restaurant': '添加餐厅',
        'history': '历史与餐厅'
    },
    'Malay': {
        'home': 'Laman Utama',
        'food_assistant': 'Pembantu Makanan',
        'add_restaurant': 'Tambah Restoran',
        'history': 'Sejarah & Restoran'
    },
    'Tamil': {
        'home': 'முகப்பு',
        'food_assistant': 'உணவு உதவியாளர்',
        'add_restaurant': 'உணவகம் சேர்க்கவும்',
        'history': 'வரலாறு & உணவகங்கள்'
    }
}

PLACEHOLDERS = {
    'English': "E.g. I want something soft and warm for lunch, maybe porridge...",
    'Simplified Chinese': "例如：我想吃软一点的午餐，也许是粥...",
    'Malay': "Cth: Saya mahu sesuatu yang lembut dan hangat untuk makan tengah hari...",
    'Tamil': "எ.கா: மதிய உணவுக்கு மென்மையான சூடான உணவு வேண்டும்...",
}

DIETARY_OPTIONS = {
    'English': ["No Pork 🐷", "No Beef 🐄", "No Seafood 🐟", "No Nuts 🥜", "No Dairy 🥛", "Not Spicy 🌶️", "Vegetarian 🥦", "Halal ☪️"],
    'Simplified Chinese': ["不吃猪肉 🐷", "不吃牛肉 🐄", "不吃海鲜 🐟", "不吃坚果 🥜", "不吃乳制品 🥛", "不辣 🌶️", "素食 🥦", "清真 ☪️"],
    'Malay': ["Tiada Babi 🐷", "Tiada Daging Lembu 🐄", "Tiada Makanan Laut 🐟", "Tiada Kacang 🥜", "Tiada Tenusu 🥛", "Tidak Pedas 🌶️", "Vegetarian 🥦", "Halal ☪️"],
    'Tamil': ["பன்றி இல்லை 🐷", "மாட்டிறைச்சி இல்லை 🐄", "கடல் உணவு இல்லை 🐟", "கொட்டை இல்லை 🥜", "பால் இல்லை 🥛", "காரம் வேண்டாம் 🌶️", "சைவம் 🥦", "ஹலால் ☪️"],
}

SEARCH_BTN = {'English': '🔍  Find Food For Me!', 'Simplified Chinese': '🔍  为我找美食！', 'Malay': '🔍  Cari Makanan Untuk Saya!', 'Tamil': '🔍  உணவு தேடு!'}
BUDGET_LBL = {'English': 'Your budget per dish (SGD $)', 'Simplified Chinese': '每道菜的预算（新币）', 'Malay': 'Belanjawan anda per hidangan (SGD $)', 'Tamil': 'ஒரு உணவுக்கான பட்ஜெட் (SGD $)'}
DIET_LBL   = {'English': 'Foods you CANNOT eat:', 'Simplified Chinese': '您不能吃的食物：', 'Malay': 'Makanan yang TIDAK boleh dimakan:', 'Tamil': 'சாப்பிட முடியாத உணவுகள்:'}

HOME_FEATURES = {
    'English': [
        ("🤖", "Talk to me", "Tell me what you'd like to eat and I'll find the best dishes for you."),
        ("📄", "Add a Menu", "Share a restaurant's menu with me and I'll remember all the dishes."),
        ("💰", "Save Money", "Tell me your budget and I'll only show you what fits your wallet."),
        ("🛡️", "Eat Safely", "Tell me what you can't eat and I'll make sure you stay safe and healthy."),
    ],
    'Simplified Chinese': [
        ("🤖", "跟我聊聊", "告诉我您想吃什么，我会为您找到最好的菜肴。"),
        ("📄", "添加菜单", "分享餐厅菜单给我，我会记住所有菜品。"),
        ("💰", "省钱", "告诉我您的预算，我只显示适合您的选择。"),
        ("🛡️", "安全饮食", "告诉我您不能吃什么，我会确保您的安全与健康。"),
    ],
    'Malay': [
        ("🤖", "Bercakap dengan Saya", "Beritahu saya apa yang anda ingin makan dan saya akan cari hidangan terbaik."),
        ("📄", "Tambah Menu", "Kongsi menu restoran dengan saya dan saya akan ingat semua hidangan."),
        ("💰", "Jimat Wang", "Beritahu belanjawan anda dan saya akan tunjukkan yang sesuai."),
        ("🛡️", "Makan Selamat", "Beritahu saya apa yang anda tidak boleh makan dan saya pastikan anda selamat."),
    ],
    'Tamil': [
        ("🤖", "என்னிடம் பேசுங்கள்", "நீங்கள் என்ன சாப்பிட விரும்புகிறீர்கள் என்று சொல்லுங்கள், சிறந்த உணவைக் கண்டுபிடிப்பேன்."),
        ("📄", "மெனு சேர்க்கவும்", "உணவக மெனுவைப் பகிருங்கள், அனைத்து உணவுகளையும் நினைவில் கொள்கிறேன்."),
        ("💰", "பணம் சேமிக்க", "உங்கள் பட்ஜெட்டைச் சொல்லுங்கள், பொருத்தமானவற்றை மட்டும் காட்டுகிறேன்."),
        ("🛡️", "பாதுகாப்பாக சாப்பிட", "எதைச் சாப்பிட முடியாது என்று சொல்லுங்கள், பாதுகாப்பாக வைத்திருப்பேன்."),
    ],
}

HOME_STEPS = {
    'English': [
        ("1", "Pick your favorite language on the left side."),
        ("2", "Go to <b>🤖 Food Assistant</b> and tell me what you feel like eating."),
        ("3", "Let me know if there are foods you need to avoid (like pork or seafood)."),
        ("4", "Set your price range and press the big green button!"),
        ("5", "Look at my suggestions and enjoy a wonderful meal! 😊"),
    ],
    'Simplified Chinese': [
        ("1", "在左侧选择您喜欢的语言。"),
        ("2", "前往<b>🤖 美食助手</b>，告诉我您想吃什么。"),
        ("3", "告诉我您需要避免的食物（如猪肉或海鲜）。"),
        ("4", "设定您的价格范围，然后按绿色大按钮！"),
        ("5", "查看我的建议，享受美好的一餐！😊"),
    ],
    'Malay': [
        ("1", "Pilih bahasa kegemaran anda di sebelah kiri."),
        ("2", "Pergi ke <b>🤖 Pembantu Makanan</b> dan beritahu saya apa yang anda ingin makan."),
        ("3", "Beritahu saya jika ada makanan yang perlu dielakkan (seperti babi atau makanan laut)."),
        ("4", "Tetapkan julat harga anda dan tekan butang hijau besar!"),
        ("5", "Lihat cadangan saya dan nikmati hidangan yang hebat! 😊"),
    ],
    'Tamil': [
        ("1", "இடது பக்கத்தில் உங்களுக்கு பிடித்த மொழியைத் தேர்ந்தெடுக்கவும்."),
        ("2", "<b>🤖 உணவு உதவியாளர்</b> சென்று நீங்கள் என்ன சாப்பிட விரும்புகிறீர்கள் என்று சொல்லுங்கள்."),
        ("3", "தவிர்க்க வேண்டிய உணவுகள் (பன்றி இறைச்சி அல்லது கடல் உணவு போன்றவை) இருந்தால் சொல்லுங்கள்."),
        ("4", "விலை வரம்பை அமைத்து பெரிய பச்சை பொத்தானை அழுத்தவும்!"),
        ("5", "எனது பரிந்துரைகளைப் பார்த்து சிறந்த உணவை அனுபவியுங்கள்! 😊"),
    ],
}

HOME_NO_RESTAURANTS = {
    'English': '<strong>💡 No restaurants yet!</strong> Go to <b>📄 Add Restaurant</b> on the left to share a menu with me and get started.',
    'Simplified Chinese': '<strong>💡 还没有餐厅！</strong> 前往左侧的<b>📄 添加餐厅</b>，与我分享菜单即可开始。',
    'Malay': '<strong>💡 Tiada restoran lagi!</strong> Pergi ke <b>📄 Tambah Restoran</b> di sebelah kiri untuk berkongsi menu dan mulakan.',
    'Tamil': '<strong>💡 இன்னும் உணவகங்கள் இல்லை!</strong> இடதுபுறம் உள்ள <b>📄 உணவகம் சேர்க்கவும்</b> சென்று மெனுவைப் பகிர்ந்து தொடங்கவும்.',
}

HOME_FOOTER = {
    'English': 'Helping you eat well every day',
    'Simplified Chinese': '帮助您每天吃得好',
    'Malay': 'Membantu anda makan dengan baik setiap hari',
    'Tamil': 'ஒவ்வொரு நாளும் நன்றாக சாப்பிட உதவுகிறது',
}

# ─── Sidebar ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍜 GrabEats")
    st.markdown("### Senior Helper")
    st.markdown("---")

    selected_lang_label = st.selectbox(
        "🌐 Language / 语言",
        list(LANGUAGES.keys()),
        key="lang_select"
    )
    lang = LANGUAGES[selected_lang_label]

    st.markdown("---")
    st.markdown("**📌 Menu**")

    # Navigation buttons — use on_click callback for reliable state update
    for key in NAV_KEYS:
        is_active = st.session_state.active_page == key
        label = NAV_LABELS[lang][key]
        
        # Use callback to set active page before rerun
        def make_callback(k=key):
            def callback():
                st.session_state.active_page = k
            return callback
        
        st.button(
            label,
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
            on_click=make_callback(key)
        )

    st.markdown("---")
    n_restaurants = len(st.session_state.restaurants)
    n_history = len(st.session_state.chat_history)
    st.markdown(f"""
    <div class="sidebar-stats">
        <p>📊 Quick Stats</p>
        <p class="stat-line">🏢 {n_restaurants} Restaurants</p>
        <p class="stat-line">💬 {n_history} Searches</p>
    </div>
    """, unsafe_allow_html=True)

    if not chatbot:
        st.markdown("---")
        st.markdown("👋 **Your Food Assistant is resting.** Please ask for help to get it started!")

# ─── Active page ─────────────────────────────────────────────────────────────────
active = st.session_state.active_page
# ─── PAGE: HOME ───────────────────────────────────────────────────────────────────
if active == 'home':

    # Language-specific hero text
    hero_title = {
        'English': '🍜 GrabEats Senior Helper',
        'Simplified Chinese': '🍜 GrabEats 乐龄助手',
        'Malay': '🍜 GrabEats Pembantu Warga Emas',
        'Tamil': '🍜 GrabEats மூத்தோர் உதவியாளர்',
    }
    hero_subtitle = {
        'English': 'Your friendly food assistant — made especially for you!',
        'Simplified Chinese': '您的贴心美食助手 — 专为您打造！',
        'Malay': 'Pembantu makanan mesra anda — dibuat khas untuk anda!',
        'Tamil': 'உங்கள் நட்பு உணவு உதவியாளர் — உங்களுக்காகவே உருவாக்கப்பட்டது!',
    }
    
    st.markdown(f"""
    <div class="hero-banner">
        <h1>{hero_title.get(lang, hero_title['English'])}</h1>
        <p>{hero_subtitle.get(lang, hero_subtitle['English'])}</p>
    </div>
    """, unsafe_allow_html=True)

    # How can I help heading
    help_heading = {
        'English': '### ✨ How can I help you today?',
        'Simplified Chinese': '### ✨ 今天我能帮您什么？',
        'Malay': '### ✨ Bagaimana saya boleh bantu anda hari ini?',
        'Tamil': '### ✨ இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?',
    }
    st.markdown(help_heading.get(lang, help_heading['English']))
    
    c1, c2, c3, c4 = st.columns(4)
    features = HOME_FEATURES.get(lang, HOME_FEATURES['English'])
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="icon">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Steps heading
    steps_heading = {
        'English': '### 📖 Simple steps to use this app',
        'Simplified Chinese': '### 📖 使用此应用的简单步骤',
        'Malay': '### 📖 Langkah mudah untuk menggunakan aplikasi ini',
        'Tamil': '### 📖 இந்த பயன்பாட்டைப் பயன்படுத்த எளிய வழிமுறைகள்',
    }
    st.markdown(steps_heading.get(lang, steps_heading['English']))
    
    steps = HOME_STEPS.get(lang, HOME_STEPS['English'])
    for num, text_s in steps:
        st.markdown(f"""
        <div class="step-row">
            <span class="step-badge">{num}</span>
            <p>{text_s}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Saved restaurants heading
    saved_heading = {
        'English': '### 🏢 Your Saved Restaurants',
        'Simplified Chinese': '### 🏢 您保存的餐厅',
        'Malay': '### 🏢 Restoran Anda yang Disimpan',
        'Tamil': '### 🏢 உங்கள் சேமித்த உணவகங்கள்',
    }
    st.markdown(saved_heading.get(lang, saved_heading['English']))

    if st.session_state.restaurants:
        cols = st.columns(3)
        for i, (name, data) in enumerate(st.session_state.restaurants.items()):
            n_items = len(data.get('items', []))
            dish_label = {
                'English': f"dish{'es' if n_items != 1 else ''} saved",
                'Simplified Chinese': f"道菜已保存",
                'Malay': f"hidangan disimpan",
                'Tamil': f"உணவுகள் சேமிக்கப்பட்டன",
            }
            with cols[i % 3]:
                st.markdown(f"""
                <div class="restaurant-card">
                    <div class="r-name">🍽️ {name}</div>
                    <div class="r-loc">📍 {data['location']}</div>
                    <div class="r-items">🗒️ {n_items} {dish_label.get(lang, dish_label['English'])}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        no_rest = HOME_NO_RESTAURANTS.get(lang, HOME_NO_RESTAURANTS['English'])
        st.markdown(f"""
        <div class="tip-box">
            {no_rest}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    footer_text = HOME_FOOTER.get(lang, HOME_FOOTER['English'])
    made_with = {
        'English': 'Made with ❤️ for Singapore Seniors',
        'Simplified Chinese': '用❤️为新加坡乐龄人士打造',
        'Malay': 'Dibuat dengan ❤️ untuk Warga Emas Singapura',
        'Tamil': 'சிங்கப்பூர் மூத்தோருக்காக ❤️ உடன் உருவாக்கப்பட்டது',
    }
    st.markdown(f"""
    <div style='text-align:center; padding:22px; background:white; border-radius:18px;
                box-shadow:0 2px 12px rgba(0,0,0,0.06); color:#555; font-size:17px;
                border:1.5px solid #BBF0D0;'>
        🍜 <b style="color:#166534;">GrabEats Senior Helper</b> &nbsp;|&nbsp;
        {made_with.get(lang, made_with['English'])} &nbsp;|&nbsp;
        <span style="color:#2E9E5B; font-weight:700;">{footer_text}</span>
    </div>
    """, unsafe_allow_html=True)

# ─── PAGE: FOOD ASSISTANT ─────────────────────────────────────────────────────────
elif active == 'food_assistant':

    page_title = PAGE_TITLES[lang]['food_assistant']
    st.markdown(f"""
    <div class="page-header">
        <span class="ph-icon">🤖</span>
        <h2>{page_title}</h2>
    </div>
    """, unsafe_allow_html=True)

    tip_text = {
        'English': """<strong>💡 Tip:</strong> Just tell me what you feel like eating today — in your own words!
        For example: <em>"I'd like something soft and warm for lunch, maybe porridge"</em>""",
        'Simplified Chinese': """<strong>💡 提示：</strong>用您自己的话告诉我今天想吃什么！
        例如：<em>"我想吃软一点的午餐，也许是粥"</em>""",
        'Malay': """<strong>💡 Tip:</strong> Hanya beritahu saya apa yang anda rasa nak makan hari ini — dalam perkataan anda sendiri!
        Contohnya: <em>"Saya mahu sesuatu yang lembut dan hangat untuk makan tengah hari, mungkin bubur"</em>""",
        'Tamil': """<strong>💡 குறிப்பு:</strong> இன்று நீங்கள் என்ன சாப்பிட விரும்புகிறீர்கள் என்று உங்கள் சொந்த வார்த்தைகளில் சொல்லுங்கள்!
        உதாரணமாக: <em>"மதிய உணவுக்கு மென்மையான சூடான உணவு வேண்டும், ஒருவேளை கஞ்சி"</em>""",
    }
    st.markdown(f"""
    <div class="tip-box">
        {tip_text.get(lang, tip_text['English'])}
    </div>
    """, unsafe_allow_html=True)

    user_input_label = {
        'English': "💬 What would you like to eat today?",
        'Simplified Chinese': "💬 今天想吃什么？",
        'Malay': "💬 Apa yang anda ingin makan hari ini?",
        'Tamil': "💬 இன்று நீங்கள் என்ன சாப்பிட விரும்புகிறீர்கள்?",
    }
    user_input = st.text_area(
        user_input_label.get(lang, user_input_label['English']),
        placeholder=PLACEHOLDERS.get(lang, PLACEHOLDERS['English']),
        height=130,
        key="user_query"
    )

    col_d, col_b = st.columns([3, 2])

    with col_d:
        dietary_restrictions = st.multiselect(
            DIET_LBL.get(lang, DIET_LBL['English']),
            options=DIETARY_OPTIONS.get(lang, DIETARY_OPTIONS['English']),
            key="dietary"
        )

    with col_b:
        price_range = st.select_slider(
            BUDGET_LBL.get(lang, BUDGET_LBL['English']),
            options=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 30, 50],
            value=(5, 15),
            key="price_range"
        )
        st.markdown(f"""
        <div class="budget-display">💰 ${price_range[0]} – ${price_range[1]} SGD</div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    btn_label = SEARCH_BTN.get(lang, SEARCH_BTN['English'])

    if st.button(btn_label, use_container_width=True, key="search_btn"):
        warning_msg = {
            'English': "⚠️ Please tell me what you'd like to eat so I can help!",
            'Simplified Chinese': "⚠️ 请告诉我您想吃什么，我才能帮忙！",
            'Malay': "⚠️ Sila beritahu saya apa yang anda ingin makan supaya saya boleh bantu!",
            'Tamil': "⚠️ தயவுசெய்து நீங்கள் என்ன சாப்பிட விரும்புகிறீர்கள் என்று சொல்லுங்கள்!",
        }
        error_msg = {
            'English': "❌ The food assistant isn't ready to talk yet. Please ask for help with the setup.",
            'Simplified Chinese': "❌ 美食助手还没准备好。请寻求帮助完成设置。",
            'Malay': "❌ Pembantu makanan belum bersedia. Sila minta bantuan untuk persediaan.",
            'Tamil': "❌ உணவு உதவியாளர் இன்னும் தயாராக இல்லை. அமைப்பிற்கு உதவி கேட்கவும்.",
        }
        if not user_input.strip():
            st.warning(warning_msg.get(lang, warning_msg['English']))
        elif not chatbot:
            st.error(error_msg.get(lang, error_msg['English']))
        else:
            spinner_msg = {
                'English': "🍳 Looking through the menus for you... please wait a moment!",
                'Simplified Chinese': "🍳 正在为您查看菜单...请稍候！",
                'Malay': "🍳 Sedang melihat menu untuk anda... sila tunggu sebentar!",
                'Tamil': "🍳 உங்களுக்காக மெனுக்களைப் பார்க்கிறேன்... சிறிது காத்திருக்கவும்!",
            }
            with st.spinner(spinner_msg.get(lang, spinner_msg['English'])):
                try:
                    db_context = ""
                    if st.session_state.restaurants:
                        db_context = "Restaurants in our database:\n"
                        for name, data in st.session_state.restaurants.items():
                            items_str = ", ".join(data.get('items', []))
                            db_context += f"- {name} (Location: {data['location']}). Menu: {items_str}\n"

                    clean_restrictions = [r.split(' ')[0] for r in dietary_restrictions]

                    recommendation = chatbot.recommend_food(
                        user_input, lang, clean_restrictions, price_range, db_context
                    )

                    st.session_state.chat_history.append({
                        "user": user_input,
                        "bot": recommendation,
                        "restrictions": dietary_restrictions,
                        "budget": price_range
                    })
                    db.add_chat_history(user_input, recommendation)
                    
                except Exception as e:
                    error_str = str(e).lower()
                    if "quota" in error_str or "limit" in error_str:
                        friendly_msg = {
                            'English': "😅 Our AI helper is taking a short break. Please try again in a few minutes!",
                            'Simplified Chinese': "😅 我们的AI助手正在短暂休息。请几分钟后再试！",
                            'Malay': "😅 Pembantu AI kami sedang berehat sebentar. Sila cuba lagi dalam beberapa minit!",
                            'Tamil': "😅 எங்கள் AI உதவியாளர் சிறிது ஓய்வு எடுத்துக்கொள்கிறார். சில நிமிடங்களில் மீண்டும் முயற்சிக்கவும்!",
                        }
                        st.info(friendly_msg.get(lang, friendly_msg['English']))
                    elif "api" in error_str or "key" in error_str:
                        friendly_msg = {
                            'English': "🔧 The food assistant needs a quick check-up. Please ask your caregiver for help with the settings.",
                            'Simplified Chinese': "🔧 美食助手需要快速检查。请向您的看护人寻求设置帮助。",
                            'Malay': "🔧 Pembantu makanan memerlukan pemeriksaan pantas. Sila minta bantuan penjaga anda untuk tetapan.",
                            'Tamil': "🔧 உணவு உதவியாளருக்கு விரைவான பரிசோதனை தேவை. அமைப்புகளுக்கு உங்கள் பராமரிப்பாளரிடம் உதவி கேட்கவும்.",
                        }
                        st.warning(friendly_msg.get(lang, friendly_msg['English']))
                    else:
                        friendly_msg = {
                            'English': "🙏 Something unexpected happened. Please try again in a moment or ask for help.",
                            'Simplified Chinese': "🙏 发生了意外情况。请稍后再试或寻求帮助。",
                            'Malay': "🙏 Sesuatu yang tidak dijangka berlaku. Sila cuba sebentar lagi atau minta bantuan.",
                            'Tamil': "🙏 எதிர்பாராத ஏதோ நடந்துவிட்டது. சிறிது நேரத்தில் மீண்டும் முயற்சிக்கவும் அல்லது உதவி கேட்கவும்.",
                        }
                        st.warning(friendly_msg.get(lang, friendly_msg['English']))

    if st.session_state.chat_history:
        st.markdown("<br>", unsafe_allow_html=True)
        chat_title = {
            'English': "### 💬 Our Conversation",
            'Simplified Chinese': "### 💬 我们的对话",
            'Malay': "### 💬 Perbualan Kita",
            'Tamil': "### 💬 எங்கள் உரையாடல்",
        }
        st.markdown(chat_title.get(lang, chat_title['English']))

        you_asked = {
            'English': "You asked 👤",
            'Simplified Chinese': "您问 👤",
            'Malay': "Anda tanya 👤",
            'Tamil': "நீங்கள் கேட்டீர்கள் 👤",
        }
        i_suggested = {
            'English': "I suggested 🤖",
            'Simplified Chinese': "我建议 🤖",
            'Malay': "Saya cadangkan 🤖",
            'Tamil': "நான் பரிந்துரைத்தேன் 🤖",
        }
        for entry in reversed(st.session_state.chat_history):
            st.markdown(f"""
            <div class="chat-label user-label">{you_asked.get(lang, you_asked['English'])}</div>
            <div class="chat-bubble-user">{entry['user']}</div>
            <div class="chat-label">{i_suggested.get(lang, i_suggested['English'])}</div>
            <div class="chat-bubble-bot">{entry['bot']}</div>
            <hr>
            """, unsafe_allow_html=True)

# ─── PAGE: ADD RESTAURANT ─────────────────────────────────────────────────────────
elif active == 'add_restaurant':

    page_title = PAGE_TITLES[lang]['add_restaurant']
    st.markdown(f"""
    <div class="page-header">
        <span class="ph-icon">📄</span>
        <h2>{page_title}</h2>
    </div>
    """, unsafe_allow_html=True)

    tip_text = {
        'English': """<strong>💡 How it works:</strong> Type in the restaurant name and where it is,
        then share their menu file with me. I will remember all the dishes for you!""",
        'Simplified Chinese': """<strong>💡 如何使用：</strong>输入餐厅名称和位置，
        然后分享菜单文件给我。我会为您记住所有菜品！""",
        'Malay': """<strong>💡 Bagaimana ia berfungsi:</strong> Taipkan nama restoran dan lokasinya,
        kemudian kongsi fail menu dengan saya. Saya akan ingat semua hidangan untuk anda!""",
        'Tamil': """<strong>💡 இது எப்படி வேலை செய்கிறது:</strong> உணவகத்தின் பெயரையும் இருப்பிடத்தையும் உள்ளிடவும்,
        பின்னர் மெனு கோப்பை என்னுடன் பகிருங்கள். அனைத்து உணவுகளையும் உங்களுக்காக நினைவில் கொள்கிறேன்!""",
    }
    st.markdown(f"""
    <div class="tip-box">
        {tip_text.get(lang, tip_text['English'])}
    </div>
    """, unsafe_allow_html=True)

    step1_title = {
        'English': "### 1️⃣ Restaurant Details",
        'Simplified Chinese': "### 1️⃣ 餐厅详情",
        'Malay': "### 1️⃣ Butiran Restoran",
        'Tamil': "### 1️⃣ உணவக விவரங்கள்",
    }
    st.markdown(step1_title.get(lang, step1_title['English']))
    col1, col2 = st.columns(2)
    
    name_placeholder = {
        'English': "e.g. Hai Kee Porridge",
        'Simplified Chinese': "例如：海记粥品",
        'Malay': "cth: Hai Kee Porridge",
        'Tamil': "எ.கா: ஹாய் கீ கஞ்சி",
    }
    loc_placeholder = {
        'English': "e.g. Toa Payoh Lor 8, #01-12",
        'Simplified Chinese': "例如：大巴窑8巷 #01-12",
        'Malay': "cth: Toa Payoh Lor 8, #01-12",
        'Tamil': "எ.கா: தோ பாயோ லோர் 8, #01-12",
    }
    name_label = {
        'English': "🏢 Restaurant Name",
        'Simplified Chinese': "🏢 餐厅名称",
        'Malay': "🏢 Nama Restoran",
        'Tamil': "🏢 உணவகத்தின் பெயர்",
    }
    loc_label = {
        'English': "📍 Where is it?",
        'Simplified Chinese': "📍 在哪里？",
        'Malay': "📍 Di mana?",
        'Tamil': "📍 எங்கே உள்ளது?",
    }
    
    with col1:
        restaurant_name = st.text_input(
            name_label.get(lang, name_label['English']),
            placeholder=name_placeholder.get(lang, name_placeholder['English'])
        )
    with col2:
        restaurant_location = st.text_input(
            loc_label.get(lang, loc_label['English']),
            placeholder=loc_placeholder.get(lang, loc_placeholder['English'])
        )

    st.markdown("<br>", unsafe_allow_html=True)
    step2_title = {
        'English': "### 2️⃣ Share Menu File",
        'Simplified Chinese': "### 2️⃣ 分享菜单文件",
        'Malay': "### 2️⃣ Kongsi Fail Menu",
        'Tamil': "### 2️⃣ மெனு கோப்பைப் பகிரவும்",
    }
    st.markdown(step2_title.get(lang, step2_title['English']))

    uploader_label = {
        'English': "📎 Place the menu file here",
        'Simplified Chinese': "📎 将菜单文件放在这里",
        'Malay': "📎 Letakkan fail menu di sini",
        'Tamil': "📎 மெனு கோப்பை இங்கே வைக்கவும்",
    }
    uploaded_file = st.file_uploader(
        uploader_label.get(lang, uploader_label['English']),
        type=['pdf'],
        key="menu_upload"
    )

    if uploaded_file:
        got_it = {
            'English': f"✅ <b>Got it!</b> I'm ready to learn the menu for: {uploaded_file.name}",
            'Simplified Chinese': f"✅ <b>收到！</b> 我已准备好学习：{uploaded_file.name} 的菜单",
            'Malay': f"✅ <b>Faham!</b> Saya sedia untuk mempelajari menu: {uploaded_file.name}",
            'Tamil': f"✅ <b>புரிந்தது!</b> மெனுவைக் கற்க தயாராக உள்ளேன்: {uploaded_file.name}",
        }
        st.markdown(f"""
        <div style='background:#F0FFF4; border:2px solid #28a745; border-radius:12px;
                    padding:14px 20px; font-size:18px; color:#1a5e2a; margin:10px 0;'>
            {got_it.get(lang, got_it['English'])}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    upload_btn_label = {
        'English': "📤  Remember this restaurant",
        'Simplified Chinese': "📤  记住这个餐厅",
        'Malay': "📤  Ingat restoran ini",
        'Tamil': "📤  இந்த உணவகத்தை நினைவில் கொள்",
    }
    if st.button(upload_btn_label.get(lang, upload_btn_label['English']), use_container_width=True, key="upload_btn"):
        name_warn = {
            'English': "⚠️ Please tell me the restaurant's name!",
            'Simplified Chinese': "⚠️ 请告诉我餐厅名称！",
            'Malay': "⚠️ Sila beritahu nama restoran!",
            'Tamil': "⚠️ உணவகத்தின் பெயரைச் சொல்லுங்கள்!",
        }
        file_warn = {
            'English': "⚠️ Please share a menu file with me first!",
            'Simplified Chinese': "⚠️ 请先分享菜单文件！",
            'Malay': "⚠️ Sila kongsi fail menu dahulu!",
            'Tamil': "⚠️ முதலில் மெனு கோப்பைப் பகிரவும்!",
        }
        if not restaurant_name.strip():
            st.warning(name_warn.get(lang, name_warn['English']))
        elif not uploaded_file:
            st.warning(file_warn.get(lang, file_warn['English']))
        else:
            spinner_msg = {
                'English': "📖 Learning the dishes from the menu... this may take a moment!",
                'Simplified Chinese': "📖 正在学习菜单中的菜品...可能需要一点时间！",
                'Malay': "📖 Sedang mempelajari hidangan dari menu... ini mungkin mengambil masa!",
                'Tamil': "📖 மெனுவிலிருந்து உணவுகளைக் கற்கிறேன்... சிறிது நேரம் ஆகலாம்!",
            }
            with st.spinner(spinner_msg.get(lang, spinner_msg['English'])):
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                menu_items = extract_menu_items(temp_path)

                success = db.add_restaurant(restaurant_name.strip(), restaurant_location.strip())

                if success:
                    restaurants = db.get_restaurants()
                    res_id = next((r[0] for r in restaurants if r[1] == restaurant_name.strip()), None)
                    if res_id:
                        menu_id = db.add_menu(res_id, "Main Menu")
                        for item in menu_items:
                            if item.strip():
                                db.add_dish(menu_id, item.strip(), 0.0)

                st.session_state.restaurants[restaurant_name.strip()] = {
                    'location': restaurant_location.strip(),
                    'items': [i for i in menu_items if i.strip()]
                }
                st.session_state.restaurants_loaded = False

                if os.path.exists(temp_path):
                    os.remove(temp_path)

                filtered = [i for i in menu_items if i.strip()]
                success_msg = {
                    'English': f"🎉 **{restaurant_name}** has been saved! I remembered **{len(filtered)} dishes** for you.",
                    'Simplified Chinese': f"🎉 **{restaurant_name}** 已保存！我为您记住了 **{len(filtered)} 道菜**。",
                    'Malay': f"🎉 **{restaurant_name}** telah disimpan! Saya ingat **{len(filtered)} hidangan** untuk anda.",
                    'Tamil': f"🎉 **{restaurant_name}** சேமிக்கப்பட்டது! உங்களுக்காக **{len(filtered)} உணவுகளை** நினைவில் வைத்துள்ளேன்.",
                }
                st.success(success_msg.get(lang, success_msg['English']))

                if filtered:
                    expander_title = {
                        'English': f"👀 Take a look at the {len(filtered)} dishes I found",
                        'Simplified Chinese': f"👀 看看我找到的 {len(filtered)} 道菜",
                        'Malay': f"👀 Lihat {len(filtered)} hidangan yang saya jumpa",
                        'Tamil': f"👀 நான் கண்டறிந்த {len(filtered)} உணவுகளைப் பாருங்கள்",
                    }
                    many_more = {
                        'English': "... and many more dishes.",
                        'Simplified Chinese': "... 还有更多菜品。",
                        'Malay': "... dan banyak lagi hidangan.",
                        'Tamil': "... மேலும் பல உணவுகள்.",
                    }
                    with st.expander(expander_title.get(lang, expander_title['English'])):
                        cols = st.columns(2)
                        for j, item in enumerate(filtered[:40]):
                            with cols[j % 2]:
                                st.markdown(f'<div class="badge">🍴 {item}</div>', unsafe_allow_html=True)
                        if len(filtered) > 40:
                            st.info(many_more.get(lang, many_more['English']))

# ─── PAGE: HISTORY & RESTAURANTS ─────────────────────────────────────────────────
elif active == 'history':

    page_title = PAGE_TITLES[lang]['history']
    st.markdown(f"""
    <div class="page-header">
        <span class="ph-icon">📋</span>
        <h2>{page_title}</h2>
    </div>
    """, unsafe_allow_html=True)

    tab_labels = {
        'English': ["🕒  Our Past Chats", "🏢  Saved Restaurants"],
        'Simplified Chinese': ["🕒  过去的对话", "🏢  已保存的餐厅"],
        'Malay': ["🕒  Perbualan Lepas", "🏢  Restoran Disimpan"],
        'Tamil': ["🕒  எங்கள் பழைய உரையாடல்கள்", "🏢  சேமித்த உணவகங்கள்"],
    }
    tab1, tab2 = st.tabs(tab_labels.get(lang, tab_labels['English']))

    with tab1:
        if st.session_state.chat_history:
            chats_count = {
                'English': f"We have talked about food **{len(st.session_state.chat_history)}** times.",
                'Simplified Chinese': f"我们已经讨论了 **{len(st.session_state.chat_history)}** 次食物。",
                'Malay': f"Kita telah berbual tentang makanan **{len(st.session_state.chat_history)}** kali.",
                'Tamil': f"நாங்கள் **{len(st.session_state.chat_history)}** முறை உணவைப் பற்றி பேசியுள்ளோம்.",
            }
            st.markdown(chats_count.get(lang, chats_count['English']))
            st.markdown("<br>", unsafe_allow_html=True)

            for i, entry in enumerate(reversed(st.session_state.chat_history), 1):
                preview = entry['user'][:60] + "..." if len(entry['user']) > 60 else entry['user']
                budget  = entry.get('budget', (0, 0))

                conv_title = {
                    'English': f"🔍 Conversation #{len(st.session_state.chat_history) - i + 1}: {preview}",
                    'Simplified Chinese': f"🔍 对话 #{len(st.session_state.chat_history) - i + 1}: {preview}",
                    'Malay': f"🔍 Perbualan #{len(st.session_state.chat_history) - i + 1}: {preview}",
                    'Tamil': f"🔍 உரையாடல் #{len(st.session_state.chat_history) - i + 1}: {preview}",
                }
                foods_avoid = {
                    'English': "<b>Foods to avoid:</b>",
                    'Simplified Chinese': "<b>避免的食物：</b>",
                    'Malay': "<b>Makanan untuk dielakkan:</b>",
                    'Tamil': "<b>தவிர்க்க வேண்டிய உணவுகள்:</b>",
                }
                your_budget = {
                    'English': "<b>Your budget:</b>",
                    'Simplified Chinese': "<b>您的预算：</b>",
                    'Malay': "<b>Belanjawan anda:</b>",
                    'Tamil': "<b>உங்கள் பட்ஜெட்:</b>",
                }

                with st.expander(conv_title.get(lang, conv_title['English'])):
                    if entry.get('restrictions'):
                        rlist = "  ".join([f"<span class='badge'>{r}</span>" for r in entry['restrictions']])
                        st.markdown(f"<p style='color:#333;'>{foods_avoid.get(lang, foods_avoid['English'])} {rlist}</p>", unsafe_allow_html=True)
                    if budget[0]:
                        st.markdown(f"<p style='color:#333;'>{your_budget.get(lang, your_budget['English'])} ${budget[0]} – ${budget[1]} SGD</p>", unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown(entry['bot'])
        else:
            no_chats = {
                'English': """<strong>💡 We haven't talked yet!</strong><br>
                Go to <b>🤖 Food Assistant</b> and tell me what you'd like to eat. Our chat will show up here.""",
                'Simplified Chinese': """<strong>💡 我们还没聊过！</strong><br>
                前往<b>🤖 美食助手</b>，告诉我您想吃什么。我们的对话将显示在这里。""",
                'Malay': """<strong>💡 Kita belum berbual lagi!</strong><br>
                Pergi ke <b>🤖 Pembantu Makanan</b> dan beritahu saya apa yang anda ingin makan. Perbualan kita akan dipaparkan di sini.""",
                'Tamil': """<strong>💡 நாங்கள் இன்னும் பேசவில்லை!</strong><br>
                <b>🤖 உணவு உதவியாளர்</b> சென்று நீங்கள் என்ன சாப்பிட விரும்புகிறீர்கள் என்று சொல்லுங்கள். எங்கள் உரையாடல் இங்கே காண்பிக்கப்படும்.""",
            }
            st.markdown(f"""
            <div class="tip-box">
                {no_chats.get(lang, no_chats['English'])}
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        if st.session_state.restaurants:
            saved_count = {
                'English': f"I have remembered **{len(st.session_state.restaurants)}** restaurant(s) for you.",
                'Simplified Chinese': f"我为您记住了 **{len(st.session_state.restaurants)}** 家餐厅。",
                'Malay': f"Saya telah mengingati **{len(st.session_state.restaurants)}** restoran untuk anda.",
                'Tamil': f"உங்களுக்காக **{len(st.session_state.restaurants)}** உணவகங்களை நினைவில் வைத்துள்ளேன்.",
            }
            st.markdown(saved_count.get(lang, saved_count['English']))
            st.markdown("<br>", unsafe_allow_html=True)

            where_is = {
                'English': "Where it is:",
                'Simplified Chinese': "在哪里：",
                'Malay': "Di mana:",
                'Tamil': "எங்கே உள்ளது:",
            }
            not_specified = {
                'English': "Not specified",
                'Simplified Chinese': "未指定",
                'Malay': "Tidak dinyatakan",
                'Tamil': "குறிப்பிடப்படவில்லை",
            }
            dishes_saved = {
                'English': "dishes saved",
                'Simplified Chinese': "道菜已保存",
                'Malay': "hidangan disimpan",
                'Tamil': "உணவுகள் சேமிக்கப்பட்டன",
            }
            view_all = {
                'English': "📋 View all",
                'Simplified Chinese': "📋 查看全部",
                'Malay': "📋 Lihat semua",
                'Tamil': "📋 அனைத்தையும் காண்க",
            }
            dishes_for = {
                'English': "dishes for",
                'Simplified Chinese': "道菜 -",
                'Malay': "hidangan untuk",
                'Tamil': "உணவுகள் -",
            }

            for name, data in st.session_state.restaurants.items():
                items = data.get('items', [])
                loc = data['location'] or not_specified.get(lang, not_specified['English'])

                st.markdown(f"""
                <div class="senior-card">
                    <h3>🍽️ {name}</h3>
                    <p>📍 <b>{where_is.get(lang, where_is['English'])}</b> {loc}</p>
                    <p>🗒️ <b>{len(items)} {dishes_saved.get(lang, dishes_saved['English'])}</b></p>
                </div>
                """, unsafe_allow_html=True)

                if items:
                    with st.expander(f"{view_all.get(lang, view_all['English'])} {len(items)} {dishes_for.get(lang, dishes_for['English'])} {name}"):
                        cols = st.columns(2)
                        for j, item in enumerate(items):
                            with cols[j % 2]:
                                st.markdown(f'<div class="badge">🍴 {item}</div>', unsafe_allow_html=True)
        else:
            no_restaurants = {
                'English': """<strong>💡 No restaurants remembered yet!</strong><br>
                Go to <b>📄 Add Restaurant</b> to share a menu file and I'll save a restaurant for you.""",
                'Simplified Chinese': """<strong>💡 还没有记住任何餐厅！</strong><br>
                前往<b>📄 添加餐厅</b>分享菜单文件，我会为您保存餐厅。""",
                'Malay': """<strong>💡 Tiada restoran diingati lagi!</strong><br>
                Pergi ke <b>📄 Tambah Restoran</b> untuk berkongsi fail menu dan saya akan simpan restoran untuk anda.""",
                'Tamil': """<strong>💡 இன்னும் உணவகங்கள் நினைவில் இல்லை!</strong><br>
                <b>📄 உணவகம் சேர்க்கவும்</b> சென்று மெனு கோப்பைப் பகிரவும், உங்களுக்காக உணவகத்தைச் சேமிப்பேன்.""",
            }
            st.markdown(f"""
            <div class="tip-box">
                {no_restaurants.get(lang, no_restaurants['English'])}
            </div>
            """, unsafe_allow_html=True)