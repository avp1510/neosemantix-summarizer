from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional, Dict

class InputMessage(BaseModel):
    request_id:str
    text:str
    timestamp:datetime

    #to check is the input text has less than 2000 words or not
    @field_validator('text')
    def validate_text_length(cls, value): #cls here is just like self
        if len(value.split()) > 2000:
            raise ValueError('Text must be at most 2000 words long')
        return value

class OutputMessage(BaseModel):
    request_id: str
    summary: str
    entities: Dict[str, str]
    generated_at: datetime = datetime.now()

    @field_validator('summary')
    def validate_summary_length(cls, value):
        if len(value.split()) > 100:
            raise ValueError('Summary must be at most 100 words long')
        return value
        
