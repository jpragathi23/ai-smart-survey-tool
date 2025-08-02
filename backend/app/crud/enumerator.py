from sqlalchemy.orm import Session
from app.models.enumerator import EnumeratorAssignment
from app.schemas import EnumeratorAssignmentCreate

def assign_enumerator(db: Session, assignment: EnumeratorAssignmentCreate):
    db_assign = EnumeratorAssignment(
        enumerator_id=assignment.enumerator_id,
        survey_id=assignment.survey_id,
    )
    db.add(db_assign)
    db.commit()
    db.refresh(db_assign)
    return db_assign

def list_assignments(db: Session, enumerator_id: int = None):
    query = db.query(EnumeratorAssignment)
    if enumerator_id:
        query = query.filter(EnumeratorAssignment.enumerator_id == enumerator_id)
    return query.all()
