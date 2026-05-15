import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from backend.scoring.embedder import embedder

PROFESSION_DOMAINS = {
    "software_engineering": [
        "software engineer", "developer", "programmer", "backend", "frontend",
        "fullstack", "devops", "sre", "data engineer", "ml engineer"
    ],
    "design": [
        "graphic designer", "ui designer", "ux designer", "visual designer",
        "illustrator", "creative director"
    ],
    "management": ["manager", "director", "vp", "cto", "ceo", "product manager"],
    "data_science": ["data scientist", "data analyst", "machine learning", "ai researcher"],
    "marketing": ["marketing", "seo", "content", "copywriter", "brand"],
}

def classify_domain(text: str) -> str:
    if not text:
        return "general"
    text_lower = text.lower()
    for domain, keywords in PROFESSION_DOMAINS.items():
        if any(kw in text_lower for kw in keywords):
            return domain
    return "general"

def calculate_match(parsed_resume: dict, processed_jd: dict) -> dict:
    """
    Calculates the match score between a resume and a job description.
    """
    jd_title = processed_jd.get("title", "").lower()
    resume_text = str(parsed_resume).lower()
    
    # ─── NUCLEAR CHECK (GOD MODE) ───
    # If it's a Tech JD
    if any(w in jd_title for w in ["engineer", "developer", "software", "programmer", "tech", "web"]):
        # AND it's a Designer resume
        if any(w in resume_text for w in ["designer", "graphic", "photoshop", "illustrator", "canva", "art"]):
            # AND it's NOT also an engineer
            if not any(w in resume_text for w in ["engineer", "developer", "software", "coding", "code"]):
                return {
                    "overall_score": 0.0,
                    "skills_score": 0.0,
                    "experience_score": 0.0,
                    "education_score": 0.0,
                    "matched_keywords": [],
                    "missing_keywords": processed_jd.get("required_skills", []),
                }
    # ─── 1. Skills Score (40%) ───
    resume_skills = parsed_resume.get("skills", [])
    jd_skills = processed_jd.get("required_skills", [])
    
    if not jd_skills:
        skills_score = 100.0
        matched_keywords = []
        missing_keywords = []
    else:
        # Embed skills
        resume_vecs = embedder.embed(resume_skills)
        jd_vecs = embedder.embed(jd_skills)
        
        if resume_vecs.size == 0:
            skills_score = 0.0
            matched_keywords = []
            missing_keywords = jd_skills
        else:
            # For each JD skill, find the best match in the resume
            similarities = cosine_similarity(jd_vecs, resume_vecs)
            best_matches = np.max(similarities, axis=1)
            
            # Threshold for "match"
            THRESHOLD = 0.7
            matched_indices = np.where(best_matches >= THRESHOLD)[0]
            missing_indices = np.where(best_matches < THRESHOLD)[0]
            
            matched_keywords = [jd_skills[i] for i in matched_indices]
            missing_keywords = [jd_skills[i] for i in missing_indices]
            
            # Score is the average of best matches
            skills_score = float(np.mean(best_matches)) * 100.0
            
    # ─── 2. Experience Score (40%) ───
    jd_years = processed_jd.get("min_years_experience", 0)
    exp_entries = parsed_resume.get("experience", [])
    exp_text = " ".join([e.get("text", "") for e in exp_entries])
    
    # Check Relevance via Cosine Similarity
    if not exp_text.strip() or not processed_jd.get("content"):
        experience_score = 0.0 if processed_jd.get("content") else 50.0
    else:
        # Embed full experience text and JD text
        exp_vec = embedder.embed([exp_text])
        jd_vec = embedder.embed([processed_jd.get("content", "")])
        
        if exp_vec.size > 0 and jd_vec.size > 0:
            sim = cosine_similarity(jd_vec, exp_vec)[0][0]
            experience_score = float(max(0.0, min(100.0, sim * 100.0)))
        else:
            experience_score = 50.0
        
    # ─── 3. Education Score (20%) ───
    edu_weights = {"any": 0, "bachelors": 1, "masters": 2, "phd": 3}
    jd_edu_level = processed_jd.get("required_education_level", "any")
    
    # Extract from parsed education
    resume_edu_level = "any"
    edu_text = " ".join([e.get("text", "") for e in parsed_resume.get("education", [])]).lower()
    
    if any(w in edu_text for w in ["phd", "ph.d", "doctorate"]):
        resume_edu_level = "phd"
    elif any(w in edu_text for w in ["master", "m.s", "ma ", "mba", "m.a"]):
        resume_edu_level = "masters"
    elif any(w in edu_text for w in ["bachelor", "b.s", "ba ", "bsc", "b.a", "btech", "b.tech"]):
        resume_edu_level = "bachelors"
    
    if jd_edu_level == "any":
        education_score = 50.0 # Default to 50 if JD doesn't care
    elif edu_weights.get(resume_edu_level, 0) >= edu_weights.get(jd_edu_level, 0):
        education_score = 100.0
    else:
        education_score = 50.0 # Partial match
        
    # ─── 4. Title Match (Total Shutdown) ───
    jd_title = processed_jd.get("title", "").lower()
    resume_skills = [s.lower() for s in parsed_resume.get("skills", [])]
    
    # If it's a Tech JD
    if any(w in jd_title for w in ["engineer", "developer", "software", "programmer", "tech", "web"]):
        # But the resume doesn't have a SINGLE tech skill in its list
        tech_keywords = ["java", "python", "javascript", "html", "css", "php", "sql", "react", "node", "aws", "docker", "c++", "c#", "ruby"]
        if not any(k in tech_keywords for k in resume_skills):
            # Also check if they even have "Engineer" in their background
            if not any(w in str(parsed_resume).lower() for w in ["engineer", "developer", "software"]):
                return {
                    "overall_score": 0.0,
                    "skills_score": 0.0,
                    "experience_score": 0.0,
                    "education_score": 0.0,
                    "matched_keywords": [],
                    "missing_keywords": processed_jd.get("required_skills", []),
                }
            
    # ─── 4.5 Profession Mismatch Gate ───
    jd_title_words = set([w for w in jd_title.split() if len(w) > 3])
    profession_match = False
    
    if not jd_title_words:
        profession_match = True
    else:
        for w in jd_title_words:
            if w in resume_text:
                profession_match = True
                break
                
    # ─── 5. Overall Score (Stricter Weighted Average) ───
    overall_score = (skills_score * 0.7) + (experience_score * 0.2) + (education_score * 0.1)
    
    jd_content = processed_jd.get("content", "")
    resume_raw_text = parsed_resume.get("raw_text", "") or str(parsed_resume)
    
    jd_domain = classify_domain(jd_content) if jd_content else classify_domain(jd_title)
    resume_domain = classify_domain(resume_raw_text)
    
    profession_mismatch = False
    if jd_domain != "general" and resume_domain != "general" and jd_domain != resume_domain:
        overall_score = min(overall_score, 15.0)
        profession_mismatch = True
    elif not profession_match:
        overall_score = min(overall_score, 25.0)
    
    return {
        "overall_score": round(overall_score, 1),
        "skills_score": round(skills_score, 1),
        "experience_score": round(experience_score, 1),
        "education_score": round(education_score, 1),
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "profession_mismatch": profession_mismatch,
    }
