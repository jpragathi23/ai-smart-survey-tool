# backend/app/routes/analytics_routes.py

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services import analytics_service

router = APIRouter()

@router.get("/survey/{survey_id}")
def get_survey_analytics(
    survey_id: int,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        # Currently the service ignores date filters; extend if needed
        analytics = analytics_service.generate_survey_analytics(survey_id, db)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")
