from google import genai
from llama_cpp import Llama

class LLMOrchestrator:
    def __init__(self, mode="gemini"):
        self.mode = mode

    def analyze_sentiment(self, text: str):
        if self.mode == "gemini":
            return self._call_gemini(text)
        elif self.mode == "bielik":
            return self._call_bielik(text)
        elif self.mode == "herbert":
            return self._call_herbert(text)

    def _call_gemini(self, text):
        # Logika dla API Google
        pass

    def _call_bielik(self, text):
        # Logika dla lokalnego modelu przez llama-cpp
        pass