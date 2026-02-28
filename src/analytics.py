from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance

class AnalyticsModule:
    def __init__(self, embedding_model, llm_orchestrator):
        self.llm = llm_orchestrator
        # Konfiguracja BERTopic z HerBERT-em jako bazą
        self.topic_model = BERTopic(
            embedding_model=embedding_model,
            representation_model=KeyBERTInspired() # Wykorzystujemy HerBERTa do słów kluczowych
        )

    def perform_topic_modeling(self, docs):
        """Odkrywanie tematów w ankietach"""
        topics, probs = self.topic_model.fit_transform(docs)
        return topics, self.topic_model.get_topic_info()

    def generate_business_labels(self, topic_info):
        """Post-processing: LLM nadaje nazwy klastrom"""
        labels = {}
        for index, row in topic_info.iterrows():
            if row['Topic'] == -1: continue # Pomijamy szum
            
            keywords = row['Representation']
            # Prompt do LLM (Bielik/Gemini)
            prompt = f"Na podstawie słów kluczowych: {keywords}, wymyśl krótką (max 3 słowa) nazwę kategorii biznesowej."
            labels[row['Topic']] = self.llm.generate(prompt)
            
        return labels