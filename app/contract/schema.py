from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional, Dict

class InputMessage(BaseModel):
    request_id:str
    user_id: Optional[str]
    message: str
    request_time: datetime

    #to check is the input text has less than 2000 words or not
    @field_validator('message')
    def validate_message_length(cls, value):
        if len(value.split()) > 2000:
            raise ValueError('Message must be at most 2000 words long')
        return value

class OutputMessage(BaseModel):
    request_id: str
    user_id: Optional[str]
    summary: str
    entities: Dict[str, str]
    request_time: datetime
    response_time: datetime = datetime.now()

    @field_validator('summary')
    def validate_summary_length(cls, value):
        if len(value.split()) > 100:
            raise ValueError('Summary must be at most 100 words long')
        return value
        
