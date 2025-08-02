from sqlalchemy.orm import Session
from app.models.response import Response
from app.schemas import ResponseCreate

def create_response(db: Session, resp: ResponseCreate):
    db_resp = Response(
        question_id=resp.question_id,
        user_id=resp.user_id,
        respondent_id=getattr(resp, "respondent_id", ""),
        answer=resp.answer,
    )
    db.add(db_resp)
    db.commit()
    db.refresh(db_resp)
    return db_resp

def list_responses_for_survey(db: Session, survey_id: int):
    return db.query(Response).filter(Response.survey_id == survey_id).all()
