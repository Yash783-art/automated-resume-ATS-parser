import pytest
from backend.nlp.jd_processor import process_jd

def test_process_jd_software_engineer():
    jd_text = """
    We are looking for a Senior Software Engineer.
    Requirements:
    - 5+ years of experience in Python and Django.
    - Bachelor's degree in Computer Science or related field.
    - Experience with AWS, Docker, and Kubernetes.
    """
    processed = process_jd(jd_text)
    
    assert processed["min_years_experience"] == 5
    assert processed["required_education_level"] == "bachelors"
    assert "Python" in processed["required_skills"]
    assert "Django" in processed["required_skills"]
    assert "AWS" in processed["required_skills"]

def test_process_jd_marketing():
    jd_text = """
    Marketing Manager needed for a fast-paced agency.
    At least 3 years of experience in digital marketing.
    Master's degree preferred.
    Skills: SEO, SEM, Content Strategy.
    """
    processed = process_jd(jd_text)
    
    assert processed["min_years_experience"] == 3
    assert processed["required_education_level"] == "masters"
    assert "SEO" in processed["required_skills"]

def test_process_jd_no_reqs():
    jd_text = "Hiring someone cool."
    processed = process_jd(jd_text)
    assert processed["min_years_experience"] == 0
    assert processed["required_education_level"] == "any"
