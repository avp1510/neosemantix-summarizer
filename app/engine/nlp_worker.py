import spacy
from app.contract.interface import INLPProcessor

class SpacyProcessor(INLPProcessor):
    def __init__(self, model_name="en_core_web_trf"):
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            # Fallback to a CPU optimized model
            self.nlp = spacy.load("en_core_web_sm")

    def process_message(self, message: str) -> dict:
        doc = self.nlp(message)
        
        
        # Extract entities
        entity_map = {ent.text: ent.label_ for ent in doc.ents}
        
        # Filter Tokens to reduce LLM costs
        # though of removing stopwords and punctuation but that might 
        # hamper language understanding so just removed white space here
        filtered_tokens = [
            token.text.lower() for token in doc 
            if not token.is_space
        ]
    
    
        # Rejoin into a "Compressed" string
        compressed_text = " ".join(filtered_tokens)
    
        return {
            "entities": entity_map,
            "compressed_payload": compressed_text
        }