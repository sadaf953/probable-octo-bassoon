from crewai import Agent
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY

# Check for Google API key (improved error handling)
if not GOOGLE_API_KEY:
    raise ValueError("Google API Key is not set. Please set the GOOGLE_API_KEY in your .env file.")

# Use Gemini LLM (more concise)
llm = ChatGoogleGenerativeAI(
    google_api_key=GOOGLE_API_KEY, 
    model="gemini-pro", 
    temperature=0.5, 
    verbose=True,
    provider="google"  # Explicitly specify the provider
)


def create_agent(role, goal, backstory, tools=[], allow_delegation=False):
    """Helper function to create agents with consistent structure."""
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools,
        llm=llm,
        allow_delegation=allow_delegation,
        verbose=True,
    )


# Create agents using the helper function (improved readability)
university_ranking_agent = create_agent(
    role="University Ranking Agent",
    goal="Rank universities for M.Tech in Artificial Intelligence in Australia based on curriculum quality, fees, and global reputation.",
    backstory="""The University Ranking Agent has been developed with an extensive background in higher education consulting and academic research. 
    With years of experience in evaluating and ranking educational institutions, this agent has access to a wide range of global databases, 
    allowing it to analyze a university's curriculum, faculty, research output, and industry connections. It leverages advanced data 
    analysis techniques to compare institutions and identify the top programs tailored to the student's specific academic and career goals. 
    The agent is particularly adept at understanding the evolving landscape of AI education and can pinpoint which universities are 
    leading in this cutting-edge field.""",
)

curriculum_fetching_agent = create_agent(
    role="Curriculum Fetching Agent",
    goal="Fetch detailed curriculum information for M.Tech in Artificial Intelligence programs from top universities in Australia.",
    backstory="""The Curriculum Fetching Agent is like a librarian with specialized knowledge in the field of artificial intelligence education. 
    Having spent years curating academic resources, this agent has developed an intuitive understanding of what makes a curriculum truly 
    effective. It digs deep into university course offerings, syllabi, and academic catalogs to extract comprehensive details about 
    AI programs, ensuring students get the most relevant and up-to-date information.""",
)

data_collection_agent = create_agent(
    role="Data Collection Agent",
    goal="Collect comprehensive student information and preferences for M.Tech in Artificial Intelligence programs.",
    backstory="""A meticulous data gatherer with expertise in understanding student profiles and academic aspirations. 
    This agent uses advanced information extraction techniques to compile a holistic view of the student's background, 
    academic interests, and career objectives.""",
)

fee_scholarship_agent = create_agent(
    role="Fee and Scholarship Agent",
    goal="Research and provide detailed information about tuition fees and scholarship opportunities for M.Tech in AI programs.",
    backstory="""A financial research specialist with a deep understanding of international education funding. 
    This agent navigates complex scholarship databases and university financial aid resources to identify the most 
    suitable and affordable options for students pursuing advanced AI education.""",
)

application_assistance_agent = create_agent(
    role="Application Assistance Agent",
    goal="Guide students through the entire application process for M.Tech in Artificial Intelligence programs.",
    backstory="""An expert navigator of university application processes, this agent provides step-by-step guidance, 
    helping students understand and complete application requirements, prepare necessary documentation, 
    and submit compelling applications to top AI programs.""",
)

coordinator_agent = create_agent(
    role="Coordinator Agent",
    goal="Synthesize and coordinate information from all agents to provide a comprehensive university recommendation.",
    backstory="""The master strategist who brings together insights from various specialized agents. 
    This agent analyzes the collected data, rankings, curriculum details, and application insights to 
    craft a personalized and strategic recommendation that aligns perfectly with the student's academic and career goals.""",
    allow_delegation=True,
)