from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    JSON,
    Boolean,
)
from sqlalchemy.orm import relationship
from app.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id", ondelete="CASCADE"))
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="text")  # text, radio, checkbox
    options = Column(JSON, default=[])
    validation_rules = Column(JSON, default={})
    order_index = Column(Integer, default=0)
    is_mandatory = Column(Boolean, default=False)
    translations = Column(JSON, default={})
    nss_code = Column(String(50), nullable=True)
    lgd_location_type = Column(String(50), nullable=True)

    survey = relationship("Survey", back_populates="questions")
    responses = relationship(
        "Response", back_populates="question", cascade="all, delete-orphan", passive_deletes=True
    )
