# Core/Risk-assisment/contract_loader.py
import os
import pdfplumber
from typing import List, Dict, Any

def load_live_contract(file_path: str) -> List[Dict[str, Any]]:
    """
    Ingests live contract files supporting PDF and TXT formats.
    Extracts raw text pages and preserves structural page numbers.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Target contract file not found at: {file_path}")
        
    contract_pages = []
    file_extension = os.path.splitext(file_path)[1].lower()
    
    # Process PDF contract files using pdfplumber mapping
    if file_extension == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text and text.strip():
                    contract_pages.append({
                        "text": text.strip(),
                        "page_number": page_num,
                        "source_file": os.path.basename(file_path)
                    })
                    
    # Process standard text contract files
    elif file_extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as txt_file:
            text = txt_file.read()
            if text.strip():
                contract_pages.append({
                    "text": text.strip(),
                    "page_number": 1,
                    "source_file": os.path.basename(file_path)
                })
    else:
        raise ValueError(f"Unsupported contract file format extension: {file_extension}")
        
    return contract_pages
