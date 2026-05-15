from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    clerk_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resumes = relationship("Resume", back_populates="user")
    job_descriptions = relationship("JobDescription", back_populates="user")

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.clerk_id"))
    filename = Column(String)
    r2_key = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    status = Column(String, default="queued") # queued, processing, parsed, failed

    user = relationship("User", back_populates="resumes")
    parsed_resume = relationship("ParsedResume", back_populates="resume", uselist=False)
    match_results = relationship("MatchResult", back_populates="resume")

class ParsedResume(Base):
    __tablename__ = "parsed_resumes"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    raw_text = Column(Text)
    structured_json = Column(JSON)
    parsed_at = Column(DateTime(timezone=True), server_default=func.now())
    confidence_score = Column(Float)

    resume = relationship("Resume", back_populates="parsed_resume")

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.clerk_id"))
    title = Column(String)
    content = Column(Text)
    extracted_keywords_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_template = Column(Boolean, default=False)

    user = relationship("User", back_populates="job_descriptions")
    match_results = relationship("MatchResult", back_populates="jd")

class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    jd_id = Column(Integer, ForeignKey("job_descriptions.id"))
    overall_score = Column(Float)
    skills_score = Column(Float)
    experience_score = Column(Float)
    education_score = Column(Float)
    matched_keywords = Column(JSON) # List of matched keywords
    missing_keywords = Column(JSON) # List of missing keywords
    profession_mismatch = Column(Boolean, default=False)
    scored_at = Column(DateTime(timezone=True), server_default=func.now())

    resume = relationship("Resume", back_populates="match_results")
    jd = relationship("JobDescription", back_populates="match_results")
