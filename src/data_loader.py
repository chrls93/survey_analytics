import pandas as pd
import os


class DataLoader:
    def __init__(self, allowed_extensions=('.csv', '.xlsx', '.xls', '.json', '.txt',
                                           '.tsv')):
        self.allowed_extensions = allowed_extensions

    def load_data(self, file_path):
        """
        Wczytuje plik źródłowy za pomocą pandas.
        Weryfikuje strukturę danych i dokonuje preprocessing'u.
        """
        _, extension = os.path.splitext(file_path)
        if extension not in self.allowed_extensions:
            raise ValueError(f"Nieobsługiwany format pliku: {extension}")

        if extension == '.csv':
            df = pd.read_csv(file_path)
        elif extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        elif extension == '.xlsx' or extension == '.xls':
            df = pd.read_excel(file_path)
        elif extension == '.json':
            df = pd.read_json(file_path)
        elif extension == '.txt':
            df = pd.read_csv(file_path, sep='\t')
        else:
            raise ValueError(f"Nieobsługiwany format pliku: {extension}")

        return self._validate(df)

    def _validate(self, df):
        """
        Weryfikuje strukturę danych i dokonuje czyszczenia wstępnego (preprocessing):
        - Sprawdza czy zbiór nie jest pusty
        - Usuwa zduplikowane kolumny (jeśli występują)
        - Usuwa wiersze z pustymi wartościami w kolumnie tekstowej
        - Usuwa zduplikowane wiersze
        """
        if df.empty:
            raise ValueError("Plik jest pusty.")
        
        if "text" not in df.columns:
            raise ValueError("Brak kolumny 'text' w pliku. Nazwij w ten sposób kolumnę, która ma zostać poddana analizie.")
        
        initial_count = len(df)
        
        # Usuń zduplikowane kolumny
        df = df.loc[:, ~df.columns.duplicated()]
        
        # Usuń puste wiersze (NaN w pierwszej kolumnie - założenie że to kolumna tekstowa)
        df = df.dropna(subset=[df.columns[0]])
        
        # Usuń zduplikowane wiersze
        df = df.drop_duplicates()
        
        removed = initial_count - len(df)
        print(f"Załadowano {len(df)} rekordów (usunięto {removed} niepoprawnych).")
        
        return df.reset_index(drop=True)