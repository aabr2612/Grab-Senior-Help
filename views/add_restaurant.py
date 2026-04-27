import streamlit as st
from menu_parser import extract_menu_items
from config.languages import PAGE_TITLES
import os

def render_add_restaurant(lang, db):
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
    
    name_placeholder = {'English': "e.g. Hai Kee Porridge", 'Simplified Chinese': "例如：海记粥品", 'Malay': "cth: Hai Kee Porridge", 'Tamil': "எ.கா: ஹாய் கீ கஞ்சி"}
    loc_placeholder = {'English': "e.g. Toa Payoh Lor 8, #01-12", 'Simplified Chinese': "例如：大巴窑8巷 #01-12", 'Malay': "cth: Toa Payoh Lor 8, #01-12", 'Tamil': "எ.கா: தோ பாயோ லோர் 8, #01-12"}
    name_label = {'English': "🏢 Restaurant Name", 'Simplified Chinese': "🏢 餐厅名称", 'Malay': "🏢 Nama Restoran", 'Tamil': "🏢 உணவகத்தின் பெயர்"}
    loc_label = {'English': "📍 Where is it?", 'Simplified Chinese': "📍 在哪里？", 'Malay': "📍 Di mana?", 'Tamil': "📍 எங்கே உள்ளது?"}
    
    with col1:
        restaurant_name = st.text_input(name_label.get(lang, name_label['English']), placeholder=name_placeholder.get(lang, name_placeholder['English']))
    with col2:
        restaurant_location = st.text_input(loc_label.get(lang, loc_label['English']), placeholder=loc_placeholder.get(lang, loc_placeholder['English']))

    st.markdown("<br>", unsafe_allow_html=True)
    step2_title = {'English': "### 2️⃣ Share Menu File", 'Simplified Chinese': "### 2️⃣ 分享菜单文件", 'Malay': "### 2️⃣ Kongsi Fail Menu", 'Tamil': "### 2️⃣ மெனு கோப்பைப் பகிரவும்"}
    st.markdown(step2_title.get(lang, step2_title['English']))

    uploader_label = {'English': "📎 Place the menu file here", 'Simplified Chinese': "📎 将菜单文件放在这里", 'Malay': "📎 Letakkan fail menu di sini", 'Tamil': "📎 மெனு கோப்பை இங்கே வைக்கவும்"}
    uploaded_file = st.file_uploader(uploader_label.get(lang, uploader_label['English']), type=['pdf'], key="menu_upload")

    if uploaded_file:
        got_it = {
            'English': f"✅ <b>Got it!</b> I'm ready to learn the menu for: {uploaded_file.name}",
            'Simplified Chinese': f"✅ <b>收到！</b> 我已准备好学习：{uploaded_file.name} 的菜单",
            'Malay': f"✅ <b>Faham!</b> Saya sedia untuk mempelajari menu: {uploaded_file.name}",
            'Tamil': f"✅ <b>புரிந்தது!</b> மெனுவைக் கற்க தயாராக உள்ளேன்: {uploaded_file.name}",
        }
        st.markdown(f"""
        <div style='background:#F0FFF4; border:2px solid #28a745; border-radius:12px; padding:14px 20px; font-size:18px; color:#1a5e2a; margin:10px 0;'>
            {got_it.get(lang, got_it['English'])}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    upload_btn_label = {'English': "📤  Remember this restaurant", 'Simplified Chinese': "📤  记住这个餐厅", 'Malay': "📤  Ingat restoran ini", 'Tamil': "📤  இந்த உணவகத்தை நினைவில் கொள்"}
    if st.button(upload_btn_label.get(lang, upload_btn_label['English']), use_container_width=True, key="upload_btn"):
        name_warn = {'English': "⚠️ Please tell me the restaurant's name!", 'Simplified Chinese': "⚠️ 请告诉我餐厅名称！", 'Malay': "⚠️ Sila beritahu nama restoran!", 'Tamil': "⚠️ உணவகத்தின் பெயரைச் சொல்லுங்கள்!"}
        file_warn = {'English': "⚠️ Please share a menu file with me first!", 'Simplified Chinese': "⚠️ 请先分享菜单文件！", 'Malay': "⚠️ Sila kongsi fail menu dahulu!", 'Tamil': "⚠️ முதலில் மெனு கோப்பைப் பகிரவும்!"}
        
        if not restaurant_name.strip():
            st.warning(name_warn.get(lang, name_warn['English']))
        elif not uploaded_file:
            st.warning(file_warn.get(lang, file_warn['English']))
        else:
            spinner_msg = {'English': "📖 Learning the dishes from the menu...", 'Simplified Chinese': "📖 正在学习菜单中的菜品...", 'Malay': "📖 Sedang mempelajari hidangan dari menu...", 'Tamil': "📖 மெனுவிலிருந்து உணவுகளைக் கற்கிறேன்..."}
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

                st.session_state.restaurants[restaurant_name.strip()] = {'location': restaurant_location.strip(), 'items': [i for i in menu_items if i.strip()]}
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
                    many_more = {'English': "... and many more dishes.", 'Simplified Chinese': "... 还有更多菜品。", 'Malay': "... dan banyak lagi hidangan.", 'Tamil': "... மேலும் பல உணவுகள்."}
                    with st.expander(expander_title.get(lang, expander_title['English'])):
                        cols = st.columns(2)
                        for j, item in enumerate(filtered[:40]):
                            with cols[j % 2]:
                                st.markdown(f'<div class="badge">🍴 {item}</div>', unsafe_allow_html=True)
                        if len(filtered) > 40:
                            st.info(many_more.get(lang, many_more['English']))