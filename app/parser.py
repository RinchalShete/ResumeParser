import re
from pdfminer.high_level import extract_text
import docx

def extract_text_from_pdf(file_path):
    return extract_text(file_path)

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return '\n'.join([p.text for p in doc.paragraphs])

def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group() if match else None

def extract_phone(text):
    # Basic Indian phone format + country code optional
    match = re.search(r'(\+?\d{1,3}[-.\s]?)?(\d{10})', text)
    if match:
        return match.group()
    return None

def extract_name(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        name_line = lines[0]
        name_line = re.sub(r'^(name\s*[:\-]?\s*)', '', name_line, flags=re.IGNORECASE).strip()
        return name_line
    return "Unknown"

def extract_skills(text):
    # Example skill list, add more as needed
    skills_list = ["Python", "FastAPI", "MongoDB", "Django", "Flask", "JavaScript", "React", "SQL"]
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    return found_skills

def extract_education(text):
    # Very basic heuristic: find lines containing degree keywords
    education = []
    lines = text.split('\n')
    for line in lines:
        if any(keyword in line.lower() for keyword in ["b.tech", "bachelor", "m.tech", "master", "degree", "university", "college"]):
            education.append({
                "degree": line.strip(),
                "college": "",   # You can add logic to extract college separately
                "year": ""       # Year extraction can be added similarly
            })
    return education

def extract_experience(text):
    # Basic heuristic: lines containing job titles or experience keywords
    experience = []
    lines = text.split('\n')
    for line in lines:
        if any(keyword in line.lower() for keyword in ["intern", "developer", "engineer", "expert", "manager", "consultant"]):
            experience.append({
                "company": "",  # Could add more parsing to get company name
                "role": line.strip(),
                "duration": ""  # Duration extraction can be added
            })
    return experience

def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }
