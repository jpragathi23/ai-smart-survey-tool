# backend/app/routes/response_routes.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SubmitResponseRequest, SubmitResponseResult
from app.models import survey_models
from app.services import validation_service

router = APIRouter()

# ---------------------------
# Submit a Survey Response
# ---------------------------
@router.post("/submit", response_model=SubmitResponseResult)
def submit_response(payload: SubmitResponseRequest, db: Session = Depends(get_db)):
    try:
        # Fetch question for context
        question = db.query(survey_models.Question).filter_by(id=payload.question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Validate answer (real-time validation)
        validation_status, confidence = validation_service.validate_answer(
            question=question,
            answer=payload.answer
        )

        # Store response
        response = survey_models.Response(
            survey_id=payload.survey_id,
            question_id=payload.question_id,
            respondent_id=payload.respondent_id,
            answer=payload.answer,
            confidence_score=confidence,
            validation_status=validation_status,
            metadata=payload.metadata
        )
        db.add(response)
        db.commit()

        return SubmitResponseResult(
            status="success",
            message="Response saved",
            confidence_score=confidence,
            validation_status=validation_status
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Response submission failed: {str(e)}")
