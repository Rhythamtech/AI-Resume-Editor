import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.resume import router as resume_router
import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AI Resume Editor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.mount("/img", StaticFiles(directory="img"), name="img")

@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/template")
async def get_template():
    # Get all images from img folder
    image_files = [f for f in os.listdir("img") if f.lower().endswith('.jpg')]
    
    # Return URLs for the images
    image_urls = [f"/img/{image}" for image in image_files]
    return {"images": image_urls}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
