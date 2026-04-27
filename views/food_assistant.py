import streamlit as st
from config.languages import PLACEHOLDERS, DIETARY_OPTIONS, SEARCH_BTN, BUDGET_LBL, DIET_LBL, PAGE_TITLES

def render_food_assistant(lang, chatbot, db):
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
                    
                except Exception:
                    friendly_msg = {
                        'English': "😅 Our AI helper is taking a short break. Please try again in a few minutes!",
                        'Simplified Chinese': "😅 我们的AI助手正在短暂休息。请几分钟后再试！",
                        'Malay': "😅 Pembantu AI kami sedang berehat sebentar. Sila cuba lagi dalam beberapa minit!",
                        'Tamil': "😅 எங்கள் AI உதவியாளர் சிறிது ஓய்வு எடுத்துக்கொள்கிறார். சில நிமிடங்களில் மீண்டும் முயற்சிக்கவும்!",
                    }
                    st.info(friendly_msg.get(lang, friendly_msg['English']))

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