# backend/app/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# -------------------------
# Request: Create Survey
# -------------------------
class SurveyCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    survey_type: str  # custom, nss, ai_generated
    nss_template_type: Optional[str] = None
    languages: List[str] = ["en"]
    adaptive_enabled: bool = True
    voice_enabled: bool = False
    status: Optional[str] = "draft"

# -------------------------
# Response: Survey
# -------------------------
class QuestionSchema(BaseModel):
    id: int
    question_text: str
    question_type: str
    options: Optional[List[str]] = []
    translations: Optional[Dict[str, str]] = {}
    order_index: Optional[int] = 0
    is_mandatory: Optional[bool] = False

    class Config:
        orm_mode = True

class SurveyResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    survey_type: str
    nss_template_type: Optional[str]
    languages: List[str]
    adaptive_enabled: bool
    voice_enabled: bool
    status: str
    created_at: datetime
    questions: List[QuestionSchema] = []

    class Config:
        orm_mode = True

# -------------------------
# Adaptive Question Output
# -------------------------
class AdaptiveQuestionResponse(BaseModel):
    question_id: int
    question_text: str
    question_type: str
    options: Optional[List[str]] = []
    order_index: Optional[int] = 0
    is_mandatory: Optional[bool] = False
    completed: Optional[bool] = False

# -------------------------
# Submit Response
# -------------------------
class SubmitResponseRequest(BaseModel):
    survey_id: int
    question_id: int
    respondent_id: str
    answer: Any
    metadata: Optional[Dict[str, Any]] = {}

class SubmitResponseResult(BaseModel):
    status: str
    message: str
    confidence_score: Optional[int] = None
    validation_status: Optional[str] = None
