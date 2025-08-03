from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
    DateTime,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base  # relative import
from .question import Question  # relative import

class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    survey_type = Column(String(50))  # custom, nss, ai_generated
    nss_template_type = Column(String(50), nullable=True)
    languages = Column(JSON, default=lambda: ["en"])  # safer default
    adaptive_enabled = Column(Boolean, default=True)
    voice_enabled = Column(Boolean, default=False)
    status = Column(String(50), default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    creator = relationship("User", foreign_keys=[created_by])

    questions = relationship(
        "Question",
        back_populates="survey",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
