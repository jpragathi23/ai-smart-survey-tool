# backend/app/routes/response_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Response
from app.schemas import SubmitResponseRequest, SubmitResponseResult

router = APIRouter(prefix="/responses", tags=["Responses"])


@router.post("/submit", response_model=SubmitResponseResult)
def submit_response(payload: SubmitResponseRequest, db: Session = Depends(get_db)):
    try:
        # Check if this respondent already answered this question
        existing = (
            db.query(Response)
            .filter(
                Response.survey_id == payload.survey_id,
                Response.question_id == payload.question_id,
                Response.respondent_id == payload.respondent_id,
            )
            .first()
        )

        if existing:
            # Update the existing answer
            existing.answer = payload.answer
            existing.confidence_score = payload.confidence_score
            existing.validation_status = payload.validation_status
            existing.extra_metadata = payload.extra_metadata or {}
            db.commit()
            db.refresh(existing)

            return SubmitResponseResult(
                response_id=existing.id,
                survey_id=existing.survey_id,
                question_id=existing.question_id,
                respondent_id=existing.respondent_id,
                validation_status=existing.validation_status,
                message="Response updated successfully",
            )

        # Create a new response record
        new_response = Response(
            survey_id=payload.survey_id,
            question_id=payload.question_id,
            respondent_id=payload.respondent_id,
            answer=payload.answer,
            confidence_score=payload.confidence_score,
            validation_status=payload.validation_status,
            extra_metadata=payload.extra_metadata or {},
        )
        db.add(new_response)
        db.commit()
        db.refresh(new_response)

        return SubmitResponseResult(
            response_id=new_response.id,
            survey_id=new_response.survey_id,
            question_id=new_response.question_id,
            respondent_id=new_response.respondent_id,
            validation_status=new_response.validation_status,
            message="Response submitted successfully",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting response: {str(e)}")
