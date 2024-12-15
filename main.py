import streamlit as st
import os
from scrape import scrape_website, extract_body_content, clean_body_content
from crew import run_crew_process
from utils.data_processing import read_student_data, generate_report #Import necessary functions

def validate_input(student_info):
    """Validates student input with improved error handling."""
    errors = []
    required_fields = [
        "B.Tech College Name",
        "B.Tech CGPA",
        "Course Taken in B.Tech",
        "Course of Interest for M.Tech in AI",
    ]

    for field in required_fields:
        if not student_info.get(field):
            errors.append(f"Please enter your {field}")

    try:
        cgpa = float(student_info["B.Tech CGPA"])
        if not 0 <= cgpa <= 10:
            errors.append("CGPA must be between 0 and 10")
    except ValueError:
        errors.append("Invalid CGPA format. Please enter a number.")

    return errors


def save_student_info(student_info, file_path='student.txt'):
    """Saves student info to a file with improved error handling."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:  #Added encoding for better compatibility
            for key, value in student_info.items():
                f.write(f"{key}: {value}\n")
        return True
    except IOError as e:
        st.error(f"Error saving student information: {e}")
        return False


def main():
    st.set_page_config(page_title="Uni-Guide: M.Tech Advisor", page_icon="🎓")
    st.title("🎓 Uni-Guide: M.Tech Advisor")

    # Student Information Section
    st.header("📝 Student Information")
    col1, col2 = st.columns(2)

    with col1:
        btech_college_name = st.text_input("B.Tech College Name")
        btech_course = st.text_input("Course Taken in B.Tech")
        intake_period = st.selectbox("Preferred Intake Period", ["February", "September"])

    with col2:
        btech_cgpa = st.text_input("B.Tech CGPA")
        mtech_interest = st.text_input("Course of Interest for M.Tech in AI")
        intake_year = st.text_input("Desired Year of Intake (e.g., 2025 or later)")

    is_indian_student = st.checkbox("Indian Student")

    if st.button("🚀 Submit Student Information"):
        student_info = {
            "B.Tech College Name": btech_college_name,
            "B.Tech CGPA": btech_cgpa,
            "Course Taken in B.Tech": btech_course,
            "Course of Interest for M.Tech in AI": mtech_interest,
            "Preferred Intake Period": intake_period,
            "Desired Year of Intake": intake_year,
            "Indian Student": is_indian_student,
        }

        input_errors = validate_input(student_info)
        if input_errors:
            for error in input_errors:
                st.error(error)
        else:
            if save_student_info(student_info):
                st.success("Student information saved successfully!")

                if st.button("🔍 Get University Recommendations"):
                    with st.spinner("Generating recommendations..."):
                        try:
                            result = run_crew_process(student_info)
                            st.write(result)
                            if isinstance(result, str) and "Report generated successfully" in result:
                                with open('output.txt', 'r') as f:
                                    report_content = f.read()
                                st.text_area("Recommendations", report_content)

                        except Exception as e:
                            st.error(f"An error occurred: {e}")


    # College Search Section (simplified for brevity)
    st.header("🔎 College Search")
    if st.button("🌐 Search Colleges"):
      # ... (Your college search logic here) ...


if __name__ == "__main__":
    main()