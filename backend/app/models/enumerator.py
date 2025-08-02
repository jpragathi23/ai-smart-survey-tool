from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class EnumeratorAssignment(Base):
    __tablename__ = "enumerator_assignments"

    id = Column(Integer, primary_key=True, index=True)
    enumerator_id = Column(Integer, ForeignKey("users.id"))
    survey_id = Column(Integer, ForeignKey("surveys.id"))

    enumerator = relationship("User")
    survey = relationship("Survey")




