from src.utils.parser import ResumeParser
from src.utils.generator import ResumeGenerator

def main():
    url = "CV.pdf"

    parser = ResumeParser()
    response = parser.process_resume(url)
    generator = ResumeGenerator()
    generator.generate(response,1,"resume.html") 


if __name__ == "__main__":
    main()
