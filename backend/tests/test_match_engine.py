import pytest
from backend.scoring.match_engine import calculate_match

def test_calculate_match_perfect():
    parsed_resume = {
        "skills": ["Python", "React", "AWS"],
        "experience": [],
        "education": []
    }
    processed_jd = {
        "required_skills": ["Python", "React", "AWS"],
        "min_years_experience": 0,
        "required_education_level": "any"
    }
    
    result = calculate_match(parsed_resume, processed_jd)
    
    assert result["overall_score"] == 100.0
    assert result["skills_score"] == 100.0
    assert "Python" in result["matched_keywords"]
    assert len(result["missing_keywords"]) == 0

def test_calculate_match_partial():
    parsed_resume = {
        "skills": ["Python", "JavaScript"],
        "experience": [],
        "education": []
    }
    processed_jd = {
        "required_skills": ["Python", "React", "AWS"],
        "min_years_experience": 0,
        "required_education_level": "any"
    }
    
    result = calculate_match(parsed_resume, processed_jd)
    
    assert result["overall_score"] < 100.0
    assert "Python" in result["matched_keywords"]
    assert "React" in result["missing_keywords"]

def test_calculate_match_semantic():
    # Test that "PostgreSQL" matches "Postgres" or similar
    parsed_resume = {
        "skills": ["PostgreSQL", "FastAPI"],
        "experience": [],
        "education": []
    }
    processed_jd = {
        "required_skills": ["Postgres", "FastAPI"],
        "min_years_experience": 0,
        "required_education_level": "any"
    }
    
    result = calculate_match(parsed_resume, processed_jd)
    # Cosine similarity should be high for "PostgreSQL" vs "Postgres"
    assert "Postgres" in result["matched_keywords"]
    assert result["skills_score"] > 80.0
