from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import get_db
from backend.models import Resume, JobDescription, MatchResult, User
from backend.auth import get_current_user
from backend.scoring.match_engine import calculate_match
from backend.schemas import MatchRequest, MatchResponse, BatchMatchRequest, BatchMatchResponse

router = APIRouter()

@router.post("/", response_model=MatchResponse)
async def match_resume_to_jd(
    req: MatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Fetch Resume and JD
    resume = db.query(Resume).filter(
        Resume.id == req.resume_id, 
        Resume.user_id == current_user.clerk_id
    ).first()
    jd = db.query(JobDescription).filter(
        JobDescription.id == req.jd_id, 
        JobDescription.user_id == current_user.clerk_id
    ).first()
    
    if not resume or not jd:
        raise HTTPException(status_code=404, detail="Resume or Job Description not found.")
    
    if resume.status != "parsed":
        raise HTTPException(status_code=400, detail=f"Resume is in state '{resume.status}'. Must be 'parsed' before matching.")

    # 2. Run match engine
    score_data = calculate_match(resume.parsed_resume.structured_json, jd.extracted_keywords_json)
    
    # 3. Save MatchResult
    match_result = MatchResult(
        resume_id=resume.id,
        jd_id=jd.id,
        overall_score=score_data["overall_score"],
        skills_score=score_data["skills_score"],
        experience_score=score_data["experience_score"],
        education_score=score_data["education_score"],
        matched_keywords=score_data["matched_keywords"],
        missing_keywords=score_data["missing_keywords"]
    )
    db.add(match_result)
    db.commit()
    db.refresh(match_result)
    
    return {
        "match_id": match_result.id,
        **score_data,
        "scored_at": match_result.scored_at
    }

@router.post("/batch", response_model=BatchMatchResponse)
async def batch_match(
    req: BatchMatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = []
    for resume_id in req.resume_ids:
        try:
            # Re-use logic or call internal function
            # For simplicity, we just repeat here but in production we'd DRY this
            resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.clerk_id).first()
            jd = db.query(JobDescription).filter(JobDescription.id == req.jd_id, JobDescription.user_id == current_user.clerk_id).first()
            
            if resume and jd and resume.status == "parsed":
                score_data = calculate_match(resume.parsed_resume.structured_json, jd.extracted_keywords_json)
                match_result = MatchResult(
                    resume_id=resume.id,
                    jd_id=jd.id,
                    **score_data
                )
                db.add(match_result)
                results.append({
                    "match_id": 0, # Placeholder if not saved yet
                    **score_data,
                    "scored_at": datetime.now()
                })
        except Exception:
            continue
            
    db.commit()
    return {"results": results}
