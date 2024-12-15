import streamlit as st
from crewai import Crew
from task import (
    collect_student_info_task,
    rank_universities_task,
    fetch_curriculum_task,
    fetch_fees_scholarships_task,
    assist_application_process_task,
    coordinate_recommendations_task
)
from agents import (
    data_collection_agent,
    university_ranking_agent,
    curriculum_fetching_agent,
    fee_scholarship_agent,
    application_assistance_agent,
    coordinator_agent
)
from utils.student_data import save_student_data

def collect_student_input():
    """Collect student input via Streamlit form."""
    st.header("Student Information Form")
    
    # Academic Details
    btech_college = st.text_input("B.Tech College Name")
    btech_cgpa = st.number_input("B.Tech CGPA", min_value=0.0, max_value=10.0, step=0.1)
    btech_course = st.text_input("Course Taken in B.Tech")
    mtech_interest = st.text_input("Course of Interest in M.Tech")
    
    # Additional Academic Details
    tenth_percentage = st.number_input("10th Percentage", min_value=0.0, max_value=100.0, step=0.1)
    twelfth_percentage = st.number_input("12th Percentage", min_value=0.0, max_value=100.0, step=0.1)
    gre_gmat_score = st.number_input("GRE/GMAT Score (if applicable)", min_value=0)
    ielts_toefl_score = st.number_input("IELTS/TOEFL Score", min_value=0.0, step=0.5)
    
    # Projects and Experience
    projects = st.text_area("Relevant Projects/Research Experience")
    awards = st.text_area("Awards and Recognition")
    work_experience = st.text_area("Work Experience")
    
    # Application Preferences
    intake_period = st.selectbox("Preferred Intake Period", ["February", "September"])
    intake_year = st.selectbox("Desired Year of Intake", [2024, 2025, 2026])
    target_countries = st.multiselect("Target Countries", ["Australia", "Canada", "USA", "UK"])
    budget_constraints = st.number_input("Budget Constraints (Approx. Annual Expenses in USD)", min_value=0)
    career_goals = st.text_area("Career Goals")
    
    # Collect and return student data
    student_data = {
        "B.Tech College Name": btech_college,
        "B.Tech CGPA": btech_cgpa,
        "Course Taken in B.Tech": btech_course,
        "Course of Interest in M.Tech": mtech_interest,
        "10th Percentage": tenth_percentage,
        "12th Percentage": twelfth_percentage,
        "GRE/GMAT Score": gre_gmat_score,
        "IELTS/TOEFL Score": ielts_toefl_score,
        "Relevant Projects/Research Experience": projects,
        "Awards and Recognition": awards,
        "Work Experience": work_experience,
        "Preferred Intake Period": intake_period,
        "Desired Year of Intake": intake_year,
        "Target Countries": target_countries,
        "Budget Constraints": budget_constraints,
        "Career Goals": career_goals
    }
    
    return student_data

def main():
    st.title("University Recommendation System for M.Tech in AI")
    
    # Collect student input
    student_data = collect_student_input()
    
    # Save student data to a JSON file
    save_student_data(student_data)
    
    # Create the crew
    crew = Crew(
        agents=[
            data_collection_agent,
            university_ranking_agent,
            curriculum_fetching_agent,
            fee_scholarship_agent,
            application_assistance_agent,
            coordinator_agent
        ],
        tasks=[
            collect_student_info_task,
            rank_universities_task,
            fetch_curriculum_task,
            fetch_fees_scholarships_task,
            assist_application_process_task,
            coordinate_recommendations_task
        ]
    )
    
    # Run the crew and display results
    if st.button("Generate University Recommendations"):
        try:
            with st.spinner("Generating recommendations..."):
                # Pass student_data to kickoff
                result = crew.kickoff(inputs={'student_data': student_data})
            
            st.success("Recommendations Generated!")
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error("Please check your Google API key and ensure it is correctly set in the .env file.")
            # Optional: Log the full traceback for debugging
            import traceback
            st.error(traceback.format_exc())

if __name__ == "__main__":
    main()
