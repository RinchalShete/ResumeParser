# 📝 Resume Parser App

This is a full-stack application that parses resumes using NLP and displays extracted data through a FastAPI backend and a Streamlit frontend.

---

## 🌐 Live Demo

[Visit the Live Resume Parser API](https://resumeparser-0q6a.onrender.com)

---

## 🚀 Features

- Upload resumes in PDF or DOCX format
- Extract key info like name, email, phone, skills, education, and experience using NLP
- FastAPI backend with interactive Swagger UI at `/docs`
- Streamlit frontend for a clean user interface

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **NLP**: spaCy
- **PDF/Docx Parsing**: `pdfminer.six`, `python-docx`

---

## 🐳 Docker Support

To build and run the app with Docker:

```bash
docker build -t resume-parser-app .
docker run -p 8000:8000 -p 8501:8501 resume-parser-app
```

Access FastAPI docs: http://localhost:8000/docs
Access Streamlit UI: http://localhost:8501

---

## ⚙️ Manual Setup (Without Docker)

### Clone the repo:
```bash
git clone https://github.com/RinchalShete/ResumeParser.git
cd ResumeParser
```

### Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
  
### Run the backend and frontend:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
streamlit run app/ui.py --server.port 8501 --server.enableCORS false
```

---

## ☁️ Deployment on Render (Without Docker)

Use "Web Service", set Python version to 3.11+, and use the following:

### 🔨 Build Command:

```bash
pip install -r requirements.txt
```

### 🚀 Start Command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run app/ui.py --server.port=$PORT --server.enableCORS false --server.address=0.0.0.0
```

Make sure your repository contains:

- requirements.txt
- app/main.py (FastAPI backend)
- app/ui.py (Streamlit frontend)
- (Optional) .gitignore, .dockerignore
  
---
