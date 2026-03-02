1.1 Opis projektu
Problem biznesowy (np. analiza anonimowych wyników ankiet pracowniczych)
Cel (automatyczna agregacja, anonimizacja, NLP, dashboard)
Dla kogo (HR, managerowie, leadership)


1.2 Architektura

[CSV / Excel]
      ↓
DataLoader
      ↓
Cleaning / Validation
      ↓
Analytics / NLP
      ↓
Streamlit UI

1.3 Stack
Python 3.x
pandas
streamlit
scikit-learn / spaCy (jeśli NLP)
matplotlib / plotly

1.4 Jak uruchomić
git clone ...
cd survey_analytics
python -m venv venv
pip install -r requirements.txt
streamlit run app.py

Dodatkowo - jeśli chcemy wykorzystać klasyfikator korzystający z LLM - nalezy podac swoj Google API Key.


References

https://github.com/poleval/2024-emotion-recognition/tree/main
https://github.com/allegro/klejbenchmark-allegroreviews

@inproceedings{rybak-etal-2020-klej,
    title = "{KLEJ}: Comprehensive Benchmark for Polish Language Understanding",
    author = "Rybak, Piotr and Mroczkowski, Robert and Tracz, Janusz and Gawlik, Ireneusz",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.111",
    pages = "1191--1201",
}