import re
import spacy

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    nlp = spacy.blank("en")

def extract_years_experience(text: str) -> int:
    """
    Extracts minimum years of experience using regex.
    """
    patterns = [
        r'(\d+)\+?\s*years?',
        r'(\d+)\s*to\s*\d+\s*years?',
        r'at least\s*(\d+)\s*years?',
        r'minimum of\s*(\d+)\s*years?'
    ]
    
    max_years = 0
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                years = int(match)
                if years > max_years:
                    max_years = years
            except ValueError:
                continue
    return max_years

def extract_education_level(text: str) -> str:
    """
    Extracts required education level.
    """
    levels = {
        "phd": ["phd", "doctorate"],
        "masters": ["master", "ms", "ma", "mba"],
        "bachelors": ["bachelor", "bs", "ba", "degree"],
    }
    
    for level, keywords in levels.items():
        for keyword in keywords:
            if re.search(r'\b' + keyword + r'\b', text, re.IGNORECASE):
                return level
    return "any"

def process_jd(jd_text: str) -> dict:
    """
    Processes a job description to extract key requirements.
    """
    # Better Skill Extraction: Use section detection
    from backend.nlp.section_detector import detect_sections
    sections = detect_sections(jd_text)
    
    # Target specific sections likely to contain skills
    target_text = sections.get("skills", "") + " " + sections.get("experience", "") + " " + sections.get("education", "")
    if not target_text.strip():
        target_text = jd_text # Fallback
        
    doc = nlp(target_text)
    skills = []
    
    BLACKLIST = {
        "experience", "team", "work", "role", "requirements", "languages", 
        "hobbies", "travelling", "activities", "projects", "opportunity",
        "benefits", "salary", "remote", "office", "company", "culture",
        "hindi", "english", "marathi", "fluent", "basic", "knowledge", "skills",
        "location", "candidate", "about", "looking", "description", "apply"
    }

    for token in doc:
        # Look for proper nouns or nouns that aren't in the blacklist
        if token.pos_ in ["PROPN", "NOUN"] and len(token.text) > 1:
            clean_text = token.text.strip().lower()
            if clean_text not in BLACKLIST:
                skills.append(token.text)
                
    # Deduplicate and limit
    unique_skills = list(dict.fromkeys(skills))[:20]
    
    return {
        "title": getattr(jd_text, "title", ""), # Placeholder if passed as object
        "required_skills": unique_skills,
        "nice_to_have_skills": [], # Placeholder
        "min_years_experience": extract_years_experience(str(jd_text)),
        "required_education_level": extract_education_level(str(jd_text)),
        "key_responsibilities": [], # Placeholder
    }
