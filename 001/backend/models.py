from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: str
    email: str
    is_premium: bool
    created_at: datetime

class Quiz(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: Optional[str]

class MindMapNode(BaseModel):
    id: str
    label: str
    children: List[str]
    parent: Optional[str]

class Summary(BaseModel):
    content: str
    key_points: List[str]
    created_at: datetime

class ContentRequest(BaseModel):
    content: str
    type: str  # summary, quiz, mindmap, audio
    language: Optional[str] = "fr" 