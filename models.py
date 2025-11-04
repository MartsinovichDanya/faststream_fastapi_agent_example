from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    msg: str

class ChatResponse(BaseModel):
    req_id: str

class CheckRequest(BaseModel):
    req_id: str

class CheckResponse(BaseModel):
    req_id: str
    status: str
    result: Optional[str] = None

class Message(BaseModel):
    req_id: str
    text: str
