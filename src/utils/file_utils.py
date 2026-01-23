import os
import tempfile
import requests
import pdfplumber
from typing import Optional


def read_pdf(file_path: str) -> str:
    """
    Reads a PDF file and extracts text from all pages.
    
    Args:
        file_path: Path to the PDF file.
        
    Returns:
        Extracted text from the PDF.
        
    Raises:
        Exception: If PDF cannot be read.
    """
    full_text = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""
    return "\n".join(full_text)


def download_file(url: str, suffix: str = ".pdf") -> str:
    """
    Download a file from URL to a temporary location.
    
    Args:
        url: URL to download from.
        suffix: File suffix/extension.
        
    Returns:
        Path to the downloaded temporary file.
        
    Raises:
        requests.HTTPError: If download fails.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        response = requests.get(url)
        response.raise_for_status()
        tmp.write(response.content)
        return tmp.name
