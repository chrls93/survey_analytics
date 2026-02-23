import pandas as pd
import os

class DataLoader:
    def __init__(self, allowed_extensions=('.csv', '.xlsx')):
        self.allowed_extensions = allowed_extensions

    def load_data(self, file_path):
        _, extension = os.path.splitext(file_path)
        if extension not in self.allowed_extensions:
            raise ValueError(f"Nieobsługiwany format pliku: {extension}")

        if extension == '.csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        return self._validate(df)

    def _validate(self, df):
        # Sprawdzenie czy zbiór nie jest pusty
        if df.empty:
            raise ValueError("Plik jest pusty.")
        
        # Usuwanie duplikatów i pustych odpowiedzi (wymaganie inżynieryjne)
        initial_count = len(df)
        df = df.dropna(subset=[df.columns[0]]) # Zakładamy, że pierwsza kolumna to tekst
        df = df.drop_duplicates()
        
        print(f"Załadowano {len(df)} rekordów (usunięto {initial_count - len(df)} niepoprawnych).")
        return df