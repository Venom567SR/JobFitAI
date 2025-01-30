def create_analysis_prompt(text, jd):
    return f"""
    Act as an advanced ATS (Applicant Tracking System) with comprehensive expertise across all professional domains. 
    Analyze the resume against the job description while considering current market trends and industry-specific requirements.
    
    Resume: {text}
    Job Description: {jd}
    
    First, carefully identify and analyze:
    1. Essential keywords from the job description (including skills, qualifications, tools, and technologies)
    2. Industry-specific terminology and requirements
    3. Required certifications, qualifications, and experience
    4. Key responsibilities and performance indicators
    5. Current market trends and industry standards
    
    You MUST respond ONLY with a valid JSON object in the exact format shown below. Do not include any other text or explanation:

    {{
        "Industry_Context": {{
            "Domain": "Primary industry domain",
            "Role_Type": "Role category",
            "Industry_Specific_Requirements": [
                "Clear, specific requirements from JD"
            ]
        }},
        "JD_Match": "XX%",
        "Match_Analysis": {{
            "Score": "XX%",
            "Reasoning": "Clear explanation of match score based on industry standards",
            "Strength_Areas": [
                "Specific strength with evidence"
            ],
            "Improvement_Areas": [
                "Specific area needing improvement"
            ]
        }},
        "Keywords_Analysis": {{
            "Missing_Keywords": [
                {{
                    "keyword": "Specific missing keyword",
                    "category": "skill|tool|qualification|certification",
                    "importance": "high|medium|low",
                    "suggestion": "How and where to add this keyword"
                }}
            ],
            "Present_Keywords": [
                {{
                    "keyword": "Specific present keyword",
                    "category": "skill|tool|qualification|certification",
                    "match_context": "How it appears in resume",
                    "alignment": "How well it aligns with JD requirements"
                }}
            ]
        }},
        "Profile_Summary": "Detailed profile summary highlighting industry-relevant experience and qualifications",
        "Resume_Enhancement": {{
            "Industry_Alignment": [
                "Specific alignment suggestion with industry standards"
            ],
            "Strategic_Tips": [
                "Actionable improvement tip with clear implementation steps"
            ],
            "Keyword_Placement": [
                "Specific section and context for keyword placement"
            ],
            "Format_Suggestions": [
                "Industry-standard format improvement with examples"
            ]
        }},
        "Interview_Prep": {{
            "Industry_Knowledge": [
                "Specific industry topic with current trends"
            ],
            "Technical_Topics": [
                "Specific technical topic with preparation resources"
            ],
            "Common_Questions": [
                "Specific question with suggested answer structure"
            ],
            "Study_Resources": [
                "Specific resource with direct links or references"
            ],
            "Practice_Tips": [
                "Specific practice tip with implementation steps"
            ]
        }},
        "Role_Analysis": {{
            "Core_Responsibilities": [
                "Specific responsibility with success metrics"
            ],
            "Required_Skills": [
                "Specific required skill with proficiency level"
            ],
            "Present_Skills": [
                "Specific skill found in resume with evidence"
            ],
            "Learning_Path": [
                "Specific learning suggestion with resources"
            ],
            "Industry_Insights": [
                "Specific industry insight with market context"
            ],
            "Career_Growth": [
                "Specific growth path with timeline and milestones"
            ]
        }},
        "Industry_Specific_Metrics": {{
            "Key_Performance_Indicators": [
                "Specific KPI with measurement criteria"
            ],
            "Certifications": [
                "Specific certification with validity and importance"
            ],
            "Tools_And_Software": [
                "Specific tool with proficiency requirement"
            ]
        }}
    }}
    
    Ensure to provide:
    1. Specific, actionable insights with clear implementation steps
    2. Evidence-based analysis referencing both resume and job description
    3. Industry-specific context for all suggestions
    4. Clear prioritization of missing keywords and improvements
    5. Practical, achievable enhancement recommendations
    """
