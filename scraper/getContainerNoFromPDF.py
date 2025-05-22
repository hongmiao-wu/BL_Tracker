import pdfplumber
import re

def extract_container_numbers_from_pdf(pdf_path):
    containers = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            chars = page.chars  # each char position
            line_chars = sorted(chars, key=lambda c: (c['top'], c['x0']))

            current_line_y = None
            current_line = ""

            for char in line_chars:
                if current_line_y is None or abs(char['top'] - current_line_y) < 2:
                    current_line += char['text']
                else:
                    containers += re.findall(r'[A-Z]{3}U[0-9]{7}', current_line)
                    current_line = char['text']
                current_line_y = char['top']
            containers += re.findall(r'[A-Z]{3}U[0-9]{7}', current_line)
    return containers
