from abc import ABC, abstractmethod

class INLPProcessor(ABC):
    @abstractmethod
    def process_text(self, text: str) -> dict:
        """
        Takes a string and returns a dict depending on what you want to return since this is an abstract class
        """
        pass