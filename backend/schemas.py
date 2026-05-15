from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# ─── Auth ───
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    clerk_id: str

class UserSchema(UserBase):
    clerk_id: str
    created_at: datetime
    class Config:
        from_attributes = True

# ─── Resume ───
class ResumeUploadResponse(BaseModel):
    resume_id: int
    status: str
    filename: str

class ResumeStatusResponse(BaseModel):
    resume_id: int
    status: str
    parsed_data: Optional[Dict[str, Any]] = None

# ─── Job Description ───
class JDCreate(BaseModel):
    content: str
    title: Optional[str] = "Untitled Position"
    is_template: bool = False

class JDResponse(BaseModel):
    jd_id: int
    title: str
    extracted_keywords: List[str]

# ─── Match ───
class MatchRequest(BaseModel):
    resume_id: int
    jd_id: int

class MatchResponse(BaseModel):
    match_id: int
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    scored_at: datetime

# ─── Batch ───
class BatchUploadResponse(BaseModel):
    results: List[ResumeUploadResponse]

class BatchMatchRequest(BaseModel):
    resume_ids: List[int]
    jd_id: int

class BatchMatchResponse(BaseModel):
    results: List[MatchResponse]
