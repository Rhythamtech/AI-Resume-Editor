from typing import List, Optional
from pydantic import BaseModel

class ContactLink(BaseModel):
    label: str
    url: str

class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    links: List[ContactLink] = []

class Experience(BaseModel):
    id: Optional[str] = None
    title: str
    company: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    employment_type: Optional[str] = None
    achievements: List[str] = []
    keywords: List[str] = []

class Education(BaseModel):
    id: Optional[str] = None
    degree: str
    field: Optional[str] = None
    school: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: Optional[str] = None

class Project(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    technologies: List[str] = []
    link: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Skill(BaseModel):
    name: str
    level: Optional[str] = None

class Certification(BaseModel):
    name: str
    issuer: str
    date: Optional[str] = None

class Language(BaseModel):
    language: str
    proficiency: Optional[str] = None

class Volunteer(BaseModel):
    role: str
    organization: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class ResumeSchema(BaseModel):
    id: Optional[str] = None
    name: str
    contact: ContactInfo
    summary: Optional[str] = None
    experience: List[Experience] = []
    education: List[Education] = []
    projects: List[Project] = []
    skills: List[Skill] = []
    certifications: List[Certification] = []
    languages: List[Language] = []
    volunteer: List[Volunteer] = []
    updated_at: Optional[str] = None
