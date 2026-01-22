import os
from jinja2 import Environment, FileSystemLoader
from src.models.resume import ResumeSchema

class ResumeGenerator:
    def __init__(self, templates_dir: str = "src/templates"):
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.templates = {
            "1": "classic.html",
            "2": "modern.html",
            "3": "structural.html",
            "4": "premium.html"
        }

    def generate(self, resume_data: ResumeSchema, template_choice: str, output_filename: str = None):
        """
        Generate a resume based on the provided data and template.
        
        Args:
            resume_data (ResumeSchema): The resume data to be used for generation.
            template_choice (str): The template to be used for generation.
            output_filename (str, optional): The name of the output file. Defaults to None.
        
        Returns:
            str: The name of the output file.
        """
        template_name = self.templates.get(template_choice, "classic.html")
        template = self.env.get_template(template_name)
        rendered_html = template.render(r=resume_data)
        
        if not output_filename:
            output_filename = f"resume_output_{template_choice}.html"
            
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(rendered_html)
            
        return output_filename
