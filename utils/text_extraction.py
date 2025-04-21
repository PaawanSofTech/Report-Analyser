import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_text = ""
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        extracted_text += page.get_text("text")
        
    return extracted_text

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def save_extracted_text(text, output_file):
    with open(output_file, "w") as f:
        f.write(text)
