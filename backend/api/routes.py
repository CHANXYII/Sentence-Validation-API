from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.schemas import ValidateSentenceRequest, ValidateSentenceResponse
from models.models import PracticeSubmission, Vocabulary
from config.database import get_db
from api.utils import mock_ai_validation
from datetime import datetime

router = APIRouter()


@router.post("/validate-sentence", response_model=ValidateSentenceResponse, status_code=status.HTTP_200_OK)
async def validate_sentence(
    request: ValidateSentenceRequest,
    db: Session = Depends(get_db)
):
    """
    POST endpoint to validate a user's sentence.
    
    Steps:
    1. Receive word_id and sentence from the request
    2. Fetch the vocabulary word from the database
    3. Call mock_ai_validation to get validation results
    4. Save the submission to the database
    5. Return the validation results
    """
    
    # Step 1: Fetch the vocabulary word from database
    vocabulary = db.query(Vocabulary).filter(Vocabulary.id == request.word_id).first()
    
    if not vocabulary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vocabulary word with id {request.word_id} not found"
        )
    
    # Step 2: Call mock AI validation function
    validation_result = mock_ai_validation(
        sentence=request.sentence,
        word=vocabulary.word,
        difficulty_level=vocabulary.difficulty_level
    )
    
    # Step 3: Save the practice submission to database
    new_submission = PracticeSubmission(
        user_id=1,
        word_id=request.word_id,
        submitted_sentence=request.sentence,
        score=validation_result["score"],
        corrected_sentence=validation_result["corrected_sentence"],
        suggestion=validation_result["suggestion"],
        timestamp=datetime.utcnow()
    )
    
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    
    # Step 4: Return the validation response
    return ValidateSentenceResponse(
        score=validation_result["score"],
        level=validation_result["level"],
        suggestion=validation_result["suggestion"],
        corrected_sentence=validation_result["corrected_sentence"]
    )


@router.get("/vocabulary/{word_id}")
async def get_vocabulary(word_id: int, db: Session = Depends(get_db)):
    """
    GET endpoint to retrieve a vocabulary word by ID.
    Useful for testing and debugging.
    """
    vocabulary = db.query(Vocabulary).filter(Vocabulary.id == word_id).first()
    
    if not vocabulary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vocabulary word with id {word_id} not found"
        )
    
    return {
        "id": vocabulary.id,
        "word": vocabulary.word,
        "definition": vocabulary.definition,
        "difficulty_level": vocabulary.difficulty_level
    }


@router.get("/submissions")
async def get_all_submissions(db: Session = Depends(get_db)):
    """
    GET endpoint to retrieve all practice submissions.
    Useful for viewing submission history.
    """
    submissions = db.query(PracticeSubmission).order_by(PracticeSubmission.timestamp.desc()).all()
    
    return {
        "total": len(submissions),
        "submissions": [
            {
                "id": sub.id,
                "user_id": sub.user_id,
                "word_id": sub.word_id,
                "submitted_sentence": sub.submitted_sentence,
                "score": sub.score,
                "timestamp": sub.timestamp
            }
            for sub in submissions
        ]
    }
