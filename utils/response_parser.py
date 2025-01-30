import json
import streamlit as st
import re

def get_default_response():
    """Return a default response structure when parsing fails."""
    return {
        "Industry_Context": {
            "Domain": "Unknown",
            "Role_Type": "Unknown",
            "Industry_Specific_Requirements": []
        },
        "JD_Match": "0%",
        "Match_Analysis": {
            "Score": "0%",
            "Reasoning": "Unable to analyze resume",
            "Strength_Areas": [],
            "Improvement_Areas": []
        },
        "Keywords_Analysis": {
            "Missing_Keywords": [
                {
                    "keyword": "Unable to analyze",
                    "category": "unknown",
                    "importance": "medium"
                }
            ],
            "Present_Keywords": []
        },
        "Profile_Summary": "Error in analysis",
        "Resume_Enhancement": {
            "Industry_Alignment": [],
            "Strategic_Tips": [],
            "Keyword_Placement": [],
            "Format_Suggestions": []
        },
        "Interview_Prep": {
            "Industry_Knowledge": [],
            "Technical_Topics": [],
            "Common_Questions": [],
            "Study_Resources": [],
            "Practice_Tips": []
        },
        "Role_Analysis": {
            "Core_Responsibilities": [],
            "Required_Skills": [],
            "Present_Skills": [],
            "Learning_Path": [],
            "Industry_Insights": [],
            "Career_Growth": []
        },
        "Industry_Specific_Metrics": {
            "Key_Performance_Indicators": [],
            "Certifications": [],
            "Tools_And_Software": []
        }
    }

def clean_json_string(json_str):
    """Clean and format the JSON string for parsing."""
    try:
        # Find the first { and last }
        start_idx = json_str.find('{')
        end_idx = json_str.rindex('}') + 1
        
        if start_idx == -1 or end_idx == -1:
            raise ValueError("No valid JSON object found in response")
            
        json_str = json_str[start_idx:end_idx]
        
        # Remove any escaped characters
        json_str = json_str.replace('\\"', '"')
        json_str = json_str.replace('\\n', ' ')
        
        # Remove trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        return json_str
    except Exception as e:
        st.error(f"Error cleaning JSON string: {str(e)}")
        raise

def parse_gemini_response(response):
    if not response:
        st.error("No response received from the model")
        return get_default_response()
    
    try:
        # Add debug information
        with st.expander("Debug Information"):
            st.text("Raw Response:")
            st.code(response, language='json')
        
        # Clean the response
        cleaned_response = clean_json_string(response)
        
        # Add cleaned response to debug
        with st.expander("Cleaned Response"):
            st.code(cleaned_response, language='json')
        
        # Parse JSON
        try:
            parsed_response = json.loads(cleaned_response)
        except json.JSONDecodeError as je:
            st.error(f"JSON Parse Error at position {je.pos}: {je.msg}")
            st.error("Problematic character: " + cleaned_response[je.pos-10:je.pos+10])
            raise
        
        # Verify structure
        required_keys = [
            "Industry_Context",
            "JD_Match",
            "Match_Analysis",
            "Keywords_Analysis",
            "Profile_Summary",
            "Resume_Enhancement",
            "Interview_Prep",
            "Role_Analysis",
            "Industry_Specific_Metrics"
        ]
        
        missing_keys = [key for key in required_keys if key not in parsed_response]
        
        if missing_keys:
            st.warning(f"Missing keys in response: {', '.join(missing_keys)}")
            default_response = get_default_response()
            for key in missing_keys:
                parsed_response[key] = default_response[key]
        
        return parsed_response
        
    except Exception as e:
        st.error(f"Error parsing response: {str(e)}")
        return get_default_response()
