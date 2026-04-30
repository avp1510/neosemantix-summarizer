import json
import os

class MessageBroker:
    def get_message_from_producer(self, file_path="app/data/input_text.json"):
        if not os.path.exists(file_path):
            return None

        with open(file_path, 'r') as file:
            # This simulates reading from a Kafka Topic 
            return json.load(file)
