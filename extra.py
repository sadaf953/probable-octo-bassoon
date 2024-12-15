from crewai import Agent, Task, Crew, Process
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sqlite3
from  groq import ChatGroq
import streamlit as st

# Download necessary NLTK data
# nltk.download('punkt')
# nltk.download('stopwords')

# # Initialize BeautifulSoup for web scraping
# def scrape_university_data(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     # Implement scraping logic here
#     return soup

# # Initialize SQLite database
# conn = sqlite3.connect('student_guidance.db')
# cursor = conn.cursor()

# # Create tables if they don't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS universities
#     (id INTEGER PRIMARY KEY, name TEXT, country TEXT, programs TEXT)
# ''')
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS scholarships
#     (id INTEGER PRIMARY KEY, name TEXT, amount REAL, eligibility TEXT)
# ''')
# conn.commit()

# llm=ChatGroq(model="mixtral-8x7b-32768",
#              verbose=True,
#              temperature=0.5,
#              api_key=GROQ_API_KEY)


# # Define the agents with enhanced capabilities
# university_selection_agent = Agent(
#     role="University Selection Agent",
#     goal="Help students identify and shortlist universities and programs",
#     backstory="Expert in matching students with suitable academic programs worldwide",
#     tools=["web_scraping", "data_analysis"],
#     llm =[llm],
# )

# scholarship_agent = Agent(
#     role="Scholarship and Financial Aid Agent",
#     goal="Inform about scholarships and assist with applications",
#     backstory="Specialist in educational funding opportunities and financial planning",
#     tools=["database_query", "eligibility_calculator"],
#     llm =[llm],
# )

# application_assistance_agent = Agent(
#     role="Application Assistance Agent",
#     goal="Support application process, offer acceptance, and fee management",
#     backstory="Experienced in guiding students through university applications and admissions",
#     tools=["form_filling_assistant", "document_preparation"],
#     llm =[llm],
# )

# visa_guidance_agent = Agent(
#     role="Visa Guidance Agent",
#     goal="Assist with visa application process and immigration matters",
#     backstory="Expert in international student visa requirements and immigration procedures",
#     tools=["visa_requirement_checker", "document_checklist_generator"],
#     llm =[llm],
# )



# # Define the tasks with data processing and analysis
# gather_info_task = Task(
#     description="Gather and process comprehensive information from the user",
#     agent=university_selection_agent,
#     expected_output="Processed user information for study abroad planning"
# )

# analyze_options_task = Task(
#     description="Analyze and match user profile with suitable universities and programs",
#     agent=university_selection_agent,
#     expected_output="List of recommended universities and programs"
# )

# find_scholarships_task = Task(
#     description="Identify relevant scholarships and financial aid options",
#     agent=scholarship_agent,
#     expected_output="List of suitable scholarships and financial aid opportunities"
# )

# prepare_applications_task = Task(
#     description="Assist in preparing application materials and documents",
#     agent=application_assistance_agent,
#     expected_output="Guidance on application preparation and document checklist"
# )

# visa_assistance_task = Task(
#     description="Provide visa application guidance and requirements",
#     agent=visa_guidance_agent,
#     expected_output="Visa application process outline and required documents"
# )

# pre_departure_prep_task = Task(
#     description="Offer pre-departure orientation and cultural briefing",
#     agent=pre_departure_agent,
#     expected_output="Pre-departure checklist and cultural orientation guide"
# )

# # Create the crew with enhanced workflow
# student_guidance_crew = Crew(
#     agents=[university_selection_agent, scholarship_agent, application_assistance_agent, visa_guidance_agent, pre_departure_agent],
#     tasks=[gather_info_task, analyze_options_task, find_scholarships_task, prepare_applications_task, visa_assistance_task, pre_departure_prep_task],
#     process=Process.sequential
# )

# Function to run the crew and get user input using Streamlit
# def run_student_guidance_crew():
#     st.title("Comprehensive Student Guidance System")
    
#     # Gather user information using Streamlit forms
#     with st.form("user_info_form"):
#         st.header("Personal Information")
#         education = st.text_input("1. What is your educational background? (e.g., B.Tech scores, degree type)")
#         study_level = st.selectbox("2. What is your desired level of study?", ["Bachelor's", "Master's", "PhD"])
#         field_of_study = st.text_input("3. What is your desired field of study and specific courses of interest?")
#         countries = st.text_input("4. Which countries or regions are you interested in for studying abroad?")
        
#         st.header("Academic and Language Proficiency")
#         gpa = st.number_input("5. What is your GPA or equivalent score?", min_value=0.0, max_value=4.0, step=0.1)
#         test_scores = st.text_input("6. Please provide your standardized test scores (e.g., TOEFL, IELTS, GRE, GMAT)")
#         language_proficiency = st.selectbox("7. What is your language proficiency level?", ["Beginner", "Intermediate", "Advanced", "Native"])
        
#         st.header("Financial Information")
#         budget = st.number_input("8. What is your budget for tuition and living expenses? (in USD)", min_value=0)
#         existing_aid = st.text_area("9. Do you have any existing financial aid, sponsorship, or scholarships? If yes, please provide details")
        
#         st.header("Visa and Immigration Details")
#         visa_status = st.text_input("10. What is your current visa status (if any)?")
#         visa_rejections = st.text_area("11. Have you had any previous visa rejections? If yes, please provide details")
#         intended_stay = st.text_input("12. What is your intended length of stay for the study program?")
        
#         st.header("Specific Preferences or Needs")
#         start_date = st.date_input("13. What is your preferred start date for the program?")
#         accommodations = st.text_area("14. Do you need any special accommodations or support services?")
#         work_study = st.checkbox("15. Are you interested in work-study options or internships?")
#         specific_scholarships = st.text_area("16. Are you interested in any specific scholarship programs or grants?")
        
#         submitted = st.form_submit_button("Submit")
    
#     if submitted:
#         # Process the user input
#         user_input = {
#             "education": education,
#             "study_level": study_level,
#             "field_of_study": field_of_study,
#             "countries_of_interest": countries,
#             "gpa": gpa,
#             "test_scores": test_scores,
#             "language_proficiency": language_proficiency,
#             "budget": budget,
#             "existing_aid": existing_aid,
#             "visa_status": visa_status,
#             "visa_rejections": visa_rejections,
#             "intended_stay": intended_stay,
#             "start_date": str(start_date),
#             "accommodations": accommodations,
#             "work_study_interest": work_study,
#             "specific_scholarships": specific_scholarships
#         }
        
#         # Set the user information for the crew to use
#         student_guidance_crew.set_user_input(user_input)
        
#         # Run the crew
#         with st.spinner("Processing your information..."):
#             result = student_guidance_crew.kickoff()
        
#         st.success("Analysis complete!")
#         st.subheader("Here's the comprehensive guidance based on your input:")
#         st.write(result)

# # Run the Streamlit app
# if __name__ == "__main__":
#     run_student_guidance_crew()


