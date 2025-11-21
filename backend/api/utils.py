import random
from typing import Tuple


def mock_ai_validation(sentence: str, word: str, difficulty_level: str) -> dict:
    """
    Mock AI validation function that simulates sentence validation.
    
    Args:
        sentence: The sentence submitted by the user
        word: The vocabulary word that should be used in the sentence
        difficulty_level: The difficulty level of the word (Beginner, Intermediate, Advanced)
    
    Returns:
        Dictionary containing score, suggestion, and corrected_sentence
    """
    
    # Check if the word is in the sentence
    word_in_sentence = word.lower() in sentence.lower()
    
    # Base score calculation
    if not word_in_sentence:
        score = random.uniform(20, 40)
        suggestion = f"The word '{word}' is not found in your sentence. Please use it correctly."
        corrected_sentence = f"Try using '{word}' in your sentence."
        return {
            "score": round(score, 2),
            "level": difficulty_level,
            "suggestion": suggestion,
            "corrected_sentence": corrected_sentence
        }
    
    # Calculate score based on difficulty level and sentence length
    sentence_length = len(sentence.split())
    
    if difficulty_level == "Beginner":
        # Beginner: Simple sentences (5-10 words)
        if 5 <= sentence_length <= 10:
            score = random.uniform(80, 95)
            suggestion = "Great job! Your sentence is clear and simple."
        elif sentence_length < 5:
            score = random.uniform(60, 75)
            suggestion = "Good start! Try to make your sentence a bit longer and more descriptive."
        else:
            score = random.uniform(70, 85)
            suggestion = "Good work! For beginner level, try to keep sentences simpler."
    
    elif difficulty_level == "Intermediate":
        # Intermediate: More complex sentences (8-15 words)
        if 8 <= sentence_length <= 15:
            score = random.uniform(85, 95)
            suggestion = "Excellent! Your sentence shows good complexity and proper word usage."
        elif sentence_length < 8:
            score = random.uniform(65, 80)
            suggestion = "Good job! Try adding more detail to match the intermediate level."
        else:
            score = random.uniform(75, 90)
            suggestion = "Well done! Just be careful not to make the sentence too complex."
    
    else:
        # Advanced: Complex sentences (12+ words)
        if sentence_length >= 12:
            score = random.uniform(85, 98)
            suggestion = "Outstanding! Your sentence demonstrates advanced language proficiency."
        elif sentence_length >= 8:
            score = random.uniform(70, 85)
            suggestion = "Good effort! For advanced level, try to create more sophisticated sentences."
        else:
            score = random.uniform(60, 75)
            suggestion = "Nice try! Advanced level requires more complex sentence structures."
    
    # Add small random variation for minor grammar corrections
    has_minor_correction = random.choice([True, False])
    if has_minor_correction and score > 70:
        corrected_sentence = sentence.capitalize()
        if not corrected_sentence.endswith('.'):
            corrected_sentence += '.'
        suggestion += " Just a minor correction needed."
    else:
        corrected_sentence = sentence
    
    return {
        "score": round(score, 2),
        "level": difficulty_level,
        "suggestion": suggestion,
        "corrected_sentence": corrected_sentence
    }


def calculate_score(sentence: str, word: str) -> float:
    """
    Helper function to calculate a score based on sentence quality.
    This is a simplified version for demonstration.
    """
    score = 50.0
    
    # Word usage check
    if word.lower() in sentence.lower():
        score += 30
    
    # Length check
    word_count = len(sentence.split())
    if word_count >= 5:
        score += min(20, word_count * 2)
    
    return min(100.0, score)
