from src.core import ResumeParser, ResumeEditor, ResumeGenerator
from src.models import ResumeSchema
import json    


def main():
    """Main entry point for the AI Resume Editor."""
    # Input resume file
    resume_path = "CV.pdf"
    
    # Parse the resume
    print("📄 Parsing resume...")
    parser = ResumeParser()
    resume_data = parser.process_resume(resume_path)
    print(f"✅ Resume parsed successfully for: {resume_data.name}")

    # Extract keywords
    print("📄 Extracting keywords...")
    with open("examples/sample_job_description.txt", "r") as f:
        job_desc = f.read()

    # Edit resume
    print("📄 Editing resume...")
    editor = ResumeEditor()
    edited_resume = editor.edit(resume_data, job_description=job_desc)
    
    # Generate HTML resume
    print("\n🎨 Generating HTML resume...")
    generator = ResumeGenerator()
    output_file = generator.generate(edited_resume, template_choice="3", output_filename="resume.html")
    print(f"✅ Resume generated: {output_file}")


if __name__ == "__main__":
    main()
