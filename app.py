import streamlit as st
from database import Database
from menu_parser import extract_menu_items
from ai_chatbot import AIChatbot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration for senior citizens - large fonts and simple interface
st.set_page_config(
    page_title="GRAB Senior Helper",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for larger text and better accessibility
st.markdown("""
    <style>
    html, body, [class*="st-"] {
        font-size: 22px;
    }
    h1 {
        font-size: 56px !important;
        color: #FF5733;
    }
    h2 {
        font-size: 42px !important;
    }
    h3 {
        font-size: 32px !important;
    }
    .stButton>button {
        font-size: 24px !important;
        height: 3em !important;
        background-color: #FF5733 !important;
        color: white !important;
    }
    .stButton>button:hover {
        background-color: #E64A19 !important;
        color: white !important;
    }
    .stTextArea>div>div>textarea {
        font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize database
db = Database('grab_helper.db')

# Initialize AI chatbot
api_key = os.getenv('GOOGLE_API_KEY')
chatbot = None
if api_key:
    chatbot = AIChatbot(api_key)
else:
    st.warning("⚠️ AI Features are disabled. Please set GOOGLE_API_KEY in .env file.")

# Initialize session state from Database
if 'restaurants_loaded' not in st.session_state:
    st.session_state.restaurants_loaded = False

if not st.session_state.restaurants_loaded:
    st.session_state.restaurants = {}
    saved_restaurants = db.get_restaurants()
    for r in saved_restaurants:
        # r = (id, name, location)
        res_id = r[0]
        res_name = r[1]
        
        # Load dishes for this restaurant
        all_items = []
        menus = db.get_menus(res_id)
        for m in menus:
            dishes = db.get_dishes(m[0])
            for d in dishes:
                all_items.append(f"{d[2]} (${d[3]:.2f})")
                
        st.session_state.restaurants[res_name] = {
            'id': res_id,
            'location': r[2],
            'items': all_items,
            'rating': 4.5
        }
    st.session_state.restaurants_loaded = True

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Language support
LANGUAGES = {
    'English': 'English',
    '中文 (Chinese)': 'Simplified Chinese',
    'Bahasa Melayu': 'Malay',
    'தமிழ் (Tamil)': 'Tamil'
}

# Translations for the UI
UI_TEXT = {
    'English': {
        'welcome': "Welcome to GRAB Senior Helper! 👋",
        'subtitle': "Find Your Favorite Food - Easy to Use!",
        'home': "🏠 Home",
        'chatbot': "🤖 Food Chatbot",
        'upload': "📄 Upload Menu",
        'orders': "📊 My Orders",
        'search_btn': "🔍 Search",
        'upload_btn': "📤 Upload Menu",
        'food_pref': "What would you like to eat?",
        'dietary': "Any foods you can't eat?",
        'budget': "Price range per item (SGD)",
    },
    'Simplified Chinese': {
        'welcome': "欢迎使用 GRAB 老年人助手！👋",
        'subtitle': "轻松寻找您最喜爱的美食！",
        'home': "🏠 首页",
        'chatbot': "🤖 美食聊天机器人",
        'upload': "📄 上传菜单",
        'orders': "📊 我的订单",
        'search_btn': "🔍 搜索",
        'upload_btn': "📤 上传菜单",
        'food_pref': "您想吃什么？",
        'dietary': "有什么忌口的吗？",
        'budget': "每份价格范围 (新币)",
    }
}

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    selected_lang_name = st.selectbox("Choose Your Language / 选择语言", list(LANGUAGES.keys()))
    lang_val = LANGUAGES[selected_lang_name]
    
    # Get text based on selected language
    text = UI_TEXT.get(lang_val, UI_TEXT['English'])
    
    st.divider()
    st.header("📋 Navigation")
    page = st.radio("Select an option:", 
                     [text['home'], text['chatbot'], text['upload'], text['orders']])

# Main title
st.title("🍽️ GRAB Senior Helper")
st.subheader(text['subtitle'])

# HOME PAGE
if page == text['home']:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://via.placeholder.com/400x300?text=Delicious+Food", use_container_width=True)
    
    with col2:
        st.markdown(f"""
        ### {text['welcome']}
        
        This app is specifically designed to help you order food easily:
        - **🤖 Chat with AI**: Tell us what you like, and we'll suggest dishes.
        - **📄 Scan Menus**: Upload any menu and we'll read it for you.
        - **💰 Save Money**: We find food within your budget.
        - **🛡️ Stay Safe**: We remember your allergies and dietary needs.
        
        **Click the options on the left to start!**
        """)
    
    st.divider()
    st.header("📍 Your Nearby Restaurants")
    if st.session_state.restaurants:
        cols = st.columns(3)
        for i, (name, data) in enumerate(st.session_state.restaurants.items()):
            with cols[i % 3]:
                st.info(f"**{name}**\n\n📍 {data['location']}")
    else:
        st.write("No restaurants saved yet. Go to 'Upload Menu' to add one!")

# FOOD CHATBOT PAGE
elif page == text['chatbot']:
    st.header(text['chatbot'])
    st.write("Type what you feel like eating today!")
    
    # User input for food preference
    user_input = st.text_area(text['food_pref'], 
                              placeholder="e.g. Soft food for lunch, or I want spicy laksa...",
                              height=120)
    
    # Dietary restrictions
    col1, col2 = st.columns(2)
    with col1:
        dietary_restrictions = st.multiselect(
            text['dietary'],
            ["Pork", "Beef", "Seafood", "Nuts", "Dairy", "Spicy", "Vegetarian", "Halal"]
        )
    
    with col2:
        price_range = st.select_slider(
            text['budget'],
            options=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 30, 50],
            value=(5, 15)
        )
    
    if st.button(text['search_btn'], use_container_width=True):
        if user_input and chatbot:
            with st.spinner("Finding the best options for you..."):
                # Prepare restaurant data for the AI to search through
                db_context = ""
                if st.session_state.restaurants:
                    db_context = "Here are the restaurants in our database:\n"
                    for name, data in st.session_state.restaurants.items():
                        items_str = ", ".join(data.get('items', []))
                        db_context += f"- {name} (Location: {data['location']}). Menu items: {items_str}\n"

                recommendation = chatbot.recommend_food(
                    user_input, lang_val, dietary_restrictions, price_range, db_context
                )
                st.success("Here are my recommendations:")
                st.markdown(recommendation)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": recommendation
                })
        elif not chatbot:
            st.error("AI is not configured. Please check your API key.")
        else:
            st.warning("Please type something first!")

# UPLOAD MENU PAGE
elif page == text['upload']:
    st.header(text['upload'])
    st.write("Upload a photo or PDF of a menu to save it.")
    
    # Restaurant info
    col1, col2 = st.columns(2)
    with col1:
        restaurant_name = st.text_input("Restaurant Name")
    with col2:
        restaurant_location = st.text_input("Location/Address")
    
    # PDF upload
    uploaded_file = st.file_uploader("Upload Menu (PDF)", type=['pdf'])
    
    if uploaded_file and st.button(text['upload_btn'], use_container_width=True):
        with st.spinner("Processing menu..."):
            # Save uploaded file
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract menu items
            menu_items = extract_menu_items(temp_path)
            
            # Store in database
            if restaurant_name:
                db.add_restaurant(restaurant_name, restaurant_location)
                st.session_state.restaurants[restaurant_name] = {
                    'location': restaurant_location,
                    'items': menu_items,
                    'rating': 4.5
                }
                st.success(f"✅ {restaurant_name} has been added to your list!")
            
            # Display menu items
            st.info(f"We found {len(menu_items)} items on this menu.")
            with st.expander("Show found items"):
                for item in menu_items[:30]:
                    if item.strip():
                        st.write(f"• {item}")
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)

# MY ORDERS PAGE
elif page == text['orders']:
    st.header(text['orders'])
    
    tab1, tab2 = st.tabs(["🕒 Search History", "🏢 Saved Restaurants"])
    
    with tab1:
        if st.session_state.chat_history:
            for i, entry in enumerate(reversed(st.session_state.chat_history), 1):
                with st.expander(f"Search: {entry['user'][:40]}..."):
                    st.markdown(entry['bot'])
        else:
            st.info("No history yet.")
            
    with tab2:
        if st.session_state.restaurants:
            for restaurant, data in st.session_state.restaurants.items():
                st.write(f"### {restaurant}")
                st.write(f"📍 {data['location']}")
                st.divider()
        else:
            st.info("No restaurants saved yet.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 16px; padding: 20px;'>
    <p>GRAB Senior Helper v1.1 | Developed with ❤️ for Singapore Seniors</p>
</div>
""", unsafe_allow_html=True)
