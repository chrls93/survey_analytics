from google import genai
from llama_cpp import Llama
import os
from dotenv import load_dotenv


class LLMOrchestrator:
    def __init__(self, mode="gemini", gemini_model="gemini-2.5-flash"):
        self.mode = mode
        self.gemini_model = gemini_model
        load_dotenv()

    def analyze_sentiment(self, text: str):
        if self.mode == "gemini":
            return self._call_gemini(text)
        elif self.mode == "bielik":
            return self._call_bielik(text)
        elif self.mode == "herbert":
            return self._call_herbert(text)

    def _call_gemini(self, text):
        """Calls Google Gemini API"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("ERROR: GOOGLE_API_KEY not found in environment variables")
            return None
        
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=self.gemini_model,
                contents=text
            )
            if response and response.text:
                return response.text
            else:
                print(f"Empty response from Gemini")
                return None
        except Exception as e:
            print(f"Gemini error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _call_gemini_with_usage(self, text: str):
        """Calls Gemini API and returns text + token usage statistics"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("ERROR: GOOGLE_API_KEY not found in environment variables")
            return None, None
        
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=self.gemini_model,
                contents=text
            )
            
            if response and response.text:
                # Extract token usage statistics
                usage = response.usage_metadata
                token_stats = {
                    "prompt_tokens": usage.prompt_token_count,
                    "completion_tokens": usage.candidates_token_count,
                    "total_tokens": usage.total_token_count
                }
                return response.text, token_stats
            else:
                print(f"Empty response from Gemini")
                return None, None
                
        except Exception as e:
            print(f"Gemini error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None, None

    def _call_bielik(self, text):
        # Logika dla lokalnego modelu przez llama-cpp
        pass