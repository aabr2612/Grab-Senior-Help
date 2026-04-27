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
   SIDEBAR — fully rebuilt for reliability
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

/* Sidebar radio buttons */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255,255,255,0.13) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin-bottom: 6px !important;
    display: flex !important;
    align-items: center !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    color: white !important;
    cursor: pointer;
    transition: background 0.2s;
    border: 1.5px solid rgba(255,255,255,0.15);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,0.26) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
[data-testid="stSidebar"] [data-testid="stRadio"] input:checked + div {
    background: rgba(255,255,255,0.28) !important;
    border-color: rgba(255,255,255,0.5) !important;
}
/* Hide default radio circle */
[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] { display: none; }
[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] { display: none !important; }

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
}

/* ── Divider ── */
hr { border-color: #A7D7B8 !important; margin: 1.5rem 0 !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #2E9E5B !important; }

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
    border: 1.5px solid #BBF0D0;          /* ← visible green-tinted edge */
    border-top: 4px solid #2E9E5B;        /* ← stronger top accent */
    text-align: center;
    height: 100%;
    margin-bottom: 16px;                   /* ← gap on small screens */
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
    border: 1.5px solid #BBF0D0;           /* ← visible green edge */
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
    color: #1a1a1a !important;             /* ← FIXED: always dark on white */
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
    border: 1.5px solid #BBF0D0;           /* ← green-tinted edge */
    border-top: 5px solid #2E9E5B;
    height: 100%;
    margin-bottom: 16px;                   /* ← gap between cards */
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
    color: #2E9E5B !important;             /* ← FIXED: green, not invisible */
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
    color: #333 !important;               /* ← FIXED: always visible */
    margin: 6px 0;
}

/* ════════════════════════════════════════
   BADGE
   ════════════════════════════════════════ */
.badge {
    display: inline-block;
    background: #F0FDF4;
    color: #166534 !important;            /* ← FIXED: dark green on light */
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
.chat-bubble-bot {
    background: white;
    color: #1a1a1a !important;
    border-radius: 18px 18px 18px 4px;
    padding: clamp(14px, 2vw, 20px) clamp(16px, 2vw, 24px);
    margin: 10px clamp(20px, 8vw, 60px) 10px 0;
    font-size: clamp(15px, 1.6vw, 20px) !important;
    line-height: 1.7;
    box-shadow: 0 3px 12px rgba(0,0,0,0.09);
    border-left: 5px solid #2E9E5B;
    border: 1.5px solid #BBF0D0;
    border-left: 5px solid #2E9E5B;
}
.chat-label {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
    color: #aaa !important;
}
.chat-label.user-label { text-align: right; color: #2E9E5B !important; }

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
    color: #1a4a2e !important;             /* ← always dark */
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
</style>
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

# ─── Language Config ─────────────────────────────────────────────────────────────
LANGUAGES = {
    '🇬🇧  English': 'English',
    '🇨🇳  中文 (Chinese)': 'Simplified Chinese',
    '🇲🇾  Bahasa Melayu': 'Malay',
    '🇮🇳  தமிழ் (Tamil)': 'Tamil'
}

NAV_PAGES = {
    'English':            ['🏠  Home', '🤖  Food Assistant', '📄  Add Restaurant', '📋  History & Restaurants'],
    'Simplified Chinese': ['🏠  首页', '🤖  美食助手', '📄  添加餐厅', '📋  历史与餐厅'],
    'Malay':              ['🏠  Laman Utama', '🤖  Pembantu Makanan', '📄  Tambah Restoran', '📋  Sejarah & Restoran'],
    'Tamil':              ['🏠  முகப்பு', '🤖  உணவு உதவியாளர்', '📄  உணவகம் சேர்க்கவும்', '📋  வரலாறு & உணவகங்கள்'],
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

    pages = NAV_PAGES[lang]
    page = st.radio("", pages, key="nav", label_visibility="collapsed")

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

# ─── PAGE: HOME ───────────────────────────────────────────────────────────────────
if page == pages[0]:

    st.markdown("""
    <div class="hero-banner">
        <h1>🍜 GrabEats Senior Helper</h1>
        <p>Your friendly food assistant — made especially for you!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✨ How can I help you today?")
    c1, c2, c3, c4 = st.columns(4)
    features = [
        ("🤖", "Talk to me", "Tell me what you'd like to eat and I'll find the best dishes for you."),
        ("📄", "Add a Menu", "Share a restaurant's menu with me and I'll remember all the dishes."),
        ("💰", "Save Money", "Tell me your budget and I'll only show you what fits your wallet."),
        ("🛡️", "Eat Safely", "Tell me what you can't eat and I'll make sure you stay safe and healthy."),
    ]
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

    st.markdown("### 📖 Simple steps to use this app")
    steps = [
        ("1", "Pick your favorite language on the left side."),
        ("2", "Go to <b>🤖 Food Assistant</b> and tell me what you feel like eating."),
        ("3", "Let me know if there are foods you need to avoid (like pork or seafood)."),
        ("4", "Set your price range and press the big green button!"),
        ("5", "Look at my suggestions and enjoy a wonderful meal! 😊"),
    ]
    for num, text_s in steps:
        st.markdown(f"""
        <div class="step-row">
            <span class="step-badge">{num}</span>
            <p>{text_s}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏢 Your Saved Restaurants")

    if st.session_state.restaurants:
        cols = st.columns(3)
        for i, (name, data) in enumerate(st.session_state.restaurants.items()):
            n_items = len(data.get('items', []))
            with cols[i % 3]:
                st.markdown(f"""
                <div class="restaurant-card">
                    <div class="r-name">🍽️ {name}</div>
                    <div class="r-loc">📍 {data['location']}</div>
                    <div class="r-items">🗒️ {n_items} dish{'es' if n_items != 1 else ''} saved</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="tip-box">
            <strong>💡 No restaurants yet!</strong> Go to <b>📄 Add Restaurant</b> on the left to share a menu with me and get started.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; padding:22px; background:white; border-radius:18px;
                box-shadow:0 2px 12px rgba(0,0,0,0.06); color:#555; font-size:17px;
                border:1.5px solid #BBF0D0;'>
        🍜 <b style="color:#166534;">GrabEats Senior Helper</b> &nbsp;|&nbsp;
        Made with ❤️ for Singapore Seniors &nbsp;|&nbsp;
        <span style="color:#2E9E5B; font-weight:700;">Helping you eat well every day</span>
    </div>
    """, unsafe_allow_html=True)

# ─── PAGE: FOOD ASSISTANT ─────────────────────────────────────────────────────────
elif page == pages[1]:

    st.markdown(f"""
    <div class="page-header">
        <span class="ph-icon">🤖</span>
        <h2>Food Assistant</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tip-box">
        <strong>💡 Tip:</strong> Just tell me what you feel like eating today — in your own words!
        For example: <em>"I'd like something soft and warm for lunch, maybe porridge"</em>
    </div>
    """, unsafe_allow_html=True)

    user_input = st.text_area(
        "💬 What would you like to eat today?",
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
        if not user_input.strip():
            st.warning("⚠️ Please tell me what you'd like to eat so I can help!")
        elif not chatbot:
            st.error("❌ The food assistant isn't ready to talk yet. Please ask for help with the setup.")
        else:
            with st.spinner("🍳 Looking through the menus for you... please wait a moment!"):
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

    if st.session_state.chat_history:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💬 Our Conversation")

        for entry in reversed(st.session_state.chat_history):
            st.markdown(f"""
            <div class="chat-label user-label">You asked 👤</div>
            <div class="chat-bubble-user">{entry['user']}</div>
            <div class="chat-label">I suggested 🤖</div>
            <div class="chat-bubble-bot">{entry['bot']}</div>
            <hr>
            """, unsafe_allow_html=True)

# ─── PAGE: ADD RESTAURANT ─────────────────────────────────────────────────────────
elif page == pages[2]:

    st.markdown(f"""
    <div class="page-header">
        <span class="ph-icon">📄</span>
        <h2>Add a Restaurant</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tip-box">
        <strong>💡 How it works:</strong> Type in the restaurant name and where it is,
        then share their menu file with me. I will remember all the dishes for you!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 1️⃣ Restaurant Details")
    col1, col2 = st.columns(2)
    with col1:
        restaurant_name = st.text_input("🏢 Restaurant Name", placeholder="e.g. Hai Kee Porridge")
    with col2:
        restaurant_location = st.text_input("📍 Where is it?", placeholder="e.g. Toa Payoh Lor 8, #01-12")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 2️⃣ Share Menu File")

    uploaded_file = st.file_uploader(
        "📎 Place the menu file here",
        type=['pdf'],
        key="menu_upload"
    )

    if uploaded_file:
        st.markdown(f"""
        <div style='background:#F0FFF4; border:2px solid #28a745; border-radius:12px;
                    padding:14px 20px; font-size:18px; color:#1a5e2a; margin:10px 0;'>
            ✅ <b>Got it!</b> I'm ready to learn the menu for: {uploaded_file.name}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📤  Remember this restaurant", use_container_width=True, key="upload_btn"):
        if not restaurant_name.strip():
            st.warning("⚠️ Please tell me the restaurant's name!")
        elif not uploaded_file:
            st.warning("⚠️ Please share a menu file with me first!")
        else:
            with st.spinner("📖 Learning the dishes from the menu... this may take a moment!"):
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
                st.success(f"🎉 **{restaurant_name}** has been saved! I remembered **{len(filtered)} dishes** for you.")

                if filtered:
                    with st.expander(f"👀 Take a look at the {len(filtered)} dishes I found"):
                        cols = st.columns(2)
                        for j, item in enumerate(filtered[:40]):
                            with cols[j % 2]:
                                st.markdown(f'<div class="badge">🍴 {item}</div>', unsafe_allow_html=True)
                        if len(filtered) > 40:
                            st.info(f"... and many more dishes.")

# ─── PAGE: HISTORY & RESTAURANTS ─────────────────────────────────────────────────
elif page == pages[3]:

    st.markdown(f"""
    <div class="page-header">
        <span class="ph-icon">📋</span>
        <h2>History & Restaurants</h2>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🕒  Our Past Chats", "🏢  Saved Restaurants"])

    with tab1:
        if st.session_state.chat_history:
            st.markdown(f"We have talked about food **{len(st.session_state.chat_history)}** times.")
            st.markdown("<br>", unsafe_allow_html=True)

            for i, entry in enumerate(reversed(st.session_state.chat_history), 1):
                preview = entry['user'][:60] + "..." if len(entry['user']) > 60 else entry['user']
                budget  = entry.get('budget', (0, 0))

                with st.expander(f"🔍 Conversation #{len(st.session_state.chat_history) - i + 1}: {preview}"):
                    if entry.get('restrictions'):
                        rlist = "  ".join([f"<span class='badge'>{r}</span>" for r in entry['restrictions']])
                        st.markdown(f"<p style='color:#333;'><b>Foods to avoid:</b> {rlist}</p>", unsafe_allow_html=True)
                    if budget[0]:
                        st.markdown(f"<p style='color:#333;'><b>Your budget:</b> ${budget[0]} – ${budget[1]} SGD</p>", unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown(entry['bot'])
        else:
            st.markdown("""
            <div class="tip-box">
                <strong>💡 We haven't talked yet!</strong><br>
                Go to <b>🤖 Food Assistant</b> and tell me what you'd like to eat. Our chat will show up here.
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        if st.session_state.restaurants:
            st.markdown(f"I have remembered **{len(st.session_state.restaurants)}** restaurant(s) for you.")
            st.markdown("<br>", unsafe_allow_html=True)

            for name, data in st.session_state.restaurants.items():
                items = data.get('items', [])

                st.markdown(f"""
                <div class="senior-card">
                    <h3>🍽️ {name}</h3>
                    <p>📍 <b>Where it is:</b> {data['location'] or 'Not specified'}</p>
                    <p>🗒️ <b>{len(items)} dishes</b> saved</p>
                </div>
                """, unsafe_allow_html=True)

                if items:
                    with st.expander(f"📋 View all {len(items)} dishes for {name}"):
                        cols = st.columns(2)
                        for j, item in enumerate(items):
                            with cols[j % 2]:
                                st.markdown(f'<div class="badge">🍴 {item}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="tip-box">
                <strong>💡 No restaurants remembered yet!</strong><br>
                Go to <b>📄 Add Restaurant</b> to share a menu file and I'll save a restaurant for you.
            </div>
            """, unsafe_allow_html=True)