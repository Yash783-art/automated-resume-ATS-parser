from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import JobDescription, User
from backend.auth import get_current_user
from backend.nlp.jd_processor import process_jd
from backend.schemas import JDCreate, JDResponse

router = APIRouter()

@router.post("/process", response_model=JDResponse)
async def process_job_description(
    jd_in: JDCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Process JD to extract keywords/requirements
    processed_data = process_jd(jd_in.content)
    processed_data["title"] = jd_in.title
    
    # 2. Save to DB
    jd = JobDescription(
        user_id=current_user.clerk_id,
        title=jd_in.title,
        content=jd_in.content,
        extracted_keywords_json=processed_data,
        is_template=jd_in.is_template
    )
    db.add(jd)
    db.commit()
    db.refresh(jd)
    
    return {
        "jd_id": jd.id,
        "title": jd.title,
        "extracted_keywords": processed_data.get("required_skills", [])
    }

@router.get("/templates", response_model=list[JDResponse])
async def get_jd_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    templates = db.query(JobDescription).filter(
        JobDescription.user_id == current_user.clerk_id,
        JobDescription.is_template == True
    ).all()
    
    return [
        {
            "jd_id": t.id,
            "title": t.title,
            "extracted_keywords": t.extracted_keywords_json.get("required_skills", [])
        } for t in templates
    ]

@router.get("/list", response_model=list[JDResponse])
async def list_jds(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    jds = db.query(JobDescription).filter(
        JobDescription.user_id == current_user.clerk_id
    ).all()
    
    return [
        {
            "jd_id": j.id,
            "title": j.title,
            "extracted_keywords": j.extracted_keywords_json.get("required_skills", []) if j.extracted_keywords_json else []
        } for j in jds
    ]
