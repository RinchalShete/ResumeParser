import streamlit as st 
import requests
import pandas as pd
import re

st.set_page_config(layout="wide")

# Custom CSS to improve readability and allow scrolling
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 18px !important;
    }
    h1 {
        font-size: 42px !important;
        color: skyblue !important;
    }
    .stDataFrame div {
        font-size: 16px !important;
    }
    [data-testid="stDataFrame"] table tbody tr td {
        white-space: normal !important;
        padding-top: 1.5em !important;
        padding-bottom: 1.5em !important;
        overflow-x: auto !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Resume Parser</h1>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload your resumes", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    files = [("files", (f.name, f, f.type)) for f in uploaded_files]
    response = requests.post("http://127.0.0.1:8000/upload/", files=files)

    if response.status_code == 200:
        st.success("Resumes parsed successfully!")
        result = response.json()

        def clean_text(text):
            return re.sub(r'[^\w\s.,;:!?/@-]', '', str(text)).strip()

        def join_non_empty(values):
            filtered = [v for v in values if v and str(v).strip() != '']
            return ", ".join(filtered)

        def format_bullets_html(items, limit=5):
            formatted = [f"• {join_non_empty(clean_text(str(v)) for v in entry.values())}" 
                         for entry in items[:limit]]
            return "<br>".join(formatted)  # HTML line breaks

        all_resumes = []
        for item in result['results']:
            data = item.get('data', {})
            all_resumes.append({
                "Filename": clean_text(item.get("filename", "Unknown")),
                "Name": clean_text(data.get("name", "")),
                "Email": clean_text(data.get("email", "")),
                "Phone": clean_text(data.get("phone", "")),
                "Skills": clean_text(", ".join(data.get("skills", []))),
                "Education": format_bullets_html(data.get("education", [])),
                "Experience": format_bullets_html(data.get("experience", []))
            })

        df = pd.DataFrame(all_resumes)

        st.write("### Parsed Resumes")

        # Use st.markdown to render the final formatted HTML table
        st.markdown(
            df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )
      
    else:
        st.error(f"Failed to parse resumes: {response.text}")