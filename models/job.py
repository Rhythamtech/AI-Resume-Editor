from typing import List
from pydantic import BaseModel, Field


class JobKeywords(BaseModel):
    """Keywords extracted from a job description."""
    technical_skills: List[str] = Field(description="Hard skills like Python, AWS, React")
    soft_skills: List[str] = Field(description="Interpersonal skills like Leadership, Agile")
    domain_lingo: List[str] = Field(description="Industry specific terms like 'High Frequency Trading' or 'HIPAA'")


class JobDescription(BaseModel):
    """Job description model."""
    title: str
    company: str
    description: str
    requirements: List[str] = []
    keywords: JobKeywords = None
