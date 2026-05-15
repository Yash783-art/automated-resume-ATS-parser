import spacy
from spacy.tokens import DocBin
import json
import os

def annotate_data(input_file: str, output_file: str, model_name: str = "en_core_web_lg"):
    """
    Converts JSONL (text, entities) to spaCy's .spacy binary format.
    JSONL format: {"text": "...", "label": [[start, end, "LABEL"], ...]}
    """
    nlp = spacy.blank("en") # Use blank for training
    db = DocBin()
    
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            text = data["text"]
            labels = data["label"]
            
            doc = nlp.make_doc(text)
            ents = []
            for start, end, label in labels:
                span = doc.char_span(start, end, label=label)
                if span is None:
                    print(f"Skipping entity: {label} in text: {text[start:end]}")
                else:
                    ents.append(span)
            
            doc.ents = ents
            db.add(doc)
            
    db.to_disk(output_file)
    print(f"Saved {len(db)} docs to {output_file}")

if __name__ == "__main__":
    # Example usage:
    # annotate_data("data/train.jsonl", "data/train.spacy")
    pass
