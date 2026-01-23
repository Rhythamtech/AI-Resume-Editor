import json
from langchain_core.prompts import PromptTemplate
from src.services import create_llm
from src.models import ResumeSchema, JobKeywords, Experience, Project
from src.core.parser import STANDARD_SCHEMA


class ResumeEditor:    
    def __init__(self):
        self.llm = create_llm()
        self.prompt = PromptTemplate.from_template(
            """
            You are a resume editor. You are given a resume and a job description.
            
            Standard schema:
            {standard_schema}

            Resume text:
            ---
            {resume_text}
            """
        )
        self.keywords_prompt = PromptTemplate.from_template(
            """
            Extract the most critical keywords from this job description. Focus on terms that would filter a resume in an ATS.
            ---
            {job_description}
            """
        )

        self.experience_prompt = PromptTemplate.from_template(
            """
            You are a Resume Editor. 
            Rewrite the user's bullet points to naturally incorporate the provided KEYWORDS.
            
            RULES:
            1. If the user's experience allows, swap generic terms for the specific keywords below.
            2. Example: Change "Used cloud servers" -> "Deployed on AWS EC2" (IF 'AWS' is a keyword).
            3. Do NOT lie. If the keyword is irrelevant to this specific job entry, ignore it.
            
            KEYWORDS TO TARGET:
            {keywords_str}

            Experience:
            ---
            {experience}
            """
        )

        self.project_prompt = PromptTemplate.from_template(
            """
            You are a Technical Recruiter.
            
            OBJECTIVE:
            Rewrite the description of this academic project to highlight TECHNICAL COMPETENCY.
            
            RULES:
            1. Focus on the 'How': Mention libraries, algorithms, or design patterns used.
            2. Connection: If the project used similar concepts to the Target Stack ({stack_str}), emphasize them.
            3. Remove "Student" language:
            - BAD: "I learned how to use Python."
            - GOOD: "Implemented data parsing logic using Python."
            4. Keep it grounded: Do not say you deployed to production if you only ran it on localhost.

            PROJECT:
            ---
            {project}
            """)

    def _extract_keywords(self, job_description: str) -> JobKeywords:
        structured_llm = self.llm.with_structured_output(JobKeywords)
        response = structured_llm.invoke(
            self.keywords_prompt.format(job_description=job_description)
        )
        return response

    def _tailor_experience(self, experience: list[Experience], keywords: JobKeywords) -> list[Experience]:

        tailored_experience = []
    
        for exp in experience:
            structured_llm = self.llm.with_structured_output(Experience)
            response = structured_llm.invoke(
                self.experience_prompt.format(
                    keywords_str=keywords.model_dump_json(),
                    experience=exp.model_dump_json(),
                )
            )
            tailored_experience.append(response)
        return tailored_experience
    
    def _tailor_projects(self, projects:list[Project], keywords: JobKeywords) -> list[Project]:
        tailored_projects = []
    
        for proj in projects:
            structured_llm = self.llm.with_structured_output(Project)
            response = structured_llm.invoke(
                self.project_prompt.format(
                    stack_str=str(keywords.technical_skills),
                    project=proj.model_dump_json(),
                )
            )
            tailored_projects.append(response)
        return tailored_projects

    def edit(self, resume: ResumeSchema, job_description: str) -> ResumeSchema:
        keywords = self._extract_keywords(job_description)
        tailored_experience = self._tailor_experience(resume.experience, keywords)
        

        if resume.projects:
            tailored_projects = self._tailor_projects(resume.projects, keywords)
            resume.projects = tailored_projects

        resume.experience = tailored_experience


        return resume
