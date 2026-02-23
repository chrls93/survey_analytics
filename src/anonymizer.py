import spacy

class Anonymizer:
    def __init__(self):
        self.nlp = spacy.load("pl_core_news_md")

    def mask_pii(self, text: str) -> str:
        doc = self.nlp(text)
        anonymized_text = text
        for ent in reversed(doc.ents):
            if ent.label_ in ["persName", "placeName", "orgName"]:
                anonymized_text = anonymized_text[:ent.start_char] + f"[{ent.label_}]" + anonymized_text[ent.end_char:]
        return anonymized_text