import os
import json
import re
import tempfile
import requests
from typing import Dict
import pdfplumber
from langchain_core.prompts import PromptTemplate
from fastapi import UploadFile

from services import create_llm
from models import ResumeSchema


# Standard schema definition for LLM prompts
STANDARD_SCHEMA = """{
      "id": "uuid",
      "name": "string",
      "contact": {
        "email": "string",
        "phone": "string",
        "city": "string",
        "region": "string",
        "country": "string",
        "links": [
          {"label":"GitHub","url":"string"},
          {"label":"LinkedIn","url":"string"}
        ]
      },
      "summary": "string",
      "experience": [
        {
          "id":"uuid",
          "title":"string",
          "company":"string",
          "location":"string",
          "start_date":"YYYY-MM",
          "end_date":"YYYY-MM or PRESENT",
          "employment_type":"Full-time/Part-time/Contract/Internship",
          "achievements":["string"],
          "keywords":["string"]
        }
      ],
      "education":[
        {
          "id":"uuid",
          "degree":"string",
          "field":"string",
          "school":"string",
          "start_date":"YYYY-MM",
          "end_date":"YYYY-MM",
          "gpa":"string",
          "honors":"string"
        }
      ],
      "projects":[
        {
          "id":"uuid",
          "title":"string",
          "description":"string",
          "technologies":["string"],
          "link":"string",
          "start_date":"YYYY-MM",
          "end_date":"YYYY-MM"
        }
      ],
      "skills":[
        {"name":"string","level":"beginner|intermediate|advanced|expert|None"}
      ],
      "certifications":[
        {"name":"string","issuer":"string","date":"YYYY-MM"}
      ],
      "languages":[
        {"language":"string","proficiency":"basic|conversational|fluent|native"}
      ],
      "volunteer":[
        {"role":"string","organization":"string","start_date":"YYYY-MM","end_date":"YYYY-MM","description":"string"}
      ],
      "updated_at":"YYYY-MM-DD"
    }"""


class ResumeParser:
    """Parse resumes from PDF files and convert to structured format."""
    
    def __init__(self):
        self.llm = create_llm()
        self.resume_parse_prompt = PromptTemplate.from_template(
    """
    You are a strict parser. Convert the following resume text into JSON matching the "Standard schema" shown below. Output ONLY valid JSON. 
    
    Standard schema:
    {standard_schema}

    Resume text:
    ---
    {resume_text}
    ---
    Rules:
    - Normalize dates to YYYY-MM or "PRESENT".
    - Extract contact emails, phones, links into contact.links.
    - For each experience, include at least 1 bullet in achievements.
    - Job Role must the latest job role in the resume.
    - Based on the past experience, extract the target location.
    - Extract the overall experience in years.
    """ 
)

    def read_pdf(self, file_path: str) -> str:
        """
        Reads a PDF file and extracts text from all pages.
        
        Args:
            file_path: Path to the PDF file.
            
        Returns:
            Extracted text from the PDF.
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

    def process_resume(self, resume_url_or_path: str) -> ResumeSchema:
        """
        Process a resume from URL or local path.
        
        Args:
            resume_url_or_path: URL or local file path to the resume PDF.
            
        Returns:
            Parsed resume as ResumeSchema.
            
        Raises:
            ValueError: If PDF cannot be processed or parsed.
        """
        is_url = resume_url_or_path.startswith("http")
        
        if is_url:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                response = requests.get(resume_url_or_path)
                response.raise_for_status()
                tmp.write(response.content)
                tmp_path = tmp.name
        else:
            tmp_path = resume_url_or_path

        try:
            resume_text = self.read_pdf(tmp_path)
            if not resume_text:
                raise ValueError("PDF loaded but no content found.")
            
            prompt = self.resume_parse_prompt.format(
                resume_text=resume_text, 
                standard_schema=STANDARD_SCHEMA
            )
            response = self.llm.invoke(prompt)
            response_content = response.content
            
            json_data = self._extract_json_from_markdown(response_content)
            resume_schema = ResumeSchema(**json_data)
            
            return resume_schema
        finally:
            if is_url and os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _extract_json_from_markdown(self, md: str) -> Dict:
        """
        Extract JSON from markdown code blocks.
        
        Args:
            md: Markdown string potentially containing JSON.
            
        Returns:
            Parsed JSON as dictionary.
            
        Raises:
            ValueError: If JSON cannot be parsed.
        """
        pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
        match = re.search(pattern, md, re.MULTILINE)
        json_text = match.group(1) if match else md.strip()
        
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON content: {e}")


# For backward compatibility
def extract_candidate_info(resume_url_or_path: str) -> Dict:
    """
    Extract candidate information from resume (backward compatibility function).
    
    Args:
        resume_url_or_path: URL or local file path to the resume PDF.
        
    Returns:
        Resume data as dictionary.
    """
    parser = ResumeParser()
    result = parser.process_resume(resume_url_or_path)
    return result.model_dump()

async def parser_adapter(resume_file: UploadFile) -> Dict:
    pdf_bytes = await resume_file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    parser = ResumeParser()
    result = parser.process_resume(tmp_path)
    return result.model_dump()