import json
from langchain_core.prompts import PromptTemplate
from services import create_llm
from models import ResumeSchema, JobKeywords, Experience, Project


class ResumeEditor:    
    def __init__(self):
        self.llm = create_llm()
        self.summary_prompt = PromptTemplate.from_template(
            """
            You are an expert resume writer.
            Rewrite ONLY my resume Summary to match the target keywords naturally (no keyword stuffing), stay truthful (don’t add new skills), and keep it under (25-45 words only), ATS-friendly, no first-person. 
            Current Summary: {summary}
            Target Keywords: {keywords_str}
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
            4. Make the bullet more concise and shorten it.
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

    def _tailor_summary(self, summary: str, keywords: JobKeywords) -> str:
        response = self.llm.invoke(
            self.summary_prompt.format(
                summary=summary,
                keywords_str=keywords.model_dump_json(),
            )
        )
        return response.content

    def edit(self, resume: ResumeSchema, job_description: str) -> ResumeSchema:
        keywords = self._extract_keywords(job_description)
        tailored_experience = self._tailor_experience(resume.experience, keywords)
        tailored_summary = self._tailor_summary(resume.summary, keywords)

        if resume.projects:
            tailored_projects = self._tailor_projects(resume.projects, keywords)
            resume.projects = tailored_projects

        resume.experience = tailored_experience
        resume.summary = tailored_summary

        return resume
