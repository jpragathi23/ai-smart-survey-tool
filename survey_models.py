# backend/app/models/survey_models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

# ------------------
# Survey Table
# ------------------
class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    survey_type = Column(String(50))  # custom, nss, ai_generated
    nss_template_type = Column(String(50), nullable=True)
    languages = Column(JSON, default=["en"])
    adaptive_enabled = Column(Boolean, default=True)
    voice_enabled = Column(Boolean, default=False)
    status = Column(String(50), default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship("Question", back_populates="survey", cascade="all, delete-orphan")

# ------------------
# Question Table
# ------------------
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"))
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
    responses = relationship("Response", back_populates="question", cascade="all, delete-orphan")

# ------------------
# Response Table
# ------------------
class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    respondent_id = Column(String(100), nullable=False)
    answer = Column(JSON)
    confidence_score = Column(Integer, default=100)
    validation_status = Column(String(50), default="pending")
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    question = relationship("Question", back_populates="responses")
