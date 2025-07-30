# backend/app/services/analytics_service.py

from sqlalchemy.orm import Session
from app.models import survey_models
from app.schemas import AdaptiveQuestionResponse

# -------------------------------
# AI/Heuristic Adaptive Logic
# -------------------------------
def get_next_adaptive_question(survey_id: int, respondent_id: str, language: str, db: Session):
    try:
        # Fetch all questions for the survey, sorted by order
        all_questions = db.query(survey_models.Question)
            .filter(survey_models.Question.survey_id == survey_id)
            .order_by(survey_models.Question.order_index)
            .all()

        # Fetch already answered question IDs
        answered_qs = db.query(survey_models.Response.question_id)
            .filter(
                survey_models.Response.survey_id == survey_id,
                survey_models.Response.respondent_id == respondent_id
            ).all()
        answered_ids = set([q[0] for q in answered_qs])

        # Find the next unanswered question
        for q in all_questions:
            if q.id not in answered_ids:
                # Choose language-specific version if exists
                translated_text = q.translations.get(language, q.question_text)
                return AdaptiveQuestionResponse(
                    question_id=q.id,
                    question_text=translated_text,
                    question_type=q.question_type,
                    options=q.options,
                    order_index=q.order_index,
                    is_mandatory=q.is_mandatory
                )

        return None  # All questions answered

    except Exception as e:
        raise Exception(f"Adaptive question fetch failed: {str(e)}")
