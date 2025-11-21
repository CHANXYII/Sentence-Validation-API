from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from datetime import datetime
from config.database import Base


class Vocabulary(Base):
    """Model for vocabulary words table"""
    __tablename__ = "vocabulary"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), nullable=False, unique=True)
    definition = Column(Text, nullable=True)
    difficulty_level = Column(String(50), nullable=False, default="Beginner")  # Beginner, Intermediate, Advanced
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Vocabulary(id={self.id}, word={self.word}, difficulty_level={self.difficulty_level})>"


class PracticeSubmission(Base):
    """Model for practice submissions table"""
    __tablename__ = "practice_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, default=1)
    word_id = Column(Integer, nullable=False)
    submitted_sentence = Column(Text, nullable=False)
    score = Column(Float, nullable=False)
    corrected_sentence = Column(Text, nullable=True)
    suggestion = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PracticeSubmission(id={self.id}, word_id={self.word_id}, score={self.score})>"
