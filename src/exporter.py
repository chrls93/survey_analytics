import json
import pandas as pd

class Exporter:
    @staticmethod
    def save_to_excel(df, filename="wyniki_analizy.xlsx"):
        df.to_excel(f"output/{filename}", index=False)

    @staticmethod
    def save_to_json(data, filename="raport.json"):
        with open(f"output/{filename}", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)