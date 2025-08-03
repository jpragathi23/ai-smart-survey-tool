from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base

class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    respondent_id = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    answer = Column(JSON)
    confidence_score = Column(Integer, default=100)
    validation_status = Column(String(50), default="pending")
    extra_metadata = Column(JSON, default=lambda: {})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    question = relationship("Question", back_populates="responses")
    user = relationship("User", foreign_keys=[user_id])
