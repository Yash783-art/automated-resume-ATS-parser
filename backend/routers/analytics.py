from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models import Resume, MatchResult, User
from backend.auth import get_current_user

router = APIRouter()

@router.get("/stats")
async def get_analytics_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Total Resumes
    total_resumes = db.query(Resume).filter(Resume.user_id == current_user.clerk_id).count()
    
    # Average Score
    avg_score = db.query(func.avg(MatchResult.overall_score)).join(Resume).filter(Resume.user_id == current_user.clerk_id).scalar() or 0
    
    # Recent Activity
    parsed_count = db.query(Resume).filter(Resume.user_id == current_user.clerk_id, Resume.status == "parsed").count()
    
    return {
        "total_candidates": total_resumes,
        "average_match_score": round(float(avg_score), 1),
        "parsing_success_rate": round((parsed_count / total_resumes * 100) if total_resumes > 0 else 0, 1),
        "recent_trends": [] # Placeholder for future chart data
    }
