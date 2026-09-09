import streamlit as st
from pypdf import PdfReader
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("🚀 AI-Powered Resume Analyzer")
st.write("Upload a resume and a target job description to get technical recruitment feedback.")

# Retrieve API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Missing Gemini API Key. Please add it to your .env file.")
    st.stop()

# Initialize the official Google GenAI client
client = genai.Client(api_key=api_key)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

with col2:
    st.subheader("2. Target Job")
    job_description = st.text_area(
        "Paste Job Description (Optional)", 
        height=150,
        placeholder="e.g., Looking for a Software Engineer with Python and SQL experience..."
    )

if st.button("Analyze Resume", type="primary"):
    if uploaded_file:
        with st.spinner("Reading PDF and generating insights..."):
            try:
                # Extract text from the uploaded PDF
                reader = PdfReader(uploaded_file)
                resume_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                
                # Construct the prompt dynamically
                if job_description.strip():
                    prompt = f"""
                    Act as a Senior Technical Recruiter. Compare the following resume to the job description.
                    
                    Job Description:
                    {job_description}
                    
                    Resume Text:
                    {resume_text}
                    
                    Please provide:
                    1. **Match Percentage**: Estimated fit.
                    2. **Key Alignments**: Where the candidate's skills match perfectly.
                    3. **Skill Gaps**: Missing keywords or technologies.
                    4. **Actionable Feedback**: How to improve this resume for this specific role.
                    """
                else:
                    prompt = f"""
                    Act as an expert Career Coach. Review the following resume and provide constructive feedback.
                    
                    Resume Text:
                    {resume_text}
                    
                    Please provide:
                    1. **Overall Impression**: Professional summary.
                    2. **Strengths**: What stands out.
                    3. **Areas for Improvement**: Formatting, phrasing, or missing metrics.
                    4. **Recommended Roles**: Top 3 job titles this candidate is best suited for.
                    """

                # Call Gemini 3.6 Flash
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                
                # Display the AI's response
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
    else:
        st.warning("⚠️ Please upload a resume PDF first.")