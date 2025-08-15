# AI Career Navigator - Python FastAPI Backend
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import re
import json
from typing import Dict, List
import spacy
from docx import Document
import fitz  # PyMuPDF
import io

# Initialize FastAPI app
app = FastAPI(title="AI Career Navigator", description="Resume Analysis API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy model (download with: python -m spacy download en_core_web_sm)
try:
    nlp = spacy.load("en_core_web_sm")
except (OSError, IOError):
    print("spaCy English model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None

class ResumeAnalyzer:
    def __init__(self):
        # Comprehensive skill database organized by categories
        self.skill_categories = {
            "programming": [
                "javascript", "typescript", "python", "java", "c++", "c#", "php", 
                "ruby", "go", "rust", "swift", "kotlin", "scala", "r", "matlab"
            ],
            "frontend": [
                "react", "angular", "vue", "svelte", "html", "css", "sass", "less", 
                "tailwind", "bootstrap", "jquery", "webpack", "vite", "parcel"
            ],
            "backend": [
                "node.js", "express", "django", "flask", "fastapi", "spring", 
                "laravel", "rails", "asp.net", "nestjs", "koa", "gin"
            ],
            "databases": [
                "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", 
                "oracle", "sqlite", "cassandra", "dynamodb", "firebase"
            ],
            "cloud": [
                "aws", "azure", "gcp", "docker", "kubernetes", "heroku", 
                "netlify", "vercel", "digitalocean", "linode", "terraform"
            ],
            "tools": [
                "git", "github", "gitlab", "bitbucket", "jenkins", "circleci", 
                "travis", "npm", "yarn", "pip", "maven", "gradle", "jira"
            ],
            "methodologies": [
                "agile", "scrum", "kanban", "devops", "ci/cd", "tdd", "bdd", 
                "microservices", "rest", "graphql", "oauth", "jwt"
            ],
            "data_science": [
                "machine learning", "deep learning", "ai", "tensorflow", "pytorch", 
                "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "jupyter"
            ]
        }
        
        self.all_skills = [skill for skills in self.skill_categories.values() for skill in skills]
        
        # Strong action verbs that indicate leadership and achievement
        self.action_verbs = [
            "achieved", "developed", "implemented", "managed", "led", "created", 
            "designed", "built", "optimized", "improved", "increased", "reduced", 
            "streamlined", "automated", "delivered", "coordinated", "established", 
            "launched", "transformed", "architected", "pioneered", "spearheaded",
            "executed", "directed", "supervised", "mentored", "collaborated"
        ]
        
        # Industry keywords that show domain knowledge
        self.industry_keywords = [
            "software", "development", "engineering", "programming", "coding", 
            "algorithm", "database", "api", "frontend", "backend", "fullstack", 
            "devops", "cloud", "machine learning", "ai", "data science", 
            "analytics", "testing", "debugging", "security", "performance"
        ]

    def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        """Extract text from different file formats"""
        try:
            if filename.lower().endswith('.txt'):
                return file_content.decode('utf-8')
            
            elif filename.lower().endswith('.docx'):
                doc = Document(io.BytesIO(file_content))
                text = []
                for paragraph in doc.paragraphs:
                    text.append(paragraph.text)
                return '\n'.join(text)
            
            elif filename.lower().endswith('.pdf'):
                pdf_document = fitz.open(stream=file_content, filetype="pdf")
                text = []
                for page_num in range(len(pdf_document)):
                    page = pdf_document.load_page(page_num)
                    text.append(page.get_text())
                pdf_document.close()
                return '\n'.join(text)
            
            else:
                raise ValueError("Unsupported file format")
                
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error extracting text: {str(e)}")

    def detect_skills(self, text: str) -> List[str]:
        """Detect technical skills using regex and spaCy"""
        text_lower = text.lower()
        found_skills = []
        
        # Basic regex matching
        for skill in self.all_skills:
            # Create word boundary regex for better matching
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        # Enhanced skill detection using spaCy if available
        if nlp:
            doc = nlp(text)
            # Extract additional technical terms
            for token in doc:
                if (token.pos_ in ['NOUN', 'PROPN'] and 
                    len(token.text) > 2 and 
                    token.text.lower() not in found_skills):
                    # Check if it matches common tech patterns
                    if any(pattern in token.text.lower() for pattern in ['js', 'sql', 'api', 'ui', 'ux']):
                        found_skills.append(token.text.lower())
        
        return list(set(found_skills))  # Remove duplicates

    def analyze_contact_info(self, text: str) -> int:
        """Analyze contact information completeness (max 20 points)"""
        score = 0
        
        # Email detection
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, text):
            score += 5
        
        # Phone number detection
        phone_pattern = r'(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}'
        if re.search(phone_pattern, text):
            score += 5
        
        # LinkedIn profile
        if re.search(r'linkedin\.com/in/[\w-]+', text, re.IGNORECASE):
            score += 5
        
        # GitHub profile
        if re.search(r'github\.com/[\w-]+', text, re.IGNORECASE):
            score += 5
        
        return score

    def analyze_experience_quality(self, text: str) -> int:
        """Analyze experience descriptions quality (max 25 points)"""
        action_verb_count = 0
        
        for verb in self.action_verbs:
            pattern = r'\b' + re.escape(verb) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                action_verb_count += 1
        
        # Cap at reasonable maximum
        return min(action_verb_count * 2, 25)

    def analyze_skills_relevance(self, skills: List[str]) -> int:
        """Analyze skill relevance and diversity (max 20 points)"""
        skill_diversity = set()
        
        # Check which categories are represented
        for category, category_skills in self.skill_categories.items():
            category_found = [skill for skill in skills if skill in category_skills]
            if category_found:
                skill_diversity.add(category)
        
        # Base score from diversity + skill count
        diversity_score = len(skill_diversity) * 3
        skill_count_score = min(len(skills), 8)  # Max 8 points from skill count
        
        return min(diversity_score + skill_count_score, 20)

    def analyze_achievements(self, text: str) -> int:
        """Analyze quantifiable achievements (max 20 points)"""
        achievement_patterns = [
            r'\d+%',           # percentages
            r'\$[\d,]+',       # money amounts
            r'\d+\+',          # numbers with plus
            r'\d+k\+?',        # thousands
            r'\d+m\+?',        # millions
            r'\d+x',           # multipliers
            r'\d+ (?:users?|customers?|clients?|projects?|teams?|people|years?)'
        ]
        
        achievement_count = 0
        for pattern in achievement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            achievement_count += len(matches)
        
        return min(achievement_count * 3, 20)

    def analyze_formatting(self, text: str) -> int:
        """Analyze resume formatting and structure (max 10 points)"""
        score = 0
        words = text.split()
        
        # Check for section headers
        section_headers = r'\b(?:experience|education|skills|projects|work history|summary|objective)\b'
        if re.search(section_headers, text, re.IGNORECASE):
            score += 3
        
        # Check for bullet points or structured lists
        if re.search(r'[•\*\-]', text):
            score += 2
        
        # Check for appropriate length
        if 100 <= len(words) <= 800:
            score += 3
        
        # Check for consistent date formatting
        if re.search(r'\d{4}', text):
            score += 2
        
        return score

    def analyze_keywords(self, text: str) -> int:
        """Analyze industry keyword usage (max 5 points)"""
        keyword_count = 0
        
        for keyword in self.industry_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                keyword_count += 1
        
        return min(keyword_count, 5)

    def generate_suggestions(self, scores: Dict[str, int], skills: List[str], text: str) -> List[str]:
        """Generate personalized improvement suggestions"""
        suggestions = []
        words = text.split()
        
        if scores['contact_info'] < 15:
            suggestions.append("Add complete contact information including email, phone, LinkedIn, and GitHub profiles")
        
        if scores['experience_quality'] < 15:
            suggestions.append("Use stronger action verbs to describe your accomplishments (e.g., 'achieved', 'developed', 'led')")
        
        if scores['skills_relevance'] < 15:
            suggestions.append("Include more relevant technical skills and diversify across different technology categories")
        
        if scores['achievements'] < 12:
            suggestions.append("Add quantifiable achievements with specific numbers, percentages, or metrics")
        
        if scores['formatting'] < 7:
            suggestions.append("Improve resume structure with clear headers, bullet points, and consistent formatting")
        
        if len(skills) < 5:
            suggestions.append("Add more technical skills relevant to your target position")
        
        if len(words) < 100:
            suggestions.append("Expand your resume with more detailed descriptions of your experience and projects")
        
        if len(words) > 800:
            suggestions.append("Consider condensing your resume to focus on the most relevant and impactful information")
        
        # Positive feedback for high scores
        total_score = sum(scores.values())
        if total_score >= 80:
            suggestions.insert(0, "Excellent resume! Consider tailoring it further for specific job applications")
        elif total_score >= 60:
            suggestions.insert(0, "Good foundation! A few improvements will make your resume stand out")
        
        return suggestions[:6]  # Limit to 6 suggestions

    def analyze(self, text: str) -> Dict:
        """Main analysis function"""
        # Detect skills
        skills = self.detect_skills(text)
        
        # Calculate individual scores
        scores = {
            'contact_info': self.analyze_contact_info(text),
            'experience_quality': self.analyze_experience_quality(text),
            'skills_relevance': self.analyze_skills_relevance(skills),
            'achievements': self.analyze_achievements(text),
            'formatting': self.analyze_formatting(text),
            'keywords': self.analyze_keywords(text)
        }
        
        total_score = sum(scores.values())
        words = text.split()
        
        # Generate suggestions
        suggestions = self.generate_suggestions(scores, skills, text)
        
        # Create summary
        action_verb_count = len([v for v in self.action_verbs if v in text.lower()])
        quant_achievements = len(re.findall(r'\d+[%+]|[$][\d,]+', text))
        summary = (
            f"Analysis complete: {len(skills)} skills detected, "
            f"{action_verb_count} action verbs found, "
            f"{quant_achievements} quantifiable achievements "
            f"identified across {len(words)} words."
        )
        return {
            'score': total_score,
            'skills': skills[:15],  # Top 15 skills
            'suggestions': suggestions,
            'summary': summary,
            'details': scores
        }

# Initialize analyzer
analyzer = ResumeAnalyzer()

@app.post("/analyze_resume")
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze uploaded resume file and return comprehensive scoring and suggestions
    """
    try:
        # Validate file type
        allowed_types = ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file type. Please upload a .txt, .pdf, or .docx file"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Extract text from file
        text = analyzer.extract_text_from_file(file_content, file.filename)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text content found in the file")
        
        # Analyze the resume
        result = analyzer.analyze(text)
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Career Navigator API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "spacy_loaded": nlp is not None,
        "supported_formats": [".txt", ".pdf", ".docx"]
    }

@app.get("/stats")
async def stats():
    """
    Returns real model stats for frontend display.
    """
    # Replace these with your actual backend stats
    return {
        "accuracy_rate": 92.3,         # Example: 92.3%
        "resumes_analyzed": "12,345",  # Example: 12,345
        "user_rating": 4.7             # Example: 4.7
    }

if __name__ == "__main__":
    import uvicorn
    # Run FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)