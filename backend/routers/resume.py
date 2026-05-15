from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta, timezone
import uuid

from backend.database import get_db
from backend.models import Resume, User, MatchResult
from backend.auth import get_current_user
from backend.storage import storage
from backend.schemas import ResumeUploadResponse, ResumeStatusResponse
from backend.tasks.celery_app import celery_app

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    # 2. Validate file size (simplified check)
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit.")
    
    # 3. Generate R2 key
    file_id = str(uuid.uuid4())
    r2_key = f"resumes/{current_user.clerk_id}/{file_id}.pdf"
    
    # 4. Upload to R2
    storage.upload_file(contents, r2_key)
    
    # 5. Create DB record
    expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    resume = Resume(
        user_id=current_user.clerk_id,
        filename=file.filename,
        r2_key=r2_key,
        expires_at=expires_at,
        status="queued"
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    # 6. Enqueue parsing task
    celery_app.send_task("backend.tasks.parse.parse_resume_task", args=[resume.id])
    
    return {
        "resume_id": resume.id,
        "status": "queued",
        "filename": file.filename
    }

@router.get("/{resume_id}/status", response_model=ResumeStatusResponse)
async def get_resume_status(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id, 
        Resume.user_id == current_user.clerk_id
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")
    
    response = {
        "resume_id": resume.id,
        "status": resume.status
    }
    
    if resume.status == "parsed" and resume.parsed_resume:
        response["parsed_data"] = resume.parsed_resume.structured_json
        
    return response


@router.post("/batch-upload", response_model=list[ResumeUploadResponse])
async def batch_upload_resumes(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files per batch.")
        
    results = []
    for file in files:
        try:
            if not file.filename.lower().endswith(".pdf"):
                continue
            
            contents = await file.read()
            if len(contents) > MAX_FILE_SIZE:
                continue
                
            file_id = str(uuid.uuid4())
            r2_key = f"resumes/{current_user.clerk_id}/{file_id}.pdf"
            storage.upload_file(contents, r2_key)
            
            expires_at = datetime.now(timezone.utc) + timedelta(days=30)
            resume = Resume(
                user_id=current_user.clerk_id,
                filename=file.filename,
                r2_key=r2_key,
                expires_at=expires_at,
                status="queued"
            )
            db.add(resume)
            db.commit()
            db.refresh(resume)
            
            celery_app.send_task("backend.tasks.parse.parse_resume_task", args=[resume.id])
            
            results.append({
                "resume_id": resume.id,
                "status": "queued",
                "filename": file.filename
            })
        except Exception:
            continue
            
    return results
@router.get("/list")
async def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resumes = db.query(Resume).options(joinedload(Resume.match_results).joinedload(MatchResult.jd)).filter(Resume.user_id == current_user.clerk_id).order_by(Resume.created_at.desc()).all()
    
    # Enrich with basic match data for the list view
    results = []
    for r in resumes:
        best_match = None
        if r.match_results:
            # Get the highest score match for this resume
            best_match = max(r.match_results, key=lambda m: m.overall_score)
            
        results.append({
            "id": r.id,
            "filename": r.filename,
            "status": r.status,
            "created_at": r.created_at,
            "candidate_name": r.parsed_resume.structured_json.get("contact", {}).get("name") if r.parsed_resume else None,
            "best_score": round(best_match.overall_score, 1) if best_match else None,
            "best_job_title": best_match.jd.title if best_match else None,
            "profession_mismatch": best_match.profession_mismatch if best_match else False
        })
        
    return results
@router.get("/{resume_id}/details")
async def get_resume_details(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).options(joinedload(Resume.match_results).joinedload(MatchResult.jd)).filter(
        Resume.id == resume_id, 
        Resume.user_id == current_user.clerk_id
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")
    
    # Get the latest match result for this resume if it exists
    best_match = None
    if resume.match_results:
        best_match = max(resume.match_results, key=lambda m: m.overall_score)

    return {
        "id": resume.id,
        "filename": resume.filename,
        "status": resume.status,
        "created_at": resume.created_at,
        "parsed_data": resume.parsed_resume.structured_json if resume.parsed_resume else None,
        "overall_score": best_match.overall_score if best_match else 0,
        "match_id": best_match.id if best_match else None,
        "best_job_title": best_match.jd.title if best_match else None,
        "skills_score": best_match.skills_score if best_match else 0,
        "experience_score": best_match.experience_score if best_match else 0,
        "education_score": best_match.education_score if best_match else 0,
        "matched_skills": best_match.matched_keywords if best_match else [],
        "missing_skills": best_match.missing_keywords if best_match else [],
        "profession_mismatch": best_match.profession_mismatch if best_match else False
    }
