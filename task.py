from crewai import Task
from agents import data_collection_agent, university_ranking_agent, curriculum_fetching_agent, fee_scholarship_agent, application_assistance_agent
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import streamlit as st
from tools import (
    docs_tool, 
    search_tool, 
    read_student_data,
    file_tool
)

# Read student data from students.txt
student_data = read_student_data()

collect_student_info_task = Task(
    description=(
        f"""
        Collect the necessary academic details from the student to personalize the university recommendations.
        The Data Collection Agent will prompt the student to provide their B.Tech college, 
        CGPA, course taken, and the course they are interested in for M.Tech.

        The collected details should be:
        - B.Tech College Name: {student_data.get('B.Tech College Name')}
        - B.Tech CGPA: {student_data.get('B.Tech CGPA')}
        - Course Taken in B.Tech: {student_data.get('Course Taken in B.Tech')}
        - Course of Interest in M.Tech: {student_data.get('Course of Interest in M.Tech')}
        - Preferred Intake Period (February or September): {student_data.get('Preferred Intake Period')}
        - Desired Year of Intake (e.g., 2025 or later): {student_data.get('Desired Year of Intake')}

        Ensure that all information is accurately captured and validated to avoid any errors in the 
        recommendation process.
        """
    ),
    expected_output="""
        A complete and validated set of academic details, along with the preferred intake period and year, ready to be used in the university selection and ranking process.
        """,
    tools=[file_tool, search_tool],
    agent=data_collection_agent,
)

rank_universities_task = Task(
    description=(
        """
        Rank the top 15 universities in Australia offering M.Tech in Artificial Intelligence based on the student's academic profile. 
        The University Ranking Agent will use web search tools to gather data on curriculum quality, global reputation, faculty expertise, 
        and any specific student preferences provided. Additionally, factor in the intake period (February or September) and the desired year of intake (e.g., 2025 or later).

        Ensure that the ranking is thorough, accurate, and takes into account the latest data available from reliable sources.

        The profile details to consider:
        - B.Tech College Name: {btech_college_name}
        - B.Tech College Ranking: {btech_college_ranking}
        - B.Tech CGPA: {btech_cgpa}
        - Course Taken in B.Tech: {btech_course}
        - Preferred M.Tech Course: {mtech_interest}
        - Intake Period: {intake_period}
        - Desired Year of Intake: {intake_year}

        For each university, provide a link to the official website and reference the sources used for ranking.
        """
    ),
    expected_output="""
        A ranked list of the top 15 universities in Australia offering M.Tech in Artificial Intelligence, tailored to the student's profile, including intake period and year.
        Each university entry should include a link to the official website and a citation of the sources used for the ranking.
        """,
    tools=[search_tool, docs_tool],
    agent=university_ranking_agent,
)

fetch_curriculum_task = Task(
    description=(
        """
        Fetch detailed curriculum information for the M.Tech in Artificial Intelligence programs from the top 15 universities 
        in Australia, considering the preferred intake period (February or September) and the desired year of intake (e.g., 2025 or later). The Curriculum Fetching Agent will gather information on the courses, labs, projects, and any other 
        relevant academic activities offered in these programs.

        The curriculum should be analyzed for its relevance to current industry trends in AI, and its potential to provide the 
        skills and knowledge necessary for the student's career goals.

        The specific M.Tech program of interest: {mtech_interest}
        Intake Period: {intake_period}
        Desired Year of Intake: {intake_year}

        Provide links to the relevant curriculum pages on the universities' official websites, and cite the sources used to gather this information.
        """
    ),
    expected_output="""
        A comprehensive report detailing the curriculum of M.Tech in Artificial Intelligence programs from the top 15 universities.
        Each curriculum entry should include a link to the relevant curriculum page on the university's official website and citations of the sources used.
        """,
    tools=[search_tool, docs_tool],
    agent=curriculum_fetching_agent,
)

fetch_fees_scholarships_task = Task(
    description=(
        """
        Collect information on the yearly fee structures and available scholarships for the top 15 universities of
        Australia offering M.Tech in Artificial Intelligence. The Fee and Scholarship Agent will research and compile 
        comprehensive details about tuition costs, living expenses, and potential scholarship opportunities.

        Consider the following profile details:
        - B.Tech CGPA: {btech_cgpa}
        - B.Tech College Name: {btech_college_name}
        - Preferred M.Tech Course: {mtech_interest}
        - Intake Period: {intake_period}
        - Desired Year of Intake: {intake_year}

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

assist_application_process_task = Task(
    description=(
        """
        Provide comprehensive assistance with the university application process for the student, considering the intake period (February or September) and the desired year of intake (e.g., 2025 or later). The Application Assistance Agent 
        will guide the student through the necessary steps, including understanding application fees, preparing required documents, 
        and navigating the application submission process.

        Key aspects to cover:
        - Application deadlines
        - Required documents
        - Application fee details
        - Step-by-step application guidance
        - Potential challenges and how to overcome them
        - Links to official application portals

        Intake Period: {intake_period}
        Desired Year of Intake: {intake_year}
        """
    ),
    expected_output="""
        A comprehensive guide to the application process, including detailed steps, required documents, and strategic advice 
        for successfully applying to the top universities offering M.Tech in Artificial Intelligence.
        """,
    tools=[search_tool, docs_tool],
    agent=application_assistance_agent,
)
