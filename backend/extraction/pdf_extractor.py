import fitz  # PyMuPDF
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io

def extract_text_ocr(page_image_bytes: bytes) -> str:
    """
    OCR fallback using Tesseract with OpenCV pre-processing.
    """
    # Convert bytes to numpy array
    nparr = np.frombuffer(page_image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return ""

    # Pre-processing: Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Pre-processing: Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    
    # Pre-processing: Binarization (Thresholding)
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Convert back to PIL Image for pytesseract
    pil_img = Image.fromarray(binary)
    
    # Run Tesseract
    text = pytesseract.image_to_string(pil_img)
    
    return text

def extract_text(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF with strict top-to-bottom sorting.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Get blocks with position data
        blocks = page.get_text("blocks")
        # Sort blocks: Primary by Y (top to bottom), Secondary by X (left to right)
        blocks.sort(key=lambda b: (b[1], b[0]))
        
        page_text = "\n".join([b[4].strip() for b in blocks if b[4].strip()])
        
        if not page_text:
            # Fallback to OCR if page text is empty
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_bytes = pix.tobytes("png")
            page_text = extract_text_ocr(img_bytes)
            
        full_text.append(page_text)
        
    doc.close()
    return "\n\n".join(full_text)
