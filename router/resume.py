from fastapi import APIRouter
from fastapi import File, Body
from fastapi import UploadFile
from core import parser_adapter, ResumeEditor, ResumeGenerator
from fastapi import HTTPException
from models import ResumeSchema

router = APIRouter()

@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    if not file:
        raise HTTPException(status_code=400, detail="Resume cannot be empty")

    result = await parser_adapter(file)

    return result

@router.post("/edit")
async def edit_resume(resume: ResumeSchema = Body(...),job_description: str = Body(...)):
    
    if not isinstance(resume, ResumeSchema):
        raise HTTPException(status_code=400, detail="Invalid resume schema")

    if not isinstance(job_description, str):
        raise HTTPException(status_code=400, detail="Invalid job description")

    if job_description.strip() == "":
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    if not resume:
        raise HTTPException(status_code=400, detail="Resume cannot be empty")

    editor = ResumeEditor()
    result = editor.edit(resume, job_description)
    return result

@router.post("/render")    
async def render_resume(resume: ResumeSchema = Body(...), template_choice: str = Body(...)):
    if not isinstance(resume, ResumeSchema):
        raise HTTPException(status_code=400, detail="Invalid resume schema")

    if not isinstance(template_choice, str):
        raise HTTPException(status_code=400, detail="Invalid template choice")

    if template_choice.strip() == "":
        raise HTTPException(status_code=400, detail="Template choice cannot be empty")

    if not resume:
        raise HTTPException(status_code=400, detail="Resume cannot be empty")

    generator = ResumeGenerator()
    result = generator.generate(resume, template_choice, html_content=True)
    return result

    

