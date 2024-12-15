import streamlit as st
import json
import os
from datetime import datetime
from utils.student_data import save_student_data, read_student_data
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='counselor_app.log'
)

class CounselorWorkflow:
    def __init__(self):
        # Initialize session state for tracking workflow progress
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 0
        if 'student_data' not in st.session_state:
            st.session_state.student_data = {}

    def step_student_input(self):
        """Step 1: Collect Student Information"""
        st.header("🎓 Student Information Collection")
        
        # Personal Details
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", key="name")
        with col2:
            email = st.text_input("Email Address", key="email")
        
        # Academic Details
        st.subheader("Academic Background")
        col1, col2 = st.columns(2)
        with col1:
            tenth_percentage = st.number_input("10th Percentage", min_value=0.0, max_value=100.0, step=0.1, key="tenth_percentage")
            btech_college = st.text_input("B.Tech College Name", key="btech_college")
        
        with col2:
            twelfth_percentage = st.number_input("12th Percentage", min_value=0.0, max_value=100.0, step=0.1, key="twelfth_percentage")
            btech_cgpa = st.number_input("B.Tech CGPA", min_value=0.0, max_value=10.0, step=0.1, key="btech_cgpa")
        
        # Study Preferences
        st.subheader("Study Preferences")
        col1, col2 = st.columns(2)
        with col1:
            preferred_countries = st.multiselect(
                "Preferred Study Destinations", 
                ["Australia", "Canada", "USA", "UK", "Germany"], 
                key="preferred_countries"
            )
        
        with col2:
            preferred_course = st.selectbox(
                "Preferred Course", 
                ["M.Tech in Artificial Intelligence", "M.Tech in Computer Science", "M.Tech in Data Science"],
                key="preferred_course"
            )
        
        # Standardized Test Scores
        st.subheader("Test Scores")
        col1, col2 = st.columns(2)
        with col1:
            ielts_score = st.number_input("IELTS Score", min_value=0.0, max_value=9.0, step=0.1, key="ielts_score")
        
        with col2:
            gre_score = st.number_input("GRE Score", min_value=0, max_value=340, key="gre_score")
        
        # Save Button
        if st.button("Save Student Information", type="primary"):
            # Validate required fields
            if not name or not email:
                st.error("Please fill in Name and Email")
                return
            
            # Prepare student data
            student_data = {
                "name": name,
                "email": email,
                "tenth_percentage": tenth_percentage,
                "twelfth_percentage": twelfth_percentage,
                "btech_college": btech_college,
                "btech_cgpa": btech_cgpa,
                "preferred_countries": preferred_countries,
                "preferred_course": preferred_course,
                "ielts_score": ielts_score,
                "gre_score": gre_score,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save data
            save_student_data(student_data)
            st.session_state.student_data = student_data
            st.session_state.current_step = 1
            st.success("Student information saved successfully!")
            st.rerun()

    def step_university_recommendation(self):
        """Step 2: University Recommendations"""
        st.header("🏫 University Recommendations")
        
        # Retrieve saved student data
        student_data = read_student_data()
        
        # Extensive logging
        st.write("🔍 Debugging Student Data:")
        st.write(f"Raw Student Data: {student_data}")
        
        if not student_data:
            st.warning("No student data found. Please complete student information first.")
            return
        
        # Get preferred countries with extensive error handling
        try:
            preferred_countries = student_data.get('preferred_countries', [])
            
            # Force convert to list if not already a list
            if not isinstance(preferred_countries, list):
                preferred_countries = [preferred_countries]
            
            st.write(f"🌍 Preferred Countries: {preferred_countries}")
            
            if not preferred_countries:
                st.warning("No preferred countries selected. Please go back and select countries.")
                return
        except Exception as e:
            st.error(f"Error processing preferred countries: {e}")
            return
        
        # Display student profile summary
        st.subheader("Your Profile Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {student_data.get('name', 'N/A')}")
            st.write(f"**10th Percentage:** {student_data.get('tenth_percentage', 'N/A')}")
            st.write(f"**B.Tech CGPA:** {student_data.get('btech_cgpa', 'N/A')}")
        
        with col2:
            st.write(f"**Preferred Countries:** {', '.join(preferred_countries)}")
            st.write(f"**Preferred Course:** {student_data.get('preferred_course', 'N/A')}")
            st.write(f"**IELTS Score:** {student_data.get('ielts_score', 'N/A')}")
        
        # University recommendations based on preferred countries
        university_recommendations = {
            "Australia": [
                {
                    "name": "University of Melbourne",
                    "course": "M.Tech in Artificial Intelligence",
                    "ranking": 15,
                    "tuition_fee": 45000,
                    "program_highlights": "Strong industry connections, cutting-edge AI research",
                    "scholarship_opportunities": "Up to 50% tuition waiver for top international students"
                },
                {
                    "name": "Monash University",
                    "course": "M.Tech in Artificial Intelligence",
                    "ranking": 22,
                    "tuition_fee": 42000,
                    "program_highlights": "Collaborative industry projects, state-of-the-art AI labs",
                    "scholarship_opportunities": "Research excellence scholarships available"
                },
                {
                    "name": "University of Sydney",
                    "course": "M.Tech in Computer Science (AI Specialization)",
                    "ranking": 25,
                    "tuition_fee": 44000,
                    "program_highlights": "Interdisciplinary approach, machine learning focus",
                    "scholarship_opportunities": "International student merit scholarships"
                },
                {
                    "name": "UNSW Sydney",
                    "course": "M.Tech in Artificial Intelligence",
                    "ranking": 30,
                    "tuition_fee": 43000,
                    "program_highlights": "Industry-partnered capstone projects, AI ethics curriculum",
                    "scholarship_opportunities": "UNSW Global Excellence Scholarship"
                },
                {
                    "name": "University of Queensland",
                    "course": "M.Tech in Data Science and AI",
                    "ranking": 35,
                    "tuition_fee": 41000,
                    "program_highlights": "Quantum computing integration, AI research centers",
                    "scholarship_opportunities": "International postgraduate research scholarships"
                },
                {
                    "name": "University of Western Australia",
                    "course": "M.Tech in Artificial Intelligence",
                    "ranking": 40,
                    "tuition_fee": 40000,
                    "program_highlights": "Specialized AI and robotics track, industry internships",
                    "scholarship_opportunities": "UWA International Merit Scholarship"
                },
                {
                    "name": "Deakin University",
                    "course": "M.Tech in Artificial Intelligence",
                    "ranking": 45,
                    "tuition_fee": 38000,
                    "program_highlights": "Flexible online and on-campus options, AI innovation hub",
                    "scholarship_opportunities": "Vice-Chancellor's International Scholarship"
                },
                {
                    "name": "Queensland University of Technology",
                    "course": "M.Tech in Applied Artificial Intelligence",
                    "ranking": 50,
                    "tuition_fee": 39000,
                    "program_highlights": "Industry-focused curriculum, AI startup incubator",
                    "scholarship_opportunities": "QUT International Scholarship Program"
                },
                {
                    "name": "University of Adelaide",
                    "course": "M.Tech in Machine Learning and AI",
                    "ranking": 55,
                    "tuition_fee": 37000,
                    "program_highlights": "Advanced neural networks, AI ethics and governance",
                    "scholarship_opportunities": "Adelaide Scholarships International"
                },
                {
                    "name": "Curtin University",
                    "course": "M.Tech in Artificial Intelligence and Data Science",
                    "ranking": 60,
                    "tuition_fee": 36000,
                    "program_highlights": "Practical AI applications, industry collaboration",
                    "scholarship_opportunities": "Curtin International Scholarship"
                }
            ],
            "UK": [
                {
                    "name": "University of Cambridge",
                    "course": "M.Res in Artificial Intelligence",
                    "ranking": 1,
                    "tuition_fee": 55000,
                    "program_highlights": "World-leading AI research, interdisciplinary approach",
                    "scholarship_opportunities": "Gates Cambridge Scholarship"
                },
                {
                    "name": "Imperial College London",
                    "course": "M.Sc in Artificial Intelligence and Machine Learning",
                    "ranking": 10,
                    "tuition_fee": 52000,
                    "program_highlights": "Industry partnerships, cutting-edge computational methods",
                    "scholarship_opportunities": "President's PhD Scholarship"
                },
                {
                    "name": "University of Oxford",
                    "course": "M.Sc in Machine Learning",
                    "ranking": 5,
                    "tuition_fee": 54000,
                    "program_highlights": "Advanced AI and deep learning curriculum",
                    "scholarship_opportunities": "Clarendon Scholarship"
                },
                {
                    "name": "UCL (University College London)",
                    "course": "M.Sc in Artificial Intelligence",
                    "ranking": 15,
                    "tuition_fee": 48000,
                    "program_highlights": "Robotics and natural language processing focus",
                    "scholarship_opportunities": "UCL Global Scholarship"
                },
                {
                    "name": "University of Manchester",
                    "course": "M.Sc in Artificial Intelligence",
                    "ranking": 20,
                    "tuition_fee": 42000,
                    "program_highlights": "AI ethics and societal impact studies",
                    "scholarship_opportunities": "Manchester International Scholarship"
                },
                {
                    "name": "King's College London",
                    "course": "M.Sc in Artificial Intelligence",
                    "ranking": 25,
                    "tuition_fee": 46000,
                    "program_highlights": "Interdisciplinary AI research",
                    "scholarship_opportunities": "King's International Scholarship"
                },
                {
                    "name": "University of Edinburgh",
                    "course": "M.Sc in Artificial Intelligence",
                    "ranking": 30,
                    "tuition_fee": 43000,
                    "program_highlights": "Machine learning and natural language processing",
                    "scholarship_opportunities": "Edinburgh Global Scholarship"
                },
                {
                    "name": "University of Bristol",
                    "course": "M.Sc in Artificial Intelligence",
                    "ranking": 35,
                    "tuition_fee": 41000,
                    "program_highlights": "Robotics and computer vision specialization",
                    "scholarship_opportunities": "Bristol International Scholarship"
                },
                {
                    "name": "University of Southampton",
                    "course": "M.Sc in Artificial Intelligence",
                    "ranking": 40,
                    "tuition_fee": 39000,
                    "program_highlights": "AI and data science integration",
                    "scholarship_opportunities": "Southampton International Scholarship"
                },
                {
                    "name": "University of Sheffield",
                    "course": "M.Sc in Artificial Intelligence",
                    "ranking": 45,
                    "tuition_fee": 38000,
                    "program_highlights": "Practical AI applications and research",
                    "scholarship_opportunities": "Sheffield International Scholarship"
                }
            ]
        }
        
        # Display recommendations for selected countries
        for country in preferred_countries:
            st.subheader(f"Universities in {country}")
            
            # Get universities for the selected country
            country_universities = university_recommendations.get(country, [])
            
            for uni in country_universities:
                with st.expander(f"{uni['name']} - {country}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Course:** {uni['course']}")
                        st.write(f"**Global Ranking:** {uni['ranking']}")
                        st.write(f"**Estimated Annual Tuition:** ${uni['tuition_fee']}")
                    
                    with col2:
                        st.write(f"**Program Highlights:** {uni['program_highlights']}")
                        st.write(f"**Scholarship Opportunities:** {uni['scholarship_opportunities']}")
                    
                    # Add a button to save university preference
                    if st.button(f"Select {uni['name']}"):
                        # Save selected university to student data
                        student_data = read_student_data()
                        student_data['selected_universities'] = student_data.get('selected_universities', []) + [uni['name']]
                        save_student_data(student_data)
                        st.success(f"{uni['name']} added to your preferences!")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.current_step = 0
                st.rerun()
        
        with col2:
            if st.button("Next: Visa Requirements"):
                st.session_state.current_step = 2
                st.rerun()

    def main(self):
        """Main Streamlit App"""
        try:
            st.title("🌍 International Student Counselor")
            
            # Workflow steps
            steps = [
                "Student Information",
                "University Recommendations",
                "Visa Requirements",
                "Scholarship Search",
                "Document Management"
            ]
            
            # Progress indicator
            st.progress(st.session_state.current_step / (len(steps) - 1))
            
            # Step-based navigation
            if st.session_state.current_step == 0:
                self.step_student_input()
            elif st.session_state.current_step == 1:
                self.step_university_recommendation()
            # Add more steps here as you implement them
        
        except Exception as e:
            logging.error(f"Error in main workflow: {e}")
            logging.error(traceback.format_exc())
            st.error(f"An unexpected error occurred: {e}")
            st.error("Please check the logs for more details.")

def main():
    workflow = CounselorWorkflow()
    workflow.main()

if __name__ == "__main__":
    main()
