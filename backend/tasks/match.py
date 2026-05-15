from backend.tasks.celery_app import celery_app
from backend.database import SessionLocal
from backend.models import Resume, JobDescription, MatchResult
from backend.scoring.match_engine import calculate_match

@celery_app.task(name="backend.tasks.match.match_resume_to_all_jds_task")
def match_resume_to_all_jds_task(resume_id: int):
    """
    Matches a specific resume against all JDs for the same user.
    """
    db = SessionLocal()
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume or not resume.parsed_resume:
            return f"Resume {resume_id} not ready for matching"
            
        # Find all JDs for this user
        jds = db.query(JobDescription).filter(JobDescription.user_id == resume.user_id).all()
        
        for jd in jds:
            # Check if match already exists
            existing = db.query(MatchResult).filter(
                MatchResult.resume_id == resume.id,
                MatchResult.jd_id == jd.id
            ).first()
            
            # Run match engine
            score_data = calculate_match(
                resume.parsed_resume.structured_json, 
                jd.extracted_keywords_json
            )
            
            if existing:
                # Update existing
                for key, value in score_data.items():
                    setattr(existing, key, value)
            else:
                # Create new
                match_result = MatchResult(
                    resume_id=resume.id,
                    jd_id=jd.id,
                    **score_data
                )
                db.add(match_result)
        
        db.commit()
        return f"Successfully matched resume {resume_id} against {len(jds)} JDs"
        
    except Exception as e:
        print(f"Error in match_resume_to_all_jds_task: {e}")
        db.rollback()
        raise e
    finally:
        db.close()
