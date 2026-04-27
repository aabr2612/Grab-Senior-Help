# GrabEats Senior Helper 🍜

A user-friendly Streamlit application designed to empower senior citizens in Singapore to discover and order food with ease. Featuring AI-powered recommendations, multilingual support, and a senior-optimized interface.

## 🌟 Key Features

### 1. **AI-Powered Food Assistant**
- **Personalized Recommendations**: Chat with an AI assistant (Google Gemini) to find dishes based on your cravings (e.g., "I want something soft and warm").
- **Dietary Safety**: Built-in filters for common dietary restrictions (No Pork, No Seafood, Vegetarian, Halal, etc.).
- **Budget Conscious**: Set a price range per dish to find affordable meals that fit your wallet.

### 2. **Senior-Optimized Interface**
- **Visual Clarity**: Large font sizes, high-contrast colors, and a clean layout designed for easy reading.
- **Simplified Navigation**: Minimalistic sidebar and intuitive buttons.
- **Mobile Responsive**: Custom scripts to ensure a smooth experience on tablets and smartphones.
- **Multilingual**: Full interface support for **English**, **简体中文** (Chinese), **Bahasa Melayu** (Malay), and **தமிழ்** (Tamil).

### 3. **Smart Menu Management**
- **PDF Menu Parsing**: Upload restaurant menus in PDF format. The app uses OCR (Optical Character Recognition) to extract dishes and prices automatically.
- **Restaurant Discovery**: Browse a curated list of local favorites like Song Fa Bak Kut Teh and Swee Choon.
- **Persistent History**: Saves your chat interactions and added restaurants for future reference.

## 🛠️ Tech Stack

- **Framework**: [Streamlit](https://streamlit.io/)
- **AI Engine**: [Google Gemini Pro API](https://aistudio.google.com/)
- **Database**: SQLite
- **OCR & PDF Processing**: `pdfplumber`, `pytesseract`, `pdf2image`
- **Styling**: Custom Vanilla CSS & Google Fonts (Nunito & Lora)

## 📂 Project Structure

```text
grab-senior-help/
├── app.py                 # Main entry point & routing
├── ai_chatbot.py          # Gemini AI integration logic
├── database.py            # SQLite database management
├── menu_parser.py         # PDF processing & OCR logic
├── seed_db.py             # Initial database population script
├── grab_helper.db         # SQLite database file
├── components/            # UI components
│   └── sidebar.py         # Navigation & language selector
├── config/                # App configuration
│   ├── languages.py       # Multilingual translations
│   └── settings.py        # Page config, CSS, & session state
├── views/                 # Application pages
│   ├── home.py            # Welcome screen
│   ├── food_assistant.py  # AI Chat interface
│   ├── add_restaurant.py  # Menu upload & restaurant creation
│   └── history.py         # Saved restaurants & chats
└── requirements.txt       # Python dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system.
- A Google Gemini API Key.

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/aabr2612/grab-senior-helper.git
   cd grab-senior-helper
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. **Initialize Database**
   ```bash
   python seed_db.py
   ```

6. **Run the App**
   ```bash
   streamlit run app.py
   ```

## 📖 Usage Guide

1. **Select Language**: Use the sidebar to switch between English, Chinese, Malay, or Tamil.
2. **Find Food**: Navigate to **Food Assistant**, enter your preferences/dietary needs, and get recommendations.
3. **Add Menus**: Go to **Add Restaurant** to upload a PDF menu. The app will extract dishes and add them to your local database.
4. **View History**: Check **History & Restaurants** to see previously added places and your chat logs.

## 🛡️ Accessibility Features

- ✅ **Dynamic Scaling**: Font sizes scale appropriately for various screen sizes.
- ✅ **High Contrast**: Uses a "Grab-inspired" green and white theme with high legibility.
- ✅ **Icon-Assisted**: Uses emojis and icons alongside text for better cognitive recognition.
- ✅ **Simple Actions**: Large, "fat-finger" friendly buttons for easier interaction.

## 📝 License

This project is licensed under the MIT License.

---
**Made with ❤️ for the Seniors of Singapore**
