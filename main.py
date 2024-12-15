import streamlit as st
import os
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from crew import crew, kickoff_crew

def validate_input(student_info):
    """Validate student input"""
    errors = []
    required_fields = [
        "B.Tech College Name", 
        "B.Tech CGPA", 
        "Course Taken in B.Tech", 
        "Course of Interest for M.Tech in AI"
    ]
    
    for field in required_fields:
        if not student_info[field]:
            errors.append(f"Please enter your {field}")
    
    try:
        cgpa = float(student_info["B.Tech CGPA"])
        if cgpa < 0 or cgpa > 10:
            errors.append("CGPA must be between 0 and 10")
    except ValueError:
        errors.append("CGPA must be a valid number")
    
    return errors

def save_student_info(student_info):
    """Save student info to file with error handling"""
    try:
        with open('student.txt', 'w') as f:
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
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        btech_college_name = st.text_input("B.Tech College Name")
        btech_course = st.text_input("Course Taken in B.Tech")
        intake_period = st.selectbox("Preferred Intake Period", ["February", "September"])
    
    with col2:
        btech_cgpa = st.text_input("B.Tech CGPA")
        mtech_interest = st.text_input("Course of Interest for M.Tech")
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
            "Indian Student": is_indian_student
        }
        
        # Validate input
        input_errors = validate_input(student_info)
        if input_errors:
            for error in input_errors:
                st.error(error)
        else:
            if save_student_info(student_info):
                st.success("Student information saved successfully!")
                
                # Option to run crew recommendation
                if st.button("🔍 Get University Recommendations"):
                    with st.spinner("Generating personalized recommendations..."):
                        # Set inputs for the crew
                        crew.inputs = student_info
                        result = crew.kickoff()
                        st.write(result)

    # College Search Section
    st.header("🔎 College Search")
    if st.button("🌐 Search Colleges"):
        try:
            with open('urls.txt', 'r') as f:
                urls = f.read().splitlines()
        except FileNotFoundError:
            st.error("URLs file not found. Please create 'urls.txt' with university URLs.")
            return

        all_cleaned_content = []
        progress_bar = st.progress(0)

        for i, url in enumerate(urls):
            try:
                dom_content = scrape_website(url)
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)
                all_cleaned_content.append(cleaned_content)
                progress_bar.progress((i + 1) / len(urls))
            except Exception as e:
                st.warning(f"Error scraping {url}: {e}")

        st.session_state.dom_content = all_cleaned_content

        with st.expander("📄 View Scraped Content"):
            for i, content in enumerate(all_cleaned_content, start=1):
                st.text_area(f"Content from URL {i}", content, height=300)

    # Store Content Section
    if "dom_content" in st.session_state:
        if st.button("💾 Store Scraped Content"):
            try:
                with open('stored_content.txt', 'w') as f:
                    for content in st.session_state.dom_content:
                        f.write(content + "\n\n")
                st.success("Content saved to stored_content.txt")
            except IOError as e:
                st.error(f"Error storing content: {e}")

if __name__ == "__main__":
    main()
