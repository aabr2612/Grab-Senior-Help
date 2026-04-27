import google.generativeai as genai
import time
from google.api_core import exceptions

class AIChatbot:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        # Priority list of models based on your available quotas
        self.model_priority = [
            'gemini-2.0-flash', 
            'gemini-1.5-flash', 
            'gemini-flash-latest'
        ]
        self.current_model_index = 0
        self.model = genai.GenerativeModel(self.model_priority[self.current_model_index])
        
    def _generate_with_fallback(self, prompt):
        """
        Attempts to generate content, switching to fallback models if quota is exhausted.
        """
        for i in range(self.current_model_index, len(self.model_priority)):
            model_name = self.model_priority[i]
            try:
                temp_model = genai.GenerativeModel(model_name)
                response = temp_model.generate_content(prompt)
                # Success! Update our primary model to this one for future calls
                self.current_model_index = i
                self.model = temp_model
                return response
            except exceptions.ResourceExhausted:
                print(f"⚠️ Quota exhausted for {model_name}, trying fallback...")
                continue
            except exceptions.NotFound:
                print(f"⚠️ Model {model_name} not found, trying next...")
                continue
            except Exception as e:
                # If it's a different error, we should probably stop or log it
                raise e
        
        raise Exception("❌ All Gemini models reached their quota limits. Please try again later.")

    def recommend_food(self, user_input, language_code, dietary_restrictions, price_range, db_context=""):
        """
        Generate food recommendations based on senior-specific prompt and local database
        """
        prompt = f"""
        You are a helpful assistant for senior citizens in Singapore.
        
        {db_context if db_context else "Note: No specific restaurant database provided, use your general knowledge of Singapore food."}
        
        User request: {user_input}
        Language: {language_code}
        Dietary restrictions to avoid: {', '.join(dietary_restrictions) if dietary_restrictions else 'None'}
        Price range: ${price_range[0]} - ${price_range[1]} SGD
        
        Recommend the best matching restaurants and dishes from the provided database (if any). 
        If no restaurants in the database match, suggest general Singaporean options that fit the criteria.
        
        Recommend:
        1. Restaurant name
        2. Dish name and description
        3. Price
        4. Why this is a good choice for them
        
        Format the response in a friendly, encouraging way for a senior citizen.
        Use large bullet points and clear spacing.
        """
        response = self._generate_with_fallback(prompt)
        return response.text

    def search_restaurants(self, user_request, restaurants_data, language='english'):
        prompt = f"User request: {user_request}\nAvailable restaurants: {restaurants_data}"
        response = self._generate_with_fallback(prompt)
        return response.text
    
    def search_menu_items(self, user_request, menu_data, language='english'):
        prompt = f"User request: {user_request}\nMenu items: {menu_data}"
        response = self._generate_with_fallback(prompt)
        return response.text
    
    def translate_request(self, text, target_language='english'):
        prompt = f"Translate to English: {text}"
        response = self._generate_with_fallback(prompt)
        return response.text
    
    def chat(self, user_message, context=""):
        prompt = f"Context: {context}\nUser: {user_message}"
        response = self._generate_with_fallback(prompt)
        return response.text
