import pdfplumber
import pytesseract
from pdf2image import convert_from_path


def extract_menu_items(pdf_path):
    menu_items = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                menu_items.extend(text.split('\n'))
    
    return menu_items


def extract_menu_items_with_ocr(pdf_path):
    menu_items = []
    images = convert_from_path(pdf_path)
    for image in images:
        text = pytesseract.image_to_string(image)
        menu_items.extend(text.split('\n'))
    
    return menu_items