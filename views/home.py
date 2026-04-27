import streamlit as st
from config.languages import HOME_FEATURES, HOME_STEPS, HOME_NO_RESTAURANTS, HOME_FOOTER

def render_home(lang):
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
                'Simplified Chinese': "道菜已保存",
                'Malay': "hidangan disimpan",
                'Tamil': "உணவுகள் சேமிக்கப்பட்டன",
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