import streamlit as st

def init_page_config():
    st.set_page_config(
        page_title="GrabEats Senior Helper",
        page_icon="🍜",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_css():
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

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.3) !important;
        margin: 10px 0 !important;
    }

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

    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #2E9E5B !important;
        background: #E0FBE8 !important;
    }
    [data-testid="stFileUploadDropzone"]:focus-within {
        border-color: #2E9E5B !important;
        box-shadow: 0 0 0 3px rgba(46,158,91,0.15) !important;
    }

    [data-baseweb="select"]:hover {
        border-color: #2E9E5B !important;
    }

    .stButton > button:focus {
        outline: 2px solid #2E9E5B !important;
        outline-offset: 2px !important;
    }
    .stButton > button:focus:not(:active) {
        outline: 2px solid #2E9E5B !important;
        outline-offset: 2px !important;
    }

    [data-baseweb="slider"]:hover [role="slider"] {
        background-color: #2E9E5B !important;
    }
    [data-baseweb="slider"] [role="slider"]:focus {
        box-shadow: 0 0 0 3px rgba(46,158,91,0.3) !important;
        background-color: #2E9E5B !important;
    }

    [data-baseweb="tag"] {
        background-color: #2E9E5B !important;
        border-radius: 8px !important;
        font-size: 16px !important;
    }
    [data-baseweb="tag"] span { color: white !important; }

    .stAlert { font-size: 18px !important; border-radius: 14px !important; }

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
    details .badge {
        color: #166534 !important;
    }
    details p { color: #1a1a1a !important; }
    details span { color: #1a1a1a !important; }
    details div { color: #1a1a1a !important; }

    hr { border-color: #A7D7B8 !important; margin: 1.5rem 0 !important; }

    .stSpinner > div { border-top-color: #2E9E5B !important; }
    .stSpinner { color: #1a1a1a !important; }
    .stSpinner p, .stSpinner span, .stSpinner div { color: #1a1a1a !important; }

    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #2E9E5B !important;
        border-radius: 16px !important;
        background: #F0FDF4 !important;
        font-size: 18px !important;
        padding: 24px !important;
    }

    /* ═══ HERO BANNER ═══ */
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
    .chat-bubble-user p, .chat-bubble-user span, .chat-bubble-user div,
    .chat-bubble-user li, .chat-bubble-user h1, .chat-bubble-user h2,
    .chat-bubble-user h3, .chat-bubble-user h4, .chat-bubble-user strong,
    .chat-bubble-user em { color: white !important; }

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
    .chat-bubble-bot p, .chat-bubble-bot span, .chat-bubble-bot div,
    .chat-bubble-bot li, .chat-bubble-bot h1, .chat-bubble-bot h2,
    .chat-bubble-bot h3, .chat-bubble-bot h4, .chat-bubble-bot strong,
    .chat-bubble-bot em { color: #1a1a1a !important; }

    .chat-label {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 4px;
        color: #888 !important;
    }
    .chat-label p, .chat-label span, .chat-label div { color: #888 !important; }
    .chat-label.user-label { text-align: right; color: #2E9E5B !important; }
    .chat-label.user-label p, .chat-label.user-label span, .chat-label.user-label div { color: #2E9E5B !important; }

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

    @media (max-width: 768px) {
        .hero-banner { padding: 20px 18px; border-radius: 16px; }
        .feature-card { margin-bottom: 12px; }
        .restaurant-card { margin-bottom: 12px; }
        .step-row { padding: 12px 14px; }
        .step-badge { width: 34px; height: 34px; min-width: 34px; font-size: 17px; margin-right: 10px; }
        .chat-bubble-user { margin-left: 12px; }
        .chat-bubble-bot { margin-right: 12px; }
    }

    footer { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    .viewerBadge_container__1QSob { display: none !important; }

    details summary { color: #166534 !important; }
    details summary p, details summary span, details summary div { color: #166534 !important; }
    details summary:hover { background-color: #E0FBE8 !important; color: #166534 !important; }
    details summary:focus { outline-color: #2E9E5B !important; background-color: #D0F8DC !important; color: #166534 !important; }
    details[open] summary { background-color: #D0F8DC !important; border-bottom: 2px solid #2E9E5B !important; color: #166534 !important; }

    .stAlert { color: #1a1a1a !important; }
    .stAlert p, .stAlert span, .stAlert div, .stAlert strong, .stAlert b { color: #1a1a1a !important; }
    .stAlert [data-testid="stSuccess"] p, .stAlert [data-testid="stSuccess"] span { color: #1a1a1a !important; }
    .stAlert [data-testid="stInfo"] p, .stAlert [data-testid="stInfo"] span { color: #1a1a1a !important; }
    .stAlert [data-testid="stWarning"] p, .stAlert [data-testid="stWarning"] span { color: #1a1a1a !important; }
    .streamlit-expanderContent .stMarkdown p { color: #1a1a1a !important; }
    .streamlit-expanderContent .stMarkdown span { color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

def inject_mobile_script():
    st.markdown("""
    <script>
    const mediaQuery = window.matchMedia('(max-width: 768px)');
    function handleMobileSidebar() {
        if (mediaQuery.matches) {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                const buttons = sidebar.querySelectorAll('button');
                buttons.forEach(button => {
                    button.addEventListener('click', function() {
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
    handleMobileSidebar();
    window.addEventListener('resize', handleMobileSidebar);
    </script>
    """, unsafe_allow_html=True)

def init_session_state(db):
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
        try:
            db_chats = db.get_chat_history()
            if db_chats:
                for chat in db_chats:
                    user_msg = chat[0] if len(chat) > 0 else ""
                    bot_msg = chat[1] if len(chat) > 1 else ""
                    if user_msg.strip() and bot_msg.strip(): 
                        st.session_state.chat_history.append({
                            "user": user_msg,
                            "bot": bot_msg,
                            "restrictions": [],
                            "budget": (0, 0)
                        })
        except Exception as e:
            print(f"Error loading chat history: {e}")

    if 'active_page' not in st.session_state:
        st.session_state.active_page = 'home'