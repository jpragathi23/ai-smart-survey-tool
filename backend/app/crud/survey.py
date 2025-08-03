from sqlalchemy.orm import Session
from app.models.survey import Survey

from app.schemas import SurveyCreate

def create_survey(db: Session, survey: SurveyCreate):
    db_survey = Survey(
        title=survey.title,
        description=survey.description,
        created_by=survey.created_by,
        survey_type=getattr(survey, "survey_type", None),
    )
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey

def get_survey(db: Session, survey_id: int):
    return db.query(Survey).filter(Survey.id == survey_id).first()

def list_surveys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Survey).offset(skip).limit(limit).all()
