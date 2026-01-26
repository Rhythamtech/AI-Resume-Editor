from fastapi import APIRouter
from fastapi import File, Body
from fastapi import UploadFile
from core import parser_adapter
from fastapi import HTTPException
from models import ResumeSchema

router = APIRouter()

@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    result = await parser_adapter(file)

    return result

@router.post("/edit")
async def edit_resume(resume: ResumeSchema = Body(...),job_description: str = Body(...)):
    # TODO: Implement resume editing
    pass


    
