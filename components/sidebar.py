import streamlit as st
from config.languages import LANGUAGES, NAV_KEYS, NAV_LABELS

def render_sidebar(db, chatbot):
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

        for key in NAV_KEYS:
            is_active = st.session_state.active_page == key
            label = NAV_LABELS[lang][key]
            
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

    return lang, st.session_state.active_page