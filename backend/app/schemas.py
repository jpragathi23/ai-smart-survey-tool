# backend/app/schemas.py

from typing import List, Optional, Any
from pydantic import BaseModel


# --------------------------
# Survey Creation
# --------------------------
class SurveyCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    survey_type: str  # custom, nss, ai_generated
    nss_template_type: Optional[str] = None
    languages: List[str] = ["en"]
    adaptive_enabled: bool = True
    voice_enabled: bool = False
    status: Optional[str] = "draft"

    class Config:
        from_attributes = True


class QuestionSchema(BaseModel):
    id: int
    question_text: str
    question_type: str
    options: Optional[List[Any]] = []
    order_index: int
    is_mandatory: bool

    class Config:
        from_attributes = True


class SurveyResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    survey_type: str
    languages: List[str]
    adaptive_enabled: bool
    voice_enabled: bool
    status: str
    questions: List[QuestionSchema] = []

    class Config:
        from_attributes = True


# --------------------------
# Adaptive Question Response
# --------------------------
class AdaptiveQuestionResponse(BaseModel):
    question_id: int
    question_text: str
    question_type: str
    options: List[Any] = []
    order_index: int
    completed: bool = False

    class Config:
        from_attributes = True


# --------------------------
# Submit Response (Request + Result)
# --------------------------
class SubmitResponseRequest(BaseModel):
    survey_id: int
    question_id: int
    respondent_id: str
    answer: Any  # Can be text, choice id, list, dict, etc.
    confidence_score: Optional[int] = 100
    validation_status: Optional[str] = "pending"
    extra_metadata: Optional[dict] = {}

    class Config:
        from_attributes = True


class SubmitResponseResult(BaseModel):
    response_id: int
    survey_id: int
    question_id: int
    respondent_id: str
    validation_status: str
    message: str

    class Config:
        from_attributes = True
