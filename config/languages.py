LANGUAGES = {
    '🇬🇧  English': 'English',
    '🇨🇳  中文 (Chinese)': 'Simplified Chinese',
    '🇲🇾  Bahasa Melayu': 'Malay',
    '🇮🇳  தமிழ் (Tamil)': 'Tamil'
}

NAV_KEYS = ['home', 'food_assistant', 'add_restaurant', 'history']

NAV_LABELS = {
    'English': {
        'home': '🏠  Home',
        'food_assistant': '🤖  Food Assistant',
        'add_restaurant': '📄  Add Restaurant',
        'history': '📋  History & Restaurants'
    },
    'Simplified Chinese': {
        'home': '🏠  首页',
        'food_assistant': '🤖  美食助手',
        'add_restaurant': '📄  添加餐厅',
        'history': '📋  历史与餐厅'
    },
    'Malay': {
        'home': '🏠  Laman Utama',
        'food_assistant': '🤖  Pembantu Makanan',
        'add_restaurant': '📄  Tambah Restoran',
        'history': '📋  Sejarah & Restoran'
    },
    'Tamil': {
        'home': '🏠  முகப்பு',
        'food_assistant': '🤖  உணவு உதவியாளர்',
        'add_restaurant': '📄  உணவகம் சேர்க்கவும்',
        'history': '📋  வரலாறு & உணவகங்கள்'
    }
}

PAGE_TITLES = {
    'English': {
        'home': 'Home',
        'food_assistant': 'Food Assistant',
        'add_restaurant': 'Add Restaurant',
        'history': 'History & Restaurants'
    },
    'Simplified Chinese': {
        'home': '首页',
        'food_assistant': '美食助手',
        'add_restaurant': '添加餐厅',
        'history': '历史与餐厅'
    },
    'Malay': {
        'home': 'Laman Utama',
        'food_assistant': 'Pembantu Makanan',
        'add_restaurant': 'Tambah Restoran',
        'history': 'Sejarah & Restoran'
    },
    'Tamil': {
        'home': 'முகப்பு',
        'food_assistant': 'உணவு உதவியாளர்',
        'add_restaurant': 'உணவகம் சேர்க்கவும்',
        'history': 'வரலாறு & உணவகங்கள்'
    }
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

HOME_FEATURES = {
    'English': [
        ("🤖", "Talk to me", "Tell me what you'd like to eat and I'll find the best dishes for you."),
        ("📄", "Add a Menu", "Share a restaurant's menu with me and I'll remember all the dishes."),
        ("💰", "Save Money", "Tell me your budget and I'll only show you what fits your wallet."),
        ("🛡️", "Eat Safely", "Tell me what you can't eat and I'll make sure you stay safe and healthy."),
    ],
    'Simplified Chinese': [
        ("🤖", "跟我聊聊", "告诉我您想吃什么，我会为您找到最好的菜肴。"),
        ("📄", "添加菜单", "分享餐厅菜单给我，我会记住所有菜品。"),
        ("💰", "省钱", "告诉我您的预算，我只显示适合您的选择。"),
        ("🛡️", "安全饮食", "告诉我您不能吃什么，我会确保您的安全与健康。"),
    ],
    'Malay': [
        ("🤖", "Bercakap dengan Saya", "Beritahu saya apa yang anda ingin makan dan saya akan cari hidangan terbaik."),
        ("📄", "Tambah Menu", "Kongsi menu restoran dengan saya dan saya akan ingat semua hidangan."),
        ("💰", "Jimat Wang", "Beritahu belanjawan anda dan saya akan tunjukkan yang sesuai."),
        ("🛡️", "Makan Selamat", "Beritahu saya apa yang anda tidak boleh makan dan saya pastikan anda selamat."),
    ],
    'Tamil': [
        ("🤖", "என்னிடம் பேசுங்கள்", "நீங்கள் என்ன சாப்பிட விரும்புகிறீர்கள் என்று சொல்லுங்கள், சிறந்த உணவைக் கண்டுபிடிப்பேன்."),
        ("📄", "மெனு சேர்க்கவும்", "உணவக மெனுவைப் பகிருங்கள், அனைத்து உணவுகளையும் நினைவில் கொள்கிறேன்."),
        ("💰", "பணம் சேமிக்க", "உங்கள் பட்ஜெட்டைச் சொல்லுங்கள், பொருத்தமானவற்றை மட்டும் காட்டுகிறேன்."),
        ("🛡️", "பாதுகாப்பாக சாப்பிட", "எதைச் சாப்பிட முடியாது என்று சொல்லுங்கள், பாதுகாப்பாக வைத்திருப்பேன்."),
    ],
}

HOME_STEPS = {
    'English': [
        ("1", "Pick your favorite language on the left side."),
        ("2", "Go to <b>🤖 Food Assistant</b> and tell me what you feel like eating."),
        ("3", "Let me know if there are foods you need to avoid (like pork or seafood)."),
        ("4", "Set your price range and press the big green button!"),
        ("5", "Look at my suggestions and enjoy a wonderful meal! 😊"),
    ],
    'Simplified Chinese': [
        ("1", "在左侧选择您喜欢的语言。"),
        ("2", "前往<b>🤖 美食助手</b>，告诉我您想吃什么。"),
        ("3", "告诉我您需要避免的食物（如猪肉或海鲜）。"),
        ("4", "设定您的价格范围，然后按绿色大按钮！"),
        ("5", "查看我的建议，享受美好的一餐！😊"),
    ],
    'Malay': [
        ("1", "Pilih bahasa kegemaran anda di sebelah kiri."),
        ("2", "Pergi ke <b>🤖 Pembantu Makanan</b> dan beritahu saya apa yang anda ingin makan."),
        ("3", "Beritahu saya jika ada makanan yang perlu dielakkan (seperti babi atau makanan laut)."),
        ("4", "Tetapkan julat harga anda dan tekan butang hijau besar!"),
        ("5", "Lihat cadangan saya dan nikmati hidangan yang hebat! 😊"),
    ],
    'Tamil': [
        ("1", "இடது பக்கத்தில் உங்களுக்கு பிடித்த மொழியைத் தேர்ந்தெடுக்கவும்."),
        ("2", "<b>🤖 உணவு உதவியாளர்</b> சென்று நீங்கள் என்ன சாப்பிட விரும்புகிறீர்கள் என்று சொல்லுங்கள்."),
        ("3", "தவிர்க்க வேண்டிய உணவுகள் இருந்தால் சொல்லுங்கள்."),
        ("4", "விலை வரம்பை அமைத்து பெரிய பச்சை பொத்தானை அழுத்தவும்!"),
        ("5", "எனது பரிந்துரைகளைப் பார்த்து சிறந்த உணவை அனுபவியுங்கள்! 😊"),
    ],
}

HOME_NO_RESTAURANTS = {
    'English': '<strong>💡 No restaurants yet!</strong> Go to <b>📄 Add Restaurant</b> on the left to share a menu with me and get started.',
    'Simplified Chinese': '<strong>💡 还没有餐厅！</strong> 前往左侧的<b>📄 添加餐厅</b>，与我分享菜单即可开始。',
    'Malay': '<strong>💡 Tiada restoran lagi!</strong> Pergi ke <b>📄 Tambah Restoran</b> di sebelah kiri untuk berkongsi menu dan mulakan.',
    'Tamil': '<strong>💡 இன்னும் உணவகங்கள் இல்லை!</strong> இடதுபுறம் உள்ள <b>📄 உணவகம் சேர்க்கவும்</b> சென்று மெனுவைப் பகிர்ந்து தொடங்கவும்.',
}

HOME_FOOTER = {
    'English': 'Helping you eat well every day',
    'Simplified Chinese': '帮助您每天吃得好',
    'Malay': 'Membantu anda makan dengan baik setiap hari',
    'Tamil': 'ஒவ்வொரு நாளும் நன்றாக சாப்பிட உதவுகிறது',
}