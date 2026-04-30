
from app.messaging.messenger import MessageBroker
from app.contract.schema import InputMessage, OutputMessage
from app.engine.nlp_worker import SpacyProcessor
from app.engine.llm_client import SummarizationService
from dotenv import load_dotenv
load_dotenv()

def main():
    broker = MessageBroker() 
    nlp_engine = SpacyProcessor()
    llm_service = SummarizationService()

    raw_json_data = broker.get_message_from_producer()
    
    if raw_json_data:
        try:
           
            # Fetch inputs here from Kafka

            input_obj = InputMessage(
                request_id = raw_json_data["request_id"],
                text = raw_json_data["text"],
                timestamp = raw_json_data["timestamp"],
            )
            # Added input to input object to mimic a kafka topic message

            results = nlp_engine.process_text(input_obj.text)
            # This result has preprocessed text and entities
            

            print(f"\n--- NLP Results for {input_obj.request_id} ---")
            print(f"1. Entities Found: {len(results['entities'])}")
            print(f"2. First Five Entities: {list(results['entities'].items())[:5]}")
            print(f"3. Compressed Text: {results['compressed_payload'][:100]}...")

            # Get Summary from LLM
            print("\nGenerating Summary from Groq...")
            summary = llm_service.get_summary(results['compressed_payload'], results['entities'])
            
            print(f"\n--- Final Summary ---")
            print(summary)

            #Create Output Object (Standardizing the result)
            output_obj = OutputMessage(
                request_id=input_obj.request_id,
                summary=summary,
                entities=results['entities']
            )
            
            print(f"\n--- Output Contract Validated ---")
            print(f"Generated At: {output_obj.generated_at}")
            
        except Exception as e:
            print(f"Contract Violation: {e}")

if __name__ == "__main__":
    main()