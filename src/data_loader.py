import pandas as pd
import os
import re
import spacy


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

    def prepare_texts(self, df, text_column="text", min_word_length=4):
        """
        Czyszczenie i filtracja tekstów:
        - Konwersja na małe litery
        - Usunięcie URL-i i adresów email
        - Usunięcie znaków specjalnych
        - Normalizacja spacji
        - Filtracja tekstów poniżej min_word_length słów
        
        Returns:
            tuple: (raw_texts, cleaned_texts, texts, all_stopwords)
                - raw_texts: oryginalne teksty
                - cleaned_texts: wyczyszczone teksty
                - texts: wyczyszczone teksty spełniające kryterium długości
                - all_stopwords: lista stop-words dla języka polskiego
        """
        def clean_and_filter_text(text):
            if not isinstance(text, str):
                return ""
            text = text.lower()
            text = re.sub(r'http\S+|www.\S+|[\w\.-]+@[\w\.-]+', '', text)
            text = re.sub(r'[^\w\s\-ąćęłńóśźż]', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        
        # Załaduj stop-words
        try:
            nlp = spacy.load("pl_core_news_sm")
        except OSError:
            print("Brak modelu spacy 'pl_core_news_sm'. Pobieranie...")
            os.system("python -m spacy download pl_core_news_sm")
            nlp = spacy.load("pl_core_news_sm")
        
        all_stopwords = list(nlp.Defaults.stop_words) + [
            "allegro", "sprzedawca", "aukcja", "produkt", "przesyłka", 
            "paczka", "super", "polecam"
        ]
        
        # Ekstraktuj surowe teksty
        raw_texts = df[text_column].dropna().tolist()
        print(f"Po usunięciu pustych wierszy zostało {len(raw_texts)} wierszy.")
        
        # Czyszczenie tekstów
        cleaned_texts = [clean_and_filter_text(t) for t in raw_texts]
        print(f"Po usunięciu znaków i czyszczeniu za pomocą regex zostało {len(cleaned_texts)} wierszy.")
        
        # Filtracja po długości
        dataset_texts = [t for t in cleaned_texts if len(t.split()) > min_word_length]
        print(f"Po filtracji długości (>{min_word_length} słów) zostało {len(dataset_texts)} tekstów do analizy.")
        
        return raw_texts, cleaned_texts, dataset_texts, all_stopwords