import streamlit as st
from config.languages import PAGE_TITLES

def render_history(lang):
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
                budget = entry.get('budget', (0, 0))

                conv_title = {
                    'English': f"🔍 Conversation #{len(st.session_state.chat_history) - i + 1}: {preview}",
                    'Simplified Chinese': f"🔍 对话 #{len(st.session_state.chat_history) - i + 1}: {preview}",
                    'Malay': f"🔍 Perbualan #{len(st.session_state.chat_history) - i + 1}: {preview}",
                    'Tamil': f"🔍 உரையாடல் #{len(st.session_state.chat_history) - i + 1}: {preview}",
                }
                foods_avoid = {'English': "<b>Foods to avoid:</b>", 'Simplified Chinese': "<b>避免的食物：</b>", 'Malay': "<b>Makanan untuk dielakkan:</b>", 'Tamil': "<b>தவிர்க்க வேண்டிய உணவுகள்:</b>"}
                your_budget = {'English': "<b>Your budget:</b>", 'Simplified Chinese': "<b>您的预算：</b>", 'Malay': "<b>Belanjawan anda:</b>", 'Tamil': "<b>உங்கள் பட்ஜெட்:</b>"}

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
                'English': """<strong>💡 We haven't talked yet!</strong><br>Go to <b>🤖 Food Assistant</b> and tell me what you'd like to eat.""",
                'Simplified Chinese': """<strong>💡 我们还没聊过！</strong><br>前往<b>🤖 美食助手</b>，告诉我您想吃什么。""",
                'Malay': """<strong>💡 Kita belum berbual lagi!</strong><br>Pergi ke <b>🤖 Pembantu Makanan</b> dan beritahu saya apa yang anda ingin makan.""",
                'Tamil': """<strong>💡 நாங்கள் இன்னும் பேசவில்லை!</strong><br><b>🤖 உணவு உதவியாளர்</b> சென்று நீங்கள் என்ன சாப்பிட விரும்புகிறீர்கள் என்று சொல்லுங்கள்.""",
            }
            st.markdown(f"""<div class="tip-box">{no_chats.get(lang, no_chats['English'])}</div>""", unsafe_allow_html=True)

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

            where_is = {'English': "Where it is:", 'Simplified Chinese': "在哪里：", 'Malay': "Di mana:", 'Tamil': "எங்கே உள்ளது:"}
            not_specified = {'English': "Not specified", 'Simplified Chinese': "未指定", 'Malay': "Tidak dinyatakan", 'Tamil': "குறிப்பிடப்படவில்லை"}
            dishes_saved = {'English': "dishes saved", 'Simplified Chinese': "道菜已保存", 'Malay': "hidangan disimpan", 'Tamil': "உணவுகள் சேமிக்கப்பட்டன"}
            view_all = {'English': "📋 View all", 'Simplified Chinese': "📋 查看全部", 'Malay': "📋 Lihat semua", 'Tamil': "📋 அனைத்தையும் காண்க"}
            dishes_for = {'English': "dishes for", 'Simplified Chinese': "道菜 -", 'Malay': "hidangan untuk", 'Tamil': "உணவுகள் -"}

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
                'English': """<strong>💡 No restaurants remembered yet!</strong><br>Go to <b>📄 Add Restaurant</b> to share a menu file.""",
                'Simplified Chinese': """<strong>💡 还没有记住任何餐厅！</strong><br>前往<b>📄 添加餐厅</b>分享菜单文件。""",
                'Malay': """<strong>💡 Tiada restoran diingati lagi!</strong><br>Pergi ke <b>📄 Tambah Restoran</b> untuk berkongsi fail menu.""",
                'Tamil': """<strong>💡 இன்னும் உணவகங்கள் நினைவில் இல்லை!</strong><br><b>📄 உணவகம் சேர்க்கவும்</b> சென்று மெனு கோப்பைப் பகிரவும்.""",
            }
            st.markdown(f"""<div class="tip-box">{no_restaurants.get(lang, no_restaurants['English'])}</div>""", unsafe_allow_html=True)