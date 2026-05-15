from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import MatchResult, User
from backend.auth import get_current_user
import csv
import io

router = APIRouter()

@router.get("/csv/{match_id}")
async def export_match_csv(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    match = db.query(MatchResult).filter(
        MatchResult.id == match_id
    ).first()
    
    if not match or match.resume.user_id != current_user.clerk_id:
        raise HTTPException(status_code=404, detail="Match result not found.")
        
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Field", "Value"])
    writer.writerow(["Overall Score", match.overall_score])
    writer.writerow(["Skills Score", match.skills_score])
    writer.writerow(["Experience Score", match.experience_score])
    writer.writerow(["Education Score", match.education_score])
    writer.writerow(["Matched Keywords", ", ".join(match.matched_keywords)])
    writer.writerow(["Missing Keywords", ", ".join(match.missing_keywords)])
    
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=match_{match_id}.csv"}
    )

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

@router.get("/pdf/{match_id}")
async def export_match_pdf(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    match = db.query(MatchResult).filter(MatchResult.id == match_id).first()
    if not match or match.resume.user_id != current_user.clerk_id:
        raise HTTPException(status_code=404, detail="Match result not found.")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f"ATS Analysis Report: {match.resume.filename}")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 720, f"Candidate Name: {match.resume.parsed_resume.structured_json.get('contact', {}).get('name', 'N/A')}")
    p.drawString(100, 700, f"Overall Score: {round(match.overall_score, 1)}%")
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 670, "Score Breakdown:")
    p.setFont("Helvetica", 10)
    p.drawString(120, 650, f"Skills: {round(match.skills_score, 1)}%")
    p.drawString(120, 635, f"Experience: {round(match.experience_score, 1)}%")
    p.drawString(120, 620, f"Education: {round(match.education_score, 1)}%")
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 590, "Matched Skills:")
    p.setFont("Helvetica", 10)
    p.drawString(100, 575, ", ".join(match.matched_keywords[:10]))
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=report_{match_id}.pdf"}
    )
