from jinja2 import Environment, FileSystemLoader

from src.models import ResumeSchema
from src.config import settings


class ResumeGenerator:
    """Generate HTML resumes from structured data using templates."""
    
    def __init__(self, templates_dir: str = None):
        """
        Initialize the resume generator.
        
        Args:
            templates_dir: Directory containing HTML templates. 
                          If None, uses default from settings.
        """
        if templates_dir is None:
            templates_dir = settings.templates_dir
            
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.templates = {
            "1": "classic.html",
            "2": "modern.html",
            "3": "structural.html",
            "4": "premium.html"
        }

    def generate(
        self, 
        resume_data: ResumeSchema, 
        template_choice: str, 
        output_filename: str = None
    ) -> str:
        """
        Generate a resume based on the provided data and template.
        
        Args:
            resume_data: The resume data to be used for generation.
            template_choice: The template to be used for generation (1-4).
            output_filename: The name of the output file. If None, auto-generates.
        
        Returns:
            The name of the output file.
        """
        template_name = self.templates.get(str(template_choice), "classic.html")
        template = self.env.get_template(template_name)
        rendered_html = template.render(r=resume_data)
        
        if not output_filename:
            output_filename = f"resume_output_{template_choice}.html"
            
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(rendered_html)
            
        return output_filename
