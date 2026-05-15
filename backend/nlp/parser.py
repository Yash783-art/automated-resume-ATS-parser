import spacy
import re
from backend.nlp.section_detector import detect_sections

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    # Fallback if model not found (though it should be installed)
    nlp = spacy.blank("en")

def extract_contact_info(contact_text: str) -> dict:
    """
    Extracts email, phone, and name from contact section using NER and regex.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    PHONE_PATTERNS = [
        r'\+91[\s\-]?\d{10}',          # +91 8007329406
        r'\b[6-9]\d{9}\b',              # bare 10-digit Indian mobile
        r'\(\d{3}\)\s?\d{3}[\-\s]\d{4}' # US format fallback
    ]
    
    email = re.search(email_pattern, contact_text)
    
    phone = None
    for pattern in PHONE_PATTERNS:
        match = re.search(pattern, contact_text)
        if match:
            phone = match
            break
    
    # Use spaCy NER to find the name
    doc = nlp(contact_text[:500]) # Only look at the beginning
    name = "Unknown"
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break
            
    # Fallback: if no PERSON ent found, use the first line IF it doesn't look like a sentence
    if name == "Unknown":
        lines = [l.strip() for l in contact_text.split("\n") if l.strip()]
        if lines:
            first_line = lines[0]
            # If it's short and doesn't have common "objective" words
            if len(first_line) < 50 and not any(w in first_line.lower() for w in ["strive", "objective", "summary", "experience"]):
                name = first_line
    
    return {
        "name": name,
        "email": email.group(0) if email else None,
        "phone": phone.group(0).strip() if phone else None,
    }

def extract_location(text: str) -> str | None:
    # First try GPE entities from spaCy
    doc = nlp(text[:1000])
    gpe_entities = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    if gpe_entities:
        return ", ".join(gpe_entities[:2])  # city, state
    return None

def extract_skills(skills_text: str) -> list:
    """
    Extracts skills from text. Splits by comma, newline, or common bullet characters.
    """
    BLOCKLIST = {
        "hobbies", "languages", "participated activities", "personal skills", 
        "english (basic)", "hindi (fluent)", "painting", "photography", "travelling",
        "english", "hindi", "spanish", "french", "german", "reading", "writing",
        "activities", "interests", "summary", "objective"
    }
    
    # Split by comma, newline, or bullet points
    parts = re.split(r'[,\n•·|]', skills_text)
    # Clean and filter
    skills = []
    for p in parts:
        s = p.strip().strip("-").strip()
        
        if not s or len(s) < 2 or len(s) >= 40:
            continue
            
        # Word count check
        words = s.split()
        if len(words) > 4:
            continue
            
        s_lower = s.lower()
        if s_lower in BLOCKLIST:
            continue
            
        skills.append(s)
    
    # Preserve order but remove duplicates
    return list(dict.fromkeys(skills))

def parse_resume(raw_text: str) -> dict:
    """
    Main parsing pipeline.
    """
    sections = detect_sections(raw_text)
    
    # IMPROVED NAME FINDER: Search the WHOLE text if contact section is weak
    contact_text = sections.get("contact", "")
    if len(contact_text) < 10:
        contact_text = raw_text[:1000] # Use the first 1000 chars as fallback contact info
        
    contact = extract_contact_info(contact_text)
    
    # Final Fallback for Name: If still unknown, just take the first non-empty line of the whole resume
    if contact["name"] == "Unknown":
        all_lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
        if all_lines:
            contact["name"] = all_lines[0][:50] # Take first 50 chars of first line
            
    contact["location"] = extract_location(contact_text)
            
    skills = extract_skills(sections.get("skills", ""))
    
    # Placeholder for more complex NER-based extraction for education and experience
    parsed_data = {
        "contact": contact,
        "skills": skills,
        "summary": sections.get("summary", ""),
        "education": [], # TODO: Use NER
        "experience": [], # TODO: Use NER
        "confidence": 0.85 # Placeholder
    }
    
    # Basic Education Extraction (Heuristic)
    edu_text = sections.get("education", "")
    if edu_text:
        # Simple split by line for now
        for line in edu_text.split("\n"):
            if line.strip():
                parsed_data["education"].append({"text": line.strip()})
                
    # Basic Experience Extraction (Heuristic)
    exp_text = sections.get("experience", "")
    if exp_text:
        # Simple split by line for now
        for line in exp_text.split("\n"):
            if line.strip():
                parsed_data["experience"].append({"text": line.strip()})
                
    return parsed_data
