import pytest
import io
from unittest.mock import patch
from reportlab.pdfgen import canvas
from backend.extraction.pdf_extractor import extract_text

def create_dummy_pdf(text: str) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, text)
    c.save()
    return buffer.getvalue()

def test_extract_text_basic():
    original_text = "This is a test resume content."
    pdf_bytes = create_dummy_pdf(original_text)
    
    extracted_text = extract_text(pdf_bytes)
    assert original_text in extracted_text

def test_extract_text_empty():
    # Empty PDF (1 page with nothing)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.showPage()
    c.save()
    pdf_bytes = buffer.getvalue()
    
    with patch("backend.extraction.pdf_extractor.pytesseract.image_to_string") as mock_ocr:
        mock_ocr.return_value = ""
        extracted_text = extract_text(pdf_bytes)
        assert extracted_text.strip() == ""

def test_extract_text_multi_page():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "Page 1")
    c.showPage()
    c.drawString(100, 750, "Page 2")
    c.save()
    pdf_bytes = buffer.getvalue()
    
    extracted_text = extract_text(pdf_bytes)
    assert "Page 1" in extracted_text
    assert "Page 2" in extracted_text

# Note: Testing OCR fallback would require a PDF with an image of text.
def test_extract_text_ocr_trigger():
    # Create an empty PDF page which triggers OCR
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.showPage()
    c.save()
    pdf_bytes = buffer.getvalue()
    
    with patch("backend.extraction.pdf_extractor.pytesseract.image_to_string") as mock_ocr:
        mock_ocr.return_value = "OCR Text"
        extracted_text = extract_text(pdf_bytes)
        assert "OCR Text" in extracted_text

