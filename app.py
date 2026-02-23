import streamlit as st
import pandas as pd
from src.data_loader import DataLoader
from src.anonymizer import Anonymizer
from src.orchestrator import LLMOrchestrator

st.set_page_config(page_title="Survey Analyzer", layout="wide")

st.title("Analiza ankiet otwartych przy użyciu LLM")

uploaded_file = st.sidebar.file_uploader("Wgraj plik z ankietami (.csv, .xlsx)", type=["csv", "xlsx"])
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