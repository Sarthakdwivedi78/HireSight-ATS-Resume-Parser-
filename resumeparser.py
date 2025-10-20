import re
import spacy
from pdfminer.high_level import extract_text
import os

# --- spaCy Model Loading ---
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print('Downloading language model for spaCy...\n(This will only happen once)')
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

# --- Helper Functions ---

def extract_text_from_pdf(pdf_path):
    """Extracts raw text from a PDF file."""
    return extract_text(pdf_path)

# --- Core Information Extraction Functions ---

def extract_personal_info(text):
    """Extracts name, email, and professional links."""
    header_text = '\n'.join(text.split('\n')[:5])
    doc = nlp(header_text)
    name = next((ent.text for ent in doc.ents if ent.label_ == 'PERSON'), None)
    email = re.search(r'[\w\.-]+@[\w\.-]+', header_text)
    linkedin = re.search(r'linkedin\.com/in/[\w-]+', header_text, re.IGNORECASE)
    github = re.search(r'github\.com/[\w-]+', header_text, re.IGNORECASE)
    return {
        'name': name,
        'email': email.group(0) if email else None,
        'mobile_number': "Not found in header",
        'linkedin': "https://www." + linkedin.group(0) if linkedin else "N/A",
        'github': "https://www." + github.group(0) if github else "N/A",
    }

def parse_education(section_text):
    """A robust function to parse education details, ignoring formatting issues."""
    if not section_text: return []
    education_list = []
    # This regex finds patterns like "2027","M.TECH...", "IIT..." and captures the three parts.
    pattern = re.compile(r'"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"')
    matches = pattern.findall(section_text)
    for match in matches:
        year, degree, institute = match
        education_list.append({
            "year": year.strip(),
            "degree": degree.strip(),
            "institute": institute.strip()
        })
    return education_list

def parse_projects_and_experience(section_text):
    """Parses projects or experience details from its section text."""
    if not section_text: return []
    entries = []
    # Split by a newline followed by an uppercase letter and a word (a likely title)
    entry_blocks = re.split(r'\n(?=[A-Z][a-z])', section_text)
    for block in entry_blocks:
        if not block.strip(): continue
        date_match = re.search(r'(\[.*?\])', block)
        date = date_match.group(1).strip() if date_match else "N/A"
        lines = block.strip().split('\n')
        title = lines[0].strip()
        description_lines = [line.strip() for line in lines[1:] if date not in line]
        description = '\n'.join(description_lines).strip()
        entries.append({'title': title, 'date': date, 'description': description})
    return entries

def extract_skills(section_text):
    """Extracts skills from its section text."""
    if not section_text: return []
    skills_list = []
    for line in section_text.split('\n'):
        if ":" not in line and line.strip():
            skills_list.append(line.strip())
        elif ":" in line:
            parts = line.split(":")
            if len(parts) > 1 and parts[1].strip():
                skills_list.extend([skill.strip() for skill in parts[1].split(',') if skill.strip()])
    return list(set(skills_list))

# --- ATS Scoring Function ---

def calculate_ats_score(data, full_text):
    """Calculates an ATS score based on the completeness and quality of the resume."""
    score = 0
    feedback = []
    
    # Section completion scores
    if data.get('name') and data.get('email'): score += 15
    else: feedback.append("❌ Missing name or email. Ensure they are at the top of your resume.")
        
    if data.get('linkedin') != "N/A" or data.get('github') != "N/A": score += 5
    else: feedback.append("💡 Consider adding links to your LinkedIn or GitHub profiles.")

    if data.get('education'): score += 15
    else: feedback.append("❌ Education section is missing or could not be parsed.")

    if data.get('skills'): score += 20
    else: feedback.append("❌ Skills section is missing. This is a critical section for ATS.")
        
    if data.get('projects'): score += 20
    else: feedback.append("💡 Consider adding a Projects section to showcase your work.")
        
    if data.get('experience'): score += 25
    else: feedback.append("💡 Experience section not found. If you have relevant experience, be sure to include it.")

    # Quality scores based on action verbs
    action_verbs = ['developed', 'led', 'managed', 'created', 'achieved', 'implemented', 'improved', 'spearheaded', 'applied', 'resolved', 'enhanced']
    found_verbs = [verb for verb in action_verbs if verb in full_text.lower()]
    
    if len(found_verbs) > 0:
        score_bonus = min(len(found_verbs) * 2, 10)
        score += score_bonus
    else:
        feedback.append("💡 Strengthen your descriptions with action verbs like 'Developed', 'Managed', or 'Achieved'.")

    score = min(score, 100)

    # Add a summary feedback message
    if not feedback:
        if score >= 85: feedback.insert(0, "✅ Excellent! Your resume is well-optimized for ATS.")
        elif score >= 60: feedback.insert(0, "✅ Your resume is good, but a few tweaks could make it great.")
        else: feedback.insert(0, "⚠️ Your resume needs some work to be ATS-friendly.")
    elif len(feedback) > 0 and score < 85:
         feedback.insert(0, "⚠️ Your resume needs some work to be ATS-friendly.")


    return score, feedback

# --- Main Extractor Function ---

def ats_extractor(resume_path):
    """Orchestrates the extraction and scoring of all details from the resume."""
    try:
        text = extract_text_from_pdf(resume_path)
        
        all_headings = [
            "EDUCATION", "PROJECTS", "COMPETITION/CONFERENCE",
            "ENTREPRENEURIAL EXPERIENCES", "SKILLS AND EXPERTISE",
            "COURSEWORK INFORMATION", "POSITIONS OF RESPONSIBILITY",
            "AWARDS AND ACHIEVEMENTS", "EXTRA CURRICULAR ACTIVITIES"
        ]
        
        # New, more robust section extraction logic
        sections = {}
        heading_pattern = re.compile(rf"^\s*({'|'.join(all_headings)})\s*$", re.MULTILINE | re.IGNORECASE)
        matches = list(heading_pattern.finditer(text))
        
        for i, match in enumerate(matches):
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            section_heading = match.group(1).upper()
            sections[section_heading] = text[start_pos:end_pos].strip()

        data = {
            **extract_personal_info(text),
            'education': parse_education(sections.get("EDUCATION")),
            'skills': extract_skills(sections.get("SKILLS AND EXPERTISE")),
            'projects': parse_projects_and_experience(sections.get("PROJECTS")),
            'experience': parse_projects_and_experience(sections.get("ENTREPRENEURIAL EXPERIENCES")),
        }
        
        score, feedback = calculate_ats_score(data, text)
        data['score'] = score
        data['feedback'] = feedback
        
        return data

    except Exception as e:
        import traceback
        return {"error": f"An unexpected error occurred: {e}\n{traceback.format_exc()}"}

