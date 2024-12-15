from crewai import Agent
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import streamlit as st
import os
from tools import *
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

# Check if Google API key is set
if not os.getenv('GOOGLE_API_KEY'):
    st.error("Google API Key is not set. Please set the GOOGLE_API_KEY in your .env file.")
    raise ValueError("Google API Key is missing")

# Use Gemini LLM
llm = ChatGoogleGenerativeAI(
    google_api_key=os.getenv('GOOGLE_API_KEY'),
    model="gemini-pro",
    temperature=0.5,
    verbose=True
)

university_ranking_agent = Agent(
    role="University Ranking Agent",
    goal="Rank universities for M.Tech in Artificial Intelligence in Australia based on curriculum quality, fees, and global reputation.",
    backstory="""The University Ranking Agent has been developed with an extensive background in higher education consulting and academic research. 
    With years of experience in evaluating and ranking educational institutions, this agent has access to a wide range of global databases, 
    allowing it to analyze a university's curriculum, faculty, research output, and industry connections. It leverages advanced data 
    analysis techniques to compare institutions and identify the top programs tailored to the student's specific academic and career goals. 
    The agent is particularly adept at understanding the evolving landscape of AI education and can pinpoint which universities are 
    leading in this cutting-edge field.""",
    tools=[],
    llm=llm,  
    allow_delegation=False,
    verbose=True,
)

curriculum_fetching_agent = Agent(
    role="Curriculum Fetching Agent",
    goal="Fetch detailed curriculum information for M.Tech in Artificial Intelligence programs from top universities in Australia.",
    backstory="""The Curriculum Fetching Agent is like a librarian with specialized knowledge in the field of artificial intelligence education. 
    Having spent years curating academic resources, this agent has developed an intuitive understanding of what makes a curriculum truly 
    effective. It digs deep into university course offerings, syllabi, and academic catalogs to extract comprehensive details about 
    AI programs, ensuring students get the most relevant and up-to-date information.""",
    tools=[],
    llm=llm,  
    allow_delegation=False,
    verbose=True,
)

data_collection_agent = Agent(
    role="Data Collection Agent",
    goal="Collect comprehensive student information and preferences for M.Tech in Artificial Intelligence programs.",
    backstory="""A meticulous data gatherer with expertise in understanding student profiles and academic aspirations. 
    This agent uses advanced information extraction techniques to compile a holistic view of the student's background, 
    academic interests, and career objectives.""",
    tools=[],
    llm=llm,  
    allow_delegation=False,
    verbose=True,
)

fee_scholarship_agent = Agent(
    role="Fee and Scholarship Agent",
    goal="Research and provide detailed information about tuition fees and scholarship opportunities for M.Tech in AI programs.",
    backstory="""A financial research specialist with a deep understanding of international education funding. 
    This agent navigates complex scholarship databases and university financial aid resources to identify the most 
    suitable and affordable options for students pursuing advanced AI education.""",
    tools=[],
    llm=llm,  
    allow_delegation=False,
    verbose=True,
)

application_assistance_agent = Agent(
    role="Application Assistance Agent",
    goal="Guide students through the entire application process for M.Tech in Artificial Intelligence programs.",
    backstory="""An expert navigator of university application processes, this agent provides step-by-step guidance, 
    helping students understand and complete application requirements, prepare necessary documentation, 
    and submit compelling applications to top AI programs.""",
    tools=[],
    llm=llm,  
    allow_delegation=False,
    verbose=True,
)

coordinator_agent = Agent(
    role="Coordinator Agent",
    goal="Synthesize and coordinate information from all agents to provide a comprehensive university recommendation.",
    backstory="""The master strategist who brings together insights from various specialized agents. 
    This agent analyzes the collected data, rankings, curriculum details, and application insights to 
    craft a personalized and strategic recommendation that aligns perfectly with the student's academic and career goals.""",
    tools=[],
    llm=llm,  
    allow_delegation=True,
    verbose=True,
)
