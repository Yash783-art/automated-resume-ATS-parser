import re

SECTION_KEYWORDS = {
    "summary": ["summary", "objective", "profile", "about me"],
    "skills": ["skills", "technical skills", "technologies", "core competencies", "expertise", "knowledge"],
    "experience": ["experience", "work experience", "employment history", "professional background", "career history", "internship", "work history"],
    "education": ["education", "academic background", "academic history", "qualifications", "certifications"],
    "projects": ["projects", "personal projects", "notable works"],
    "contact": ["contact", "personal info", "contact details"],
}

def detect_sections(text: str) -> dict:
    """
    Splits resume text into sections based on heuristic keywords and line-level cues.
    """
    lines = text.split("\n")
    sections = {
        "contact": [],
        "summary": [],
        "skills": [],
        "experience": [],
        "education": [],
        "projects": [],
        "other": []
    }
    
    current_section = "contact" # Start with contact/header
    
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue
            
        # Check if line is a header
        # Heuristics: Short line, matches keywords or looks like a header
        is_header = False
        if len(clean_line) < 50:
            lower_line = clean_line.lower().replace(":", "").strip()
            # Check for exact matches first, then partials
            for section, keywords in SECTION_KEYWORDS.items():
                if any(lower_line == k or (len(lower_line) < 30 and k in lower_line) for k in keywords):
                    current_section = section
                    is_header = True
                    break
        
        if not is_header:
            sections[current_section].append(clean_line)
            
    # Join lines back into text
    return {k: "\n".join(v) for k, v in sections.items()}
