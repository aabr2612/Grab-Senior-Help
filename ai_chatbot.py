import google.generativeai as genai
import time
from google.api_core import exceptions

class AIChatbot:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model_priority = [
            'gemini-2.5-flash',
            'gemini-2.5-flash-lite',
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
        ]
        self.current_model_index = 0
        self.model = genai.GenerativeModel(self.model_priority[self.current_model_index])
        
    def _generate_with_fallback(self, prompt, retries=2):
        for i in range(self.current_model_index, len(self.model_priority)):
            model_name = self.model_priority[i]

            for attempt in range(retries):
                try:
                    model = genai.GenerativeModel(model_name)

                    response = model.generate_content(
                        prompt,
                        request_options={"timeout": 30}
                    )

                    if response and hasattr(response, "text"):
                        self.current_model_index = i
                        self.model = model
                        return response.text.strip()

                    return "⚠️ Empty response received. Please try again."

                except exceptions.ResourceExhausted:
                    print(f"⚠️ Quota exhausted for {model_name}")
                    break  # go to next model

                except exceptions.NotFound:
                    print(f"⚠️ Model {model_name} not found")
                    break

                except exceptions.DeadlineExceeded:
                    print(f"⏱️ Timeout on {model_name}, retrying...")
                    time.sleep(1)

                except Exception as e:
                    print(f"⚠️ Unexpected error: {str(e)}")
                    time.sleep(1)

        return "❌ AI service is temporarily unavailable. Please try again later."

    def recommend_food(self, user_input, language_code, dietary_restrictions, price_range, db_context=""):
        prompt = f"""
You are a helpful assistant for senior citizens.

{db_context if db_context else "No database provided. Use general food knowledge."}

User request: {user_input}
Language: {language_code}
Dietary restrictions: {', '.join(dietary_restrictions) if dietary_restrictions else 'None'}
Price range: {price_range[0]} - {price_range[1]}

Give:
• Restaurant
• Dish
• Price
• Why it's good (simple explanation)

Make it clear, friendly, and easy to read.
"""
        return self._generate_with_fallback(prompt)

    def search_restaurants(self, user_request, restaurants_data):
        prompt = f"User request: {user_request}\nRestaurants: {restaurants_data}"
        return self._generate_with_fallback(prompt)

    def search_menu_items(self, user_request, menu_data):
        prompt = f"User request: {user_request}\nMenu items: {menu_data}"
        return self._generate_with_fallback(prompt)

    def translate_request(self, text):
        prompt = f"Translate to English: {text}"
        return self._generate_with_fallback(prompt)

    def chat(self, user_message, context=""):
        prompt = f"Context: {context}\nUser: {user_message}"
        return self._generate_with_fallback(prompt)