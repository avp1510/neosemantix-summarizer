from abc import ABC, abstractmethod

class INLPProcessor(ABC):
    @abstractmethod
    def process_message(self, message: str) -> dict:
        # Takes a message string and returns a dict of processing results (entities, compressed payload, etc.)
        pass