# AI Resume Editor

AI Resume Editor is a powerful tool that leverages large language models to automatically analyze, improve, and customize your resume for specific job descriptions. It parses various resume formats, suggests enhancements, and can generate tailored versions and cover letters, helping you present a polished, job-focused application.

## 🚀 Features

- **📄 Resume Parsing**: Extract structured data from PDF resumes
- **🎯 Job Tailoring**: Customize resumes for specific job descriptions
- **🔍 Keyword Extraction**: Identify critical ATS keywords from job postings
- **🎨 Multiple Templates**: Generate beautiful HTML resumes with 4 different templates
- **🤖 AI-Powered**: Uses advanced LLMs for intelligent resume optimization

## 📁 Project Structure

```
AI Resume Editor/
├── src/
│   ├── config/          # Configuration management
│   ├── core/            # Core business logic (parser, editor, generator)
│   ├── models/          # Pydantic data models
│   ├── services/        # External services (LLM)
│   ├── templates/       # HTML resume templates
│   └── utils/           # Pure utility functions
├── tests/               # Test suite
├── examples/            # Example usage and sample files
├── backup/              # Backup of previous structure
├── main.py              # Main entry point
└── README.md
```

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "AI Resume Editor"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
# or using uv
uv pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4
# Optional: OPENAI_BASE_URL=https://api.openai.com/v1
```

## 📖 Usage

### Basic Usage

Run the main script to parse a resume and generate HTML:

```bash
python main.py
```

### Advanced Usage

#### 1. Parse a Resume

```python
from src.core import ResumeParser

parser = ResumeParser()
resume_data = parser.process_resume("CV.pdf")
print(f"Parsed resume for: {resume_data.name}")
```

#### 2. Generate HTML Resume

```python
from src.core import ResumeParser, ResumeGenerator

# Parse resume
parser = ResumeParser()
resume_data = parser.process_resume("CV.pdf")

# Generate HTML with different templates
generator = ResumeGenerator()
output_file = generator.generate(
    resume_data, 
    template_choice="1",  # 1=classic, 2=modern, 3=structural, 4=premium
    output_filename="my_resume.html"
)
```

#### 3. Tailor Resume for Job

```python
from src.core import ResumeParser, ResumeEditor

# Parse resume
parser = ResumeParser()
resume_data = parser.process_resume("CV.pdf")

# Read job description
with open("job_description.txt", "r") as f:
    job_desc = f.read()

# Tailor resume
editor = ResumeEditor()
tailored_resume = editor.tailor_resume(resume_data, job_desc)
```

#### 4. Extract Keywords from Job Description

```python
from src.core import ResumeEditor

editor = ResumeEditor()
job_desc = "Looking for a Python developer with AWS experience..."
keywords = editor.extract_keywords(job_desc)

print("Technical Skills:", keywords.technical_skills)
print("Soft Skills:", keywords.soft_skills)
print("Domain Lingo:", keywords.domain_lingo)
```

## 🎨 Available Templates

1. **Classic** - Traditional, professional layout
2. **Modern** - Contemporary design with clean aesthetics
3. **Structural** - Organized, section-focused layout
4. **Premium** - Elegant, feature-rich design


## 📚 Documentation

- See `examples/README.md` for more usage examples
- Check `examples/sample_job_description.txt` for job description format

## 🔧 Configuration

All configuration is managed through `src/config/settings.py`. You can customize:

- LLM model and parameters
- Template directory location
- Default temperature for AI responses

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. Code follows the project structure
2. Tests are added for new features
3. Documentation is updated

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

Built with:
- LangChain for LLM orchestration
- Pydantic for data validation
- Jinja2 for template rendering
- PDFPlumber for PDF parsing
