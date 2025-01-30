import streamlit as st
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from utils.file_processors import read_file_text
from utils.prompt_templates import create_analysis_prompt
from utils.visualizations import (
    create_match_gauge,
    create_skills_pie,
    create_improvement_radar
)
from utils.response_parser import parse_gemini_response

# Load environment variables and configure Gemini AI
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    try:
        model = genai.GenerativeModel('gemini-pro')
        generation_config = genai.types.GenerationConfig(
            temperature=0,
            top_p=1,
            top_k=1,
            max_output_tokens=2048
        )
        
        # Add a safety prefix to ensure JSON-only response
        safety_prefix = "Respond ONLY with valid JSON. No other text, explanations, or formatting."
        full_prompt = safety_prefix + "\n" + input
        
        response = model.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        
        if not response.text:
            raise ValueError("Empty response received from Gemini")
            
        return response.text.strip()
    except Exception as e:
        st.error(f"Error in Gemini response: {str(e)}")
        return None

def load_css():
    with open('static/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Page Configuration
st.set_page_config(
    page_title="JobFitAI - Smart Resume Analyzer",
    page_icon="🎯",
    layout="wide"
)

# Load CSS
load_css()

# Main App Header
st.title("🎯 JobFitAI")
st.markdown("### Your AI Career Optimization Companion")

# Create main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📄 Resume Analysis", "📊 Insights", "🎯 Interview Prep", "🏢 Industry Focus"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Your Resume",
            type=["pdf", "docx", "doc"],
            help="Supported formats: PDF, Word documents"
        )
        
    with col2:
        jd = st.text_area("Paste the Job Description", height=200)

    if uploaded_file:
        with st.expander("📄 Resume Preview"):
            resume_text = read_file_text(uploaded_file)
            st.text(resume_text)

    analyze_button = st.button("🔍 Analyze Resume")

    if analyze_button and uploaded_file and jd:
        with st.spinner("🔄 Analyzing your resume... Please wait..."):
            try:
                text = read_file_text(uploaded_file)
                response = get_gemini_response(create_analysis_prompt(text, jd))
                
                if response:
                    analysis = parse_gemini_response(response)
                    
                    if analysis:
                        st.session_state['analysis'] = analysis
                        st.success("✨ Analysis Complete!")
                        
                        # Display Industry Context
                        st.markdown("### 🏢 Industry Context")
                        industry_context = analysis.get("Industry_Context", {})
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Domain:**", industry_context.get("Domain", "N/A"))
                        with col2:
                            st.write("**Role Type:**", industry_context.get("Role_Type", "N/A"))
                        
                        # Display Match Score
                        st.markdown("### 📊 Match Analysis")
                        match_fig = create_match_gauge(analysis.get("JD_Match", "0%"))
                        st.plotly_chart(match_fig, use_container_width=True)
                        
                        # Display Profile Summary
                        st.markdown("### 📋 Profile Summary")
                        st.write(analysis.get("Profile_Summary", "No profile summary available"))
                        
                        # Display Keyword Analysis
                        st.markdown("### 🔑 Keyword Analysis")
                        keywords_analysis = analysis.get("Keywords_Analysis", {})
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("#### Missing Keywords")
                            missing_keywords = keywords_analysis.get("Missing_Keywords", [])
                            for kw in missing_keywords:
                                importance_color = {
                                    "high": "🔴",
                                    "medium": "🟡",
                                    "low": "🟢"
                                }.get(kw.get("importance", "medium"), "⚪")
                                st.markdown(f"{importance_color} **{kw['keyword']}** ({kw['category']})")

                        with col2:
                            st.markdown("#### Present Keywords")
                            present_keywords = keywords_analysis.get("Present_Keywords", [])
                            for kw in present_keywords:
                                st.markdown(f"✅ **{kw['keyword']}** - {kw['match_context']}")
                    else:
                        st.error("Failed to parse the analysis response")
                else:
                    st.error("Failed to get response from Gemini")
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.error("Please try again with a different resume or job description")

with tab2:
    if 'analysis' in st.session_state:
        analysis = st.session_state['analysis']
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🎯 Match Analysis")
            match_analysis = analysis.get("Match_Analysis", {})
            st.write(match_analysis.get("Reasoning", "No analysis available"))
            
            st.markdown("### 💪 Strength Areas")
            strengths = match_analysis.get("Strength_Areas", [])
            if strengths:
                for strength in strengths:
                    st.markdown(f"- {strength}")
            else:
                st.info("No specific strengths identified")
            
        with col2:
            st.markdown("### 🔄 Areas for Improvement")
            improvement_areas = match_analysis.get("Improvement_Areas", [])
            if improvement_areas:
                for area in improvement_areas:
                    st.markdown(f"- {area}")
                
                # Create and display improvement areas chart
                improvement_fig = create_improvement_radar(improvement_areas)
                if improvement_fig:
                    st.plotly_chart(improvement_fig, use_container_width=True)
            else:
                st.info("No specific improvement areas identified")

        # Skills Analysis Section with enhanced error handling
        st.markdown("### 💪 Skills Analysis")
        role_analysis = analysis.get("Role_Analysis", {})
        required_skills = role_analysis.get("Required_Skills", [])
        present_skills = role_analysis.get("Present_Skills", [])
        
        if required_skills and present_skills:
            skills_fig = create_skills_pie(required_skills, present_skills)
            if skills_fig:
                st.plotly_chart(skills_fig, use_container_width=True)
                
                # Add skills comparison table
                st.markdown("#### Skills Breakdown")
                cols = st.columns(2)
                with cols[0]:
                    st.markdown("**Required Skills**")
                    for skill in required_skills:
                        if skill in present_skills:
                            st.markdown(f"✅ {skill}")
                        else:
                            st.markdown(f"❌ {skill}")
                with cols[1]:
                    st.markdown("**Present Skills**")
                    for skill in present_skills:
                        st.markdown(f"✓ {skill}")
        else:
            st.info("Unable to generate skills analysis due to insufficient data")

        # Resume Enhancement Section
        st.markdown("### 📝 Resume Enhancement Tips")
        enhancement = analysis.get("Resume_Enhancement", {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Industry Alignment")
            alignments = enhancement.get("Industry_Alignment", [])
            if alignments:
                for tip in alignments:
                    st.markdown(f"- {tip}")
            
            st.markdown("#### Keyword Placement")
            placements = enhancement.get("Keyword_Placement", [])
            if placements:
                for suggestion in placements:
                    st.markdown(f"- {suggestion}")
            
        with col2:
            st.markdown("#### Strategic Tips")
            tips = enhancement.get("Strategic_Tips", [])
            if tips:
                for tip in tips:
                    st.markdown(f"- {tip}")
            
            st.markdown("#### Format Suggestions")
            formats = enhancement.get("Format_Suggestions", [])
            if formats:
                for suggestion in formats:
                    st.markdown(f"- {suggestion}")

with tab3:
    if 'analysis' in st.session_state:
        analysis = st.session_state['analysis']
        interview_prep = analysis.get("Interview_Prep", {})
        
        st.markdown("### 🎯 Interview Preparation")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Industry Knowledge")
            for knowledge in interview_prep.get("Industry_Knowledge", []):
                st.markdown(f"- {knowledge}")
                
            st.markdown("#### Technical Topics")
            for topic in interview_prep.get("Technical_Topics", []):
                st.markdown(f"- {topic}")
                
        with col2:
            st.markdown("#### Common Questions")
            for question in interview_prep.get("Common_Questions", []):
                st.markdown(f"- {question}")
                
            st.markdown("#### Practice Tips")
            for tip in interview_prep.get("Practice_Tips", []):
                st.markdown(f"- {tip}")
        
        st.markdown("### 📚 Study Resources")
        for resource in interview_prep.get("Study_Resources", []):
            st.markdown(f"- {resource}")

with tab4:
    if 'analysis' in st.session_state:
        analysis = st.session_state['analysis']
        
        st.markdown("### 📈 Industry-Specific Metrics")
        metrics = analysis.get("Industry_Specific_Metrics", {})
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🎯 Key Performance Indicators")
            for kpi in metrics.get("Key_Performance_Indicators", []):
                st.markdown(f"- {kpi}")
                
        with col2:
            st.markdown("#### 📜 Recommended Certifications")
            for cert in metrics.get("Certifications", []):
                st.markdown(f"- {cert}")
                
        with col3:
            st.markdown("#### 🛠️ Tools & Software")
            for tool in metrics.get("Tools_And_Software", []):
                st.markdown(f"- {tool}")
        
        st.markdown("### 🚀 Career Growth Opportunities")
        for path in analysis.get("Role_Analysis", {}).get("Career_Growth", []):
            st.markdown(f"- {path}")
            
        st.markdown("### 🌐 Industry Insights")
        for insight in analysis.get("Role_Analysis", {}).get("Industry_Insights", []):
            st.markdown(f"- {insight}")