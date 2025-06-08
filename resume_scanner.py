import streamlit as st
from utils.resume_parser import extract_text_from_pdf, parse_resume
from utils.job_matcher import suggest_job_roles
from utils.ats_scorer import calculate_ats_score
import os

# Set page config for a wide layout and custom page title
st.set_page_config(page_title="Resume Scanner", layout="wide", initial_sidebar_state="expanded")

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar for navigation and branding
with st.sidebar:
    st.image("img001.png", use_column_width=True, caption="RS-Resume-Scanner")
    st.markdown(
        """
        <style>
        img {
            border-radius: 50%;
            object-fit: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<h2 class='sidebar-title'>Resume Scanner</h2>", unsafe_allow_html=True)
    st.markdown("Upload your resume to analyze skills, get job suggestions, and check ATS compatibility.")
    st.markdown("---")
    st.markdown("**Features**")
    st.markdown("- Extract resume details")
    st.markdown("- Suggest job roles")
    st.markdown("- Calculate ATS score")
    st.markdown("---")
    st.markdown("<p class='sidebar-footer'>Powered by RS</p>", unsafe_allow_html=True)

# Main content with background overlay
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>Resume Scanner</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Upload your resume (PDF) to unlock personalized insights and optimize your job search.</p>", unsafe_allow_html=True)

# File uploader with custom styling
st.markdown("<div class='upload-container'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose your resume (PDF)", type=["pdf"], help="Upload a PDF file to start the analysis", key="file_uploader")
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    # Container for analysis results
    with st.container():
        st.markdown("<div class='result-container'>", unsafe_allow_html=True)
        with st.spinner("Analyzing your resume..."):
            text = extract_text_from_pdf(uploaded_file)
            resume_data = parse_resume(text)

            # Extracted Resume Details
            st.markdown("<h2 class='section-title'>Extracted Resume Details</h2>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
            with col1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<h3 class='card-title'>Skills</h3>", unsafe_allow_html=True)
                skills = ", ".join(resume_data["skills"]) if resume_data["skills"] else "None found"
                st.markdown(f"<p class='card-content'>{skills}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<h3 class='card-title'>Education</h3>", unsafe_allow_html=True)
                education = "<br>".join(resume_data["education"]) if resume_data["education"] else "None found"
                st.markdown(f"<p class='card-content'>{education}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with col3:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<h3 class='card-title'>Experience</h3>", unsafe_allow_html=True)
                experience = "<br>".join(resume_data["experience"]) if resume_data["experience"] else "None found"
                st.markdown(f"<p class='card-content'>{experience}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Job Role Suggestions
            st.markdown("<h2 class='section-title'>Suggested Job Roles</h2>", unsafe_allow_html=True)
            suggestions = suggest_job_roles(resume_data["skills"])
            if suggestions:
                for suggestion in suggestions:
                    st.markdown("<div class='suggestion-card'>", unsafe_allow_html=True)
                    st.markdown(f"<h3 class='suggestion-title'>{suggestion['role']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p class='suggestion-score'>Match Score: {suggestion['match_score']}%</p>", unsafe_allow_html=True)
                    matched_skills = ", ".join(suggestion['matched_skills'])
                    st.markdown(f"<p class='suggestion-content'>Matched Skills: {matched_skills}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='no-results'>No suitable job roles found based on your skills.</p>", unsafe_allow_html=True)

            # ATS Friendliness Score
            st.markdown("<h2 class='section-title'>ATS Friendliness Score</h2>", unsafe_allow_html=True)
            ats_score = calculate_ats_score(text, resume_data["skills"])
            st.markdown("<div class='ats-container'>", unsafe_allow_html=True)
            st.progress(ats_score / 100)
            st.markdown(f"<p class='ats-score'>Your resume is <strong>{ats_score}%</strong> ATS-friendly.</p>", unsafe_allow_html=True)
            if ats_score < 60:
                st.markdown("<div class='alert warning'>Consider adding more relevant keywords and clear section headings.</div>", unsafe_allow_html=True)
            elif ats_score < 80:
                st.markdown("<div class='alert info'>Good, but you can improve by optimizing keywords and formatting.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='alert success'>Excellent! Your resume is highly ATS-friendly.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>© Y Naga Teja Reddy. All rights reserved.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # Close main-container