from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.tasks.celery_app import celery_app
from backend.database import SessionLocal
from backend.models import Resume
from backend.storage import storage

@celery_app.task
def cleanup_expired_resumes():
    """
    Periodic task to delete expired resumes from R2 and the database.
    """
    db: Session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        expired_resumes = db.query(Resume).filter(Resume.expires_at < now).all()
        
        for resume in expired_resumes:
            # Delete from R2
            try:
                storage.delete_file(resume.r2_key)
            except Exception as e:
                print(f"Failed to delete {resume.r2_key} from R2: {e}")
            
            # Delete from DB (cascading deletes for ParsedResume and MatchResult)
            db.delete(resume)
            
        db.commit()
        return len(expired_resumes)
    except Exception as e:
        db.rollback()
        print(f"Error during cleanup task: {e}")
        raise e
    finally:
        db.close()
