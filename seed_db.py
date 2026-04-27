from database import Database

def seed():
    db = Database('grab_helper.db')
    
    # 1. Ah Tai Hainanese Chicken Rice
    db.add_restaurant("Ah Tai Hainanese Chicken Rice", "Maxwell Food Centre #01-07")
    # Note: add_restaurant doesn't return ID in current class, but we can assume IDs 1-5 for seeding
    db.add_menu(1, "Main Menu")
    db.add_dish(1, "Hainanese Chicken Rice (Standard)", 5.50)
    db.add_dish(1, "Steamed Chicken (Half)", 14.00)
    db.add_dish(1, "Oyster Sauce Vegetables", 4.00)

    # 2. Swee Choon Tim Sum
    db.add_restaurant("Swee Choon Tim Sum", "183-191 Jalan Besar")
    db.add_menu(2, "Dim Sum Selection")
    db.add_dish(2, "Swee Choon Mee Suah Kueh", 3.00)
    db.add_dish(2, "Steamed Siew Mai", 2.80)
    db.add_dish(2, "Har Kow (Prawn Dumpling)", 3.20)
    db.add_dish(2, "Salted Egg Yolk Custard Bun", 4.50)

    # 3. Han's Cafe
    db.add_restaurant("Han's Cafe", "Various Locations - e.g., Suntec City")
    db.add_menu(3, "All Day Sets")
    db.add_dish(3, "Hainanese Pork Chop Rice", 9.80)
    db.add_dish(3, "Fish & Chips", 10.50)
    db.add_dish(3, "Braised Beef Stew with Rice", 11.00)
    db.add_dish(3, "Hot Kopi-O", 1.80)

    # 4. Fun Toast
    db.add_restaurant("Fun Toast", "Raffles City Shopping Centre")
    db.add_menu(4, "Traditional Breakfast")
    db.add_dish(4, "Kaya Butter Toast Set", 5.20)
    db.add_dish(4, "Soft Boiled Eggs (2pcs)", 2.00)
    db.add_dish(4, "Soya Sauce Chicken Noodle", 6.80)
    db.add_dish(4, "Yuan Yang (Coffee & Tea)", 2.20)

    # 5. Song Fa Bak Kut Teh
    db.add_restaurant("Song Fa Bak Kut Teh", "11 New Bridge Road")
    db.add_menu(5, "Signature Pork Rib Soup")
    db.add_dish(5, "Pork Rib Soup (Regular)", 8.50)
    db.add_dish(5, "Premium Loin Rib Soup", 12.00)
    db.add_dish(5, "Braised Pig's Trotter", 7.50)
    db.add_dish(5, "Salted Vegetables", 3.00)

    print("✅ Database successfully seeded with 5 restaurants!")
    db.close()

if __name__ == "__main__":
    seed()
