from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI(title="Career Fit AI Advisor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """Extract text from PDF, DOCX, or TXT files"""
    
    if filename.endswith('.pdf'):
        try:
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")
    
    elif filename.endswith('.docx'):
        try:
            from docx import Document
            doc = Document(io.BytesIO(file_content))
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {str(e)}")
    
    elif filename.endswith('.txt'):
        return file_content.decode('utf-8', errors='ignore')
    
    else:
        raise ValueError(f"Unsupported file format: {filename}")


def get_role_profile(career_path: str) -> dict:
    """Get the profile for a specific career path"""
    
    profiles = {
        "Software Engineer": {
            "core_skills": ["Python", "Java", "JavaScript", "C++", "Git", "REST APIs", "SQL", "HTML", "CSS", "System Design"],
            "nice_to_have": ["Docker", "Kubernetes", "CI/CD", "AWS", "Azure"],
            "description": "Backend and full-stack development role"
        },
        "Data Scientist": {
            "core_skills": ["Python", "SQL", "Machine Learning", "Statistics", "TensorFlow", "Pandas", "NumPy", "Data Analysis", "Scikit-learn"],
            "nice_to_have": ["Deep Learning", "NLP", "Computer Vision", "Spark", "Scala"],
            "description": "Data analysis and machine learning focus"
        },
        "Product Manager": {
            "core_skills": ["Product Strategy", "User Research", "Wireframing", "Analytics", "Roadmap Planning", "Communication", "Metrics"],
            "nice_to_have": ["Agile", "SQL", "A/B Testing", "Prototyping", "Market Research"],
            "description": "Product strategy and cross-functional collaboration"
        },
        "UX Designer": {
            "core_skills": ["Figma", "User Research", "Prototyping", "Wireframing", "UI Design", "Design Thinking", "Usability Testing"],
            "nice_to_have": ["Animation", "CSS", "JavaScript", "Accessibility", "Design Systems"],
            "description": "User experience and interface design"
        },
        "DevOps Engineer": {
            "core_skills": ["Docker", "Kubernetes", "CI/CD", "Linux", "AWS", "Terraform", "Jenkins", "Git", "Bash"],
            "nice_to_have": ["Python", "Ansible", "Prometheus", "ELK Stack", "Microservices"],
            "description": "Infrastructure and deployment automation"
        },
        "AI/ML Engineer": {
            "core_skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NLP", "Computer Vision", "Neural Networks"],
            "nice_to_have": ["Transformer Models", "Reinforcement Learning", "MLOps", "CUDA", "Distributed Training"],
            "description": "Advanced AI and machine learning development"
        },
        "Frontend Developer": {
            "core_skills": ["JavaScript", "React", "HTML", "CSS", "Git", "REST APIs", "TypeScript", "Responsive Design", "DOM"],
            "nice_to_have": ["Vue", "Angular", "Next.js", "Webpack", "Testing", "Performance Optimization"],
            "description": "Web frontend and user interface development"
        },
        "Backend Developer": {
            "core_skills": ["Python", "Java", "SQL", "REST APIs", "Databases", "Git", "System Design", "Microservices", "Authentication"],
            "nice_to_have": ["Docker", "Kubernetes", "Message Queues", "Caching", "Scalability", "Cloud Platforms"],
            "description": "Backend services and API development"
        },
    }
    
    return profiles.get(career_path)


def extract_skills(text: str) -> list:
    """Extract skills from resume text"""
    
    common_skills = [
        "Python", "Java", "JavaScript", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "SQL",
        "React", "Vue", "Angular", "Next.js", "Node.js", "Django", "Flask", "FastAPI",
        "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "Jenkins", "CI/CD",
        "Machine Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn",
        "Data Analysis", "Statistics", "NLP", "Computer Vision", "Deep Learning",
        "REST APIs", "GraphQL", "Microservices", "System Design", "Database Design",
        "Figma", "UI Design", "UX Design", "Prototyping", "User Research",
        "Product Strategy", "Analytics", "Roadmap", "Agile", "Scrum",
        "Linux", "Bash", "Terraform", "Ansible", "Prometheus",
        "HTML", "CSS", "TypeScript", "Testing", "Responsive Design",
        "Authentication", "Security", "Caching", "Message Queues", "Scalability"
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))


def generate_recommendations(career_path: str, matching_skills: list, missing_skills: list, fit_score: float) -> str:
    """Generate personalized recommendations for the candidate"""
    
    percentage = int(fit_score * 100)
    
    if percentage >= 80:
        fit_level = "EXCELLENT FIT"
        advice = "You're well-prepared for this role! Focus on staying updated with latest technologies."
    elif percentage >= 60:
        fit_level = "GOOD FIT"
        advice = "You have a solid foundation. Work on the missing skills to strengthen your profile."
    elif percentage >= 40:
        fit_level = "MODERATE FIT"
        advice = "You have the basics. Invest time in learning the key missing skills."
    else:
        fit_level = "EARLY STAGE"
        advice = "You're starting your journey. Begin with the core skills below."
    
    recommendation_text = f"""
**Career Path: {career_path}**
**Fit Level: {fit_level} ({percentage}%)**

{advice}

**Your Strengths:**
- You have {len(matching_skills)} core skills matching this role
- Strong foundation in: {', '.join(matching_skills[:3]) if matching_skills else 'developing your skillset'}

**Areas to Improve:**
- Focus on: {', '.join(missing_skills[:3]) if missing_skills else 'advanced topics'}
- Build projects using these technologies
- Take online courses or certifications

**Action Plan:**
1. Learn one missing skill per month
2. Build a portfolio project using new skills
3. Contribute to open-source projects
4. Network with people in this role
"""
    
    return recommendation_text.strip()


@app.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    career_path: str = Form(...)
):
    """Analyze a resume for fit against a specific career path"""
    try:
        file_content = await file.read()
        
        resume_text = extract_text_from_file(file_content, file.filename)
        
        if not resume_text.strip():
            raise ValueError("Could not extract text from resume")
        
        found_skills = extract_skills(resume_text)
        
        target_role_profile = get_role_profile(career_path)
        
        if not target_role_profile:
            raise ValueError(f"Career path '{career_path}' not found")
        
        required_skills = set(target_role_profile.get("core_skills", []))
        found_skills_set = set(found_skills)
        
        matching_skills = list(found_skills_set & required_skills)
        missing_skills = list(required_skills - found_skills_set)
        
        fit_score = len(matching_skills) / len(required_skills) if required_skills else 0
        
        recommendations = generate_recommendations(
            career_path=career_path,
            matching_skills=matching_skills,
            missing_skills=missing_skills,
            fit_score=fit_score
        )
        
        return {
            "fit_score": fit_score,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations,
            "career_path": career_path,
            "found_skills_count": len(found_skills),
            "required_skills_count": len(required_skills)
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@app.get("/")
def home():
    return {"message": "Server is working"}


@app.get("/test")
def test():
    return {"status": "ok"}


@app.get("/health")
def health_check():
    return {"health": "healthy"}