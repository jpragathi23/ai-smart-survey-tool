from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.survey import Survey
from ..models.question import Question
from ..models.response import Response
from ..schemas import SurveyCreateRequest, SurveyResponse, AdaptiveQuestionResponse
from ..services import nss_service, llm_service, analytics_service

router = APIRouter()

# -----------------------------------------
# Create Survey (Custom, NSS, AI-Generated)
# -----------------------------------------
@router.post("/create", response_model=SurveyResponse)
def create_survey(payload: SurveyCreateRequest, db: Session = Depends(get_db)):
    try:
        new_survey = Survey(
            title=payload.title,
            description=payload.description,
            survey_type=payload.survey_type,
            nss_template_type=payload.nss_template_type,
            languages=payload.languages,
            adaptive_enabled=payload.adaptive_enabled,
            voice_enabled=payload.voice_enabled,
            status=payload.status or "draft"
        )
        db.add(new_survey)
        db.commit()
        db.refresh(new_survey)

        # Auto-add questions from NSS template
        if payload.survey_type == "nss" and payload.nss_template_type:
            nss_questions = nss_service.get_questions_from_template(payload.nss_template_type)
            for q in nss_questions:
                question = Question(
                    survey_id=new_survey.id,
                    question_text=q["question_text"],
                    question_type=q.get("question_type", "text"),
                    options=q.get("options", []),
                    validation_rules=q.get("validation_rules", {}),
                    nss_code=q.get("nss_code"),
                    lgd_location_type=q.get("lgd_location_type"),
                    translations=q.get("translations", {}),
                    order_index=q.get("order_index", 0),
                    is_mandatory=q.get("is_mandatory", False)
                )
                db.add(question)
            db.commit()

        return new_survey

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Survey creation failed: {str(e)}")

# ----------------------
# Get Survey by ID
# ----------------------
@router.get("/{survey_id}", response_model=SurveyResponse)
def get_survey(survey_id: int, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

# ------------------------------------------
# Generate Survey from Prompt (AI-Powered)
# ------------------------------------------
@router.post("/generate-from-prompt", response_model=SurveyResponse)
def generate_from_prompt(
    prompt: str,
    num_questions: int = 5,
    survey_title: str = "AI Survey",
    survey_description: str = "Generated using LLM",
    db: Session = Depends(get_db)
):
    try:
        questions = llm_service.generate_questions(prompt, num_questions)

        survey = Survey(
            title=survey_title,
            description=survey_description,
            survey_type="ai_generated",
            languages=["en"],
            adaptive_enabled=True,
            voice_enabled=True,
            status="draft"
        )
        db.add(survey)
        db.commit()
        db.refresh(survey)

        for idx, q in enumerate(questions):
            question = Question(
                survey_id=survey.id,
                question_text=q["text"],
                question_type=q.get("type", "text"),
                options=q.get("options", []),
                order_index=idx + 1,
                is_mandatory=True
            )
            db.add(question)
        db.commit()

        return survey

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"LLM-based survey generation failed: {str(e)}")

# -------------------------------
# Get Next Adaptive Question
# -------------------------------
@router.get("/{survey_id}/adaptive", response_model=AdaptiveQuestionResponse)
def get_next_adaptive_question(
    survey_id: int,
    respondent_id: str = Query(...),
    language: str = Query("en"),
    db: Session = Depends(get_db)
):
    try:
        question = analytics_service.get_next_adaptive_question(survey_id, respondent_id, language, db)
        if question:
            return question
        return {"message": "Survey completed", "completed": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Adaptive logic failed: {str(e)}")

# -------------------------------
# Get Respondent Progress
# -------------------------------
@router.get("/{survey_id}/progress")
def get_survey_progress(survey_id: int, respondent_id: str, db: Session = Depends(get_db)):
    try:
        total = db.query(Question).filter_by(survey_id=survey_id).count()
        answered = db.query(Response).filter_by(survey_id=survey_id, respondent_id=respondent_id).count()
        percent = round((answered / total) * 100, 2) if total > 0 else 0
        return {
            "survey_id": survey_id,
            "respondent_id": respondent_id,
            "answered_questions": answered,
            "total_questions": total,
            "completion_percentage": percent
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching progress: {str(e)}")
