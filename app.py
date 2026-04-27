import streamlit as st
from database import Database
from ai_chatbot import AIChatbot
from config.settings import init_page_config, load_css, init_session_state, inject_mobile_script
from components.sidebar import render_sidebar
from views.home import render_home
from views.food_assistant import render_food_assistant
from views.add_restaurant import render_add_restaurant
from views.history import render_history
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config & CSS ───
init_page_config()
load_css()
inject_mobile_script()

# ─── Init DB & Chatbot ───
db = Database('grab_helper.db')
api_key = os.getenv('GOOGLE_API_KEY')
chatbot = AIChatbot(api_key) if api_key else None

# ─── Session State ───
init_session_state(db)

# ─── Sidebar ───
lang, active = render_sidebar(db, chatbot)

# ─── Page Router ───
if active == 'home':
    render_home(lang)
elif active == 'food_assistant':
    render_food_assistant(lang, chatbot, db)
elif active == 'add_restaurant':
    render_add_restaurant(lang, db)
elif active == 'history':
    render_history(lang)