from sqlalchemy.orm import Session
from app.models import Survey, Question, Response

def generate_survey_analytics(survey_id: int, db: Session):
    # Fetch total questions
    total_questions = db.query(Question).filter(Question.survey_id == survey_id).count()

    # Fetch total responses
    total_responses = db.query(Response).filter(Response.survey_id == survey_id).count()

    # Completion rate (roughly, assuming all respondents answer all questions)
    completion_rate = 0
    if total_questions > 0:
        completion_rate = round((total_responses / total_questions) * 100, 2)

    # Group responses by question
    question_stats = []
    questions = db.query(Question).filter(Question.survey_id == survey_id).all()
    for q in questions:
        answers = db.query(Response).filter(Response.question_id == q.id).count()
        question_stats.append({
            "question_id": q.id,
            "question_text": q.question_text,
            "total_answers": answers
        })

    return {
        "survey_id": survey_id,
        "total_questions": total_questions,
        "total_responses": total_responses,
        "completion_rate": completion_rate,
        "questions": question_stats
    }
