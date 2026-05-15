import pytest
from backend.nlp.parser import parse_resume

def test_parse_resume_basic():
    raw_text = """
    John Doe
    john.doe@example.com | (123) 456-7890
    
    Summary
    Experienced software engineer with a focus on Python and React.
    
    Skills
    Python, JavaScript, React, PostgreSQL, Docker, AWS
    
    Experience
    Senior Developer at Tech Corp (2020-Present)
    - Led a team of 5 developers.
    - Improved API performance by 40%.
    
    Education
    B.S. in Computer Science, University of Technology (2016-2020)
    """
    
    parsed = parse_resume(raw_text)
    
    assert parsed["contact"]["name"] == "John Doe"
    assert parsed["contact"]["email"] == "john.doe@example.com"
    assert parsed["contact"]["phone"] == "(123) 456-7890"
    
    assert "Python" in parsed["skills"]
    assert "React" in parsed["skills"]
    assert "AWS" in parsed["skills"]
    
    assert len(parsed["experience"]) > 0
    assert len(parsed["education"]) > 0
    assert "Summary" not in parsed["summary"] # Check it didn't include the header

def test_parse_resume_no_contact():
    raw_text = """
    Skills
    Python, Java
    """
    parsed = parse_resume(raw_text)
    assert parsed["contact"]["email"] is None
    assert "Python" in parsed["skills"]
