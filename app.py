import streamlit as st
import pandas as pd
from src.data_loader import DataLoader
from src.anonymizer import Anonymizer
from src.orchestrator import LLMOrchestrator
from src.data_fetcher import DataFetcher

st.set_page_config(page_title="Survey Analyzer", layout="wide")

st.title("Analiza ankiet otwartych przy użyciu LLM")

uploaded_file = st.sidebar.file_uploader("Wgraj plik z ankietami (.csv, .xlsx)", type=["csv", "xlsx"])

if not uploaded_file:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Pobierz przykładowy dataset")
    datasets = {
        "Allegro reviews": "https://klejbenchmark.com/static/data/klej_ar.zip",
        "PolEval Hotels": "https://placeholder.com/poleval_hotels.zip",
        "Syntetyczna Ankieta HR": "https://placeholder.com/hr_survey.zip"
    }
    
    selected_dataset = st.sidebar.selectbox("Wybierz dataset", list(datasets.keys()))
    if st.sidebar.button("Pobierz i rozpakuj"):
        with st.spinner(f"Pobieranie {selected_dataset}..."):
            fetcher = DataFetcher()
            fetcher.download_and_extract(datasets[selected_dataset])
        st.sidebar.success("Dataset pobrany!")

model_choice = st.sidebar.selectbox("Wybierz model", ["HerBERT", "Gemini", "Bielik (Lokalnie)"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Podgląd danych:", df.head())
    
    if st.button("Uruchom analizę"):
        with st.spinner('Trwa przetwarzanie...'):
            # 1. Anonimizacja
            anon = Anonymizer()
            df['clean_text'] = df['raw_text'].apply(anon.mask_pii)
            
            # 2. Analiza (Orkiestracja)
            # Tutaj pętla po wierszach i wywołanie orkiestratora
            
            st.success("Analiza zakończona!")
            st.dataframe(df)