from backend.tasks.celery_app import celery_app
from backend.database import SessionLocal
from backend.models import Resume, ParsedResume
from backend.extraction.pdf_extractor import extract_text
from backend.nlp.parser import parse_resume
from backend.storage import storage
import boto3
from botocore.exceptions import ClientError
from backend.config import settings

@celery_app.task(name="backend.tasks.parse.parse_resume_task")
def parse_resume_task(resume_id: int):
    """
    Celery task to extract and parse resume text.
    """
    db = SessionLocal()
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            return f"Resume {resume_id} not found"
            
        resume.status = "processing"
        db.commit()
        
        # 1. Download from storage (Handles R2 or Local fallback)
        try:
            file_bytes = storage.get_file(resume.r2_key)
        except Exception as e:
            resume.status = "failed"
            db.commit()
            return f"Failed to retrieve file: {e}"
            
        # 2. Extract text
        raw_text = extract_text(file_bytes)
        with open("debug_text.txt", "w", encoding="utf-8") as f:
            f.write(raw_text)
        
        # 3. Parse text
        parsed_data = parse_resume(raw_text)
        
        # 4. Save parsed results
        parsed_resume = ParsedResume(
            resume_id=resume.id,
            raw_text=raw_text,
            structured_json=parsed_data,
            confidence_score=parsed_data.get("confidence", 0.0)
        )
        db.add(parsed_resume)
        
        resume.status = "parsed"
        db.commit()
        
        # 5. Automatically trigger matching against all active JDs
        celery_app.send_task("backend.tasks.match.match_resume_to_all_jds_task", args=[resume.id])
        
        return f"Successfully parsed and queued matching for resume {resume_id}"
        
    except Exception as e:
        if resume:
            resume.status = "failed"
            db.commit()
        print(f"Error parsing resume {resume_id}: {e}")
        raise e
    finally:
        db.close()
