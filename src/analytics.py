from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import pandas as pd

class AnalyticsEngine:
    @staticmethod
    def calculate_metrics(y_true, y_pred):
        """Oblicza metryki rzetelności systemu (Wymaganie niefunkcjonalne nr 1)"""
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "f1_macro": f1_score(y_true, y_pred, average='macro'),
            "confusion_matrix": confusion_matrix(y_true, y_pred).tolist()
        }

    @staticmethod
    def estimate_costs(total_tokens, model_name="gemini-1.5-flash"):
        """Szacowanie kosztów (Wymaganie niefunkcjonalne nr 3)"""
        # Przykładowe stawki (do aktualizacji w pracy)
        rates = {
            "gemini-1.5-flash": 0.000125, # USD za 1k tokenów
            "bielik": 0.0 # Model lokalny
        }
        cost = (total_tokens / 1000) * rates.get(model_name, 0)
        return round(cost, 4)