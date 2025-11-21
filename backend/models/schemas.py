from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ValidateSentenceRequest(BaseModel):
    """Request model for sentence validation"""
    word_id: int = Field(..., description="ID of the vocabulary word")
    sentence: str = Field(..., min_length=1, description="Sentence submitted by user")
    
    class Config:
        json_schema_extra = {
            "example": {
                "word_id": 1,
                "sentence": "I went to the library to study yesterday."
            }
        }


class ValidateSentenceResponse(BaseModel):
    """Response model for sentence validation"""
    score: float = Field(..., description="Validation score (0-100)")
    level: str = Field(..., description="Difficulty level")
    suggestion: str = Field(..., description="Feedback suggestion")
    corrected_sentence: str = Field(..., description="Corrected version of the sentence")
    
    class Config:
        json_schema_extra = {
            "example": {
                "score": 85.0,
                "level": "Intermediate",
                "suggestion": "Good job! Just a minor correction needed.",
                "corrected_sentence": "I went to the library to study yesterday."
            }
        }


class PracticeSubmissionResponse(BaseModel):
    """Response model for practice submission record"""
    id: int
    user_id: int
    word_id: int
    submitted_sentence: str
    score: float
    timestamp: datetime
    
    class Config:
        from_attributes = True
