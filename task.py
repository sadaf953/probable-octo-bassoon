from crewai import Task
from agents import (
    data_collection_agent,
    university_ranking_agent,
    curriculum_fetching_agent,
    fee_scholarship_agent,
    application_assistance_agent,
    coordinator_agent, # Added coordinator agent
)
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import streamlit as st
from utils.student_data import read_student_data
from utils.tools import (
    docs_tool,
    search_tool,
    file_tool,
)

# Function to create tasks (reduces repetition)
def create_task(description, expected_output, tools, agent):
    return Task(
        description=description,
        expected_output=expected_output,
        tools=tools,
        agent=agent,
    )

# Read student data (improved error handling)
try:
    student_data = read_student_data()
    btech_college_name = student_data.get('B.Tech College Name')
    btech_cgpa = student_data.get('B.Tech CGPA')
    btech_course = student_data.get('Course Taken in B.Tech')
    mtech_interest = student_data.get('Course of Interest in M.Tech')
    intake_period = student_data.get('Preferred Intake Period')
    intake_year = student_data.get('Desired Year of Intake')

except (FileNotFoundError, KeyError) as e:
    raise ValueError(f"Error reading student data: {e}")

# Create tasks using the helper function (improved readability)
collect_student_info_task = create_task(
    description=(
        f"""
        Collect comprehensive academic and personal details from the student to personalize university recommendations.  The Data Collection Agent will prompt the student for the following information:

        **Academic Details:**

        - **B.Tech College Name:** {student_data.get('B.Tech College Name', 'N/A')}
        - **B.Tech CGPA:** {student_data.get('B.Tech CGPA', 'N/A')}
        - **Course Taken in B.Tech:** {student_data.get('Course Taken in B.Tech', 'N/A')}
        - **Course of Interest in M.Tech:** {student_data.get('Course of Interest in M.Tech', 'N/A')}
        - **10th Percentage:** {student_data.get('10th Percentage', 'N/A')}
        - **12th Percentage:** {student_data.get('12th Percentage', 'N/A')}
        - **GRE/GMAT Score (if applicable):** {student_data.get('GRE/GMAT Score', 'N/A')}
        - **IELTS/TOEFL Score:** {student_data.get('IELTS/TOEFL Score', 'N/A')}
        - **Relevant Projects/Research Experience:** {student_data.get('Relevant Projects/Research Experience', 'N/A')} (Please provide brief descriptions)
        - **Awards and Recognition (if any):** {student_data.get('Awards and Recognition', 'N/A')} (Please provide brief descriptions)
        - **Work Experience (if any):** {student_data.get('Work Experience', 'N/A')} (Please provide brief descriptions including company, role, and duration)

        **Application Preferences:**

        - **Preferred Intake Period (February or September):** {student_data.get('Preferred Intake Period', 'N/A')}
        - **Desired Year of Intake (e.g., 2025 or later):** {student_data.get('Desired Year of Intake', 'N/A')}
        - **Target Countries (e.g., Australia, Canada, USA):** {student_data.get('Target Countries', 'N/A')}
        - **Budget Constraints (approximate range):** {student_data.get('Budget Constraints', 'N/A')}
        - **Career Goals:** {student_data.get('Career Goals', 'N/A')} (Please describe your long-term career aspirations)


        Ensure that all information is accurately captured and validated to avoid errors in the recommendation process.
        """
    ),
    expected_output="""
        A complete and validated profile including academic details, application preferences, and career goals, ready for use in the university recommendation process.
        """,
    tools=[file_tool, search_tool],
    agent=data_collection_agent,
)

rank_universities_task = create_task(
    description=(
        f"""
        Rank the top 15 universities in {student_data.get('Target Countries', ['USA'])[0]} offering M.Tech in Artificial Intelligence based on the student's academic profile. 
        The University Ranking Agent will use web search tools to gather data on curriculum quality, global reputation, faculty expertise, 
        and any specific student preferences provided. Additionally, factor in the intake period ({intake_period or 'N/A'}) and the desired year of intake ({intake_year or 'N/A'}).

        Ensure that the ranking is thorough, accurate, and takes into account the latest data available from reliable sources.

        The profile details to consider:
        - B.Tech College Name: {btech_college_name or 'N/A'}
        - B.Tech CGPA: {btech_cgpa or 'N/A'}
        - Course Taken in B.Tech: {btech_course or 'N/A'}
        - Preferred M.Tech Course: {mtech_interest or 'N/A'}
        - Intake Period: {intake_period or 'N/A'}
        - Desired Year of Intake: {intake_year or 'N/A'}

        For each university, provide a link to the official website and reference the sources used for ranking.
        """
    ),
    expected_output="""
        A ranked list of the top 15 universities offering M.Tech in Artificial Intelligence, tailored to the student's profile, including intake period and year.
        Each university entry should include a link to the official website and a citation of the sources used for the ranking.
        """,
    tools=[search_tool, docs_tool],
    agent=university_ranking_agent,
)

fetch_curriculum_task = create_task(
    description=(
        f"""
        Fetch detailed curriculum information for the M.Tech in Artificial Intelligence programs from the top 15 universities 
        in {student_data.get('Target Countries', ['USA'])[0]}, considering the preferred intake period ({intake_period or 'N/A'}) and the desired year of intake ({intake_year or 'N/A'}). 
        The Curriculum Fetching Agent will gather information on the courses, labs, projects, and research opportunities in AI and related fields.

        Focus on universities that align with the following student profile:
        - B.Tech College Name: {btech_college_name or 'N/A'}
        - B.Tech CGPA: {btech_cgpa or 'N/A'}
        - Course Taken in B.Tech: {btech_course or 'N/A'}
        - Preferred M.Tech Course: {mtech_interest or 'N/A'}
        - Intake Period: {intake_period or 'N/A'}
        - Desired Year of Intake: {intake_year or 'N/A'}

        For each university, provide:
        - Detailed curriculum structure
        - Core and elective courses in AI
        - Research and project opportunities
        - Faculty expertise
        - Links to official program pages
        """
    ),
    expected_output="""
        A comprehensive report on the curriculum details for top 15 universities offering M.Tech in Artificial Intelligence.
        Include a detailed breakdown of courses, research opportunities, and program highlights.
        """,
    tools=[search_tool, docs_tool],
    agent=curriculum_fetching_agent,
)

fetch_fees_scholarships_task = create_task(
    description=(
        f"""
        Collect information on the yearly fee structures and available scholarships for the top 15 universities of
        {student_data.get('Target Countries', ['USA'])[0]} offering M.Tech in Artificial Intelligence. 
        The Fee and Scholarship Agent will research and compile comprehensive details about tuition costs, living expenses, 
        and potential scholarship opportunities.

        Consider the following profile details:
        - B.Tech CGPA: {btech_cgpa or 'N/A'}
        - B.Tech College Name: {btech_college_name or 'N/A'}
        - Preferred M.Tech Course: {mtech_interest or 'N/A'}
        - Intake Period: {intake_period or 'N/A'}
        - Desired Year of Intake: {intake_year or 'N/A'}

        For each university, provide:
        - Yearly tuition fees
        - Estimated living expenses
        - Available scholarships and their eligibility criteria
        - Links to official scholarship pages
        """
    ),
    expected_output="""
        A detailed report on the fee structures and scholarship opportunities for the top 15 universities.
        Each entry should include comprehensive financial information, scholarship details, and links to official sources.
        """,
    tools=[search_tool, docs_tool],
    agent=fee_scholarship_agent,
)

assist_application_process_task = create_task(
    description=(
        f"""
        Provide comprehensive assistance with the university application process for the student, considering the intake period ({intake_period or 'N/A'}) and the desired year of intake ({intake_year or 'N/A'}). The Application Assistance Agent 
        will guide the student through the necessary steps, including understanding application fees, preparing required documents, 
        and navigating the application submission process.

        Key aspects to cover:
        - Application deadlines
        - Required documents
        - Application fee details
        - Step-by-step application guidance
        - Potential challenges and how to overcome them
        - Links to official application portals

        Intake Period: {intake_period or 'N/A'}
        Desired Year of Intake: {intake_year or 'N/A'}
        """
    ),
    expected_output="""
        A comprehensive guide to the application process, including detailed steps, required documents, and strategic advice 
        for successfully applying to the top universities offering M.Tech in Artificial Intelligence.
        """,
    tools=[search_tool, docs_tool],
    agent=application_assistance_agent,
)


#Added Coordinator Task
def convert_currency(amount, from_currency):
    """
    Convert currency to INR using current exchange rates.
    Note: In a real-world scenario, use an API for real-time exchange rates.
    """
    exchange_rates = {
        'USD': 83.50,  # 1 USD = 83.50 INR
        'GBP': 105.20,  # 1 GBP = 105.20 INR
        'AUD': 55.30,  # 1 AUD = 55.30 INR
    }
    
    if from_currency not in exchange_rates:
        raise ValueError(f"Unsupported currency: {from_currency}")
    
    try:
        amount = float(amount)
        return round(amount * exchange_rates[from_currency], 2)
    except ValueError:
        raise ValueError(f"Invalid amount: {amount}")

coordinate_recommendations_task = create_task(
    description="""
    Synthesize information from all agents to provide a comprehensive university recommendation.
    Consider the rankings, curriculum details, fees, scholarships, and application process information to craft a personalized recommendation.
    """,
    expected_output="""
    A concise and well-structured recommendation report detailing the top 3 universities for the student,
    including justification based on the gathered information from other agents.
    """,
    tools=[search_tool, docs_tool],
    agent=coordinator_agent,
)

def get_fees_in_inr(fees_data):
    """Converts fees from USD, GBP, AUD to INR with error handling."""
    fees_inr = {}
    for currency, amount in fees_data.items():
        try:
            converted_amount = convert_currency(amount, currency)
            fees_inr[currency] = converted_amount  #Store both original and converted
        except ValueError as e:
            fees_inr[currency] = f"Conversion Error: {e}" #Store error message
    return fees_inr