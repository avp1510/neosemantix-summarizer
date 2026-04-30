# app/engine/llm_client.py
import os
from groq import Groq
from .api import GROQ_API_KEY

class SummarizationService:
    def __init__(self, api_key: str = GROQ_API_KEY):
        self.client = Groq(api_key=api_key)
        self.prompt_path = "app/data/system_prompt.txt"

    def _load_system_instructions(self) -> str:
        if not os.path.exists(self.prompt_path):
            return "You are an expert editor. Summarize the following text in strictly less than 100 words, incorporating the provided entities."
        
        with open(self.prompt_path, 'r') as f:
            return f.read()

    def get_summary(self, text: str, entities: dict) -> str:
        """
        Connects to Groq API to get a summary of the text.
        """
        system_instructions = self._load_system_instructions()
        
        entity_list = ", ".join(entities.keys())
        user_message = f"Entities to include: {entity_list}\n\nText to summarize: {text}"

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_instructions
                    },
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=300,
                temperature=0.4,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error retrieving summary from Groq: {str(e)}"
