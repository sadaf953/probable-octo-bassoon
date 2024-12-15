import os
from dotenv import load_dotenv

# Selective imports to avoid OpenAI dependencies
from crewai_tools import (
    SerperDevTool, 
    FileReadTool, 
    DirectoryReadTool
)
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Use SerperDevTool to search for universities instead of web scraping
def search_universities(query):
    """
    Use SerperDevTool to search for universities instead of web scraping
    
    Args:
        query (str): Search query for universities
    
    Returns:
        list: Search results
    """
    search_tool = SerperDevTool()
    try:
        search_results = search_tool.search(query)
        return search_results
    except Exception as e:
        print(f"Error during university search: {e}")
        return []

def rank_colleges(data):
    """
    Simplified ranking function
    
    Args:
        data (DataFrame): University data to rank
    
    Returns:
        DataFrame: Ranked universities
    """
    try:
        # Assuming data is a DataFrame or similar structure
        ranked_data = data.sort_values(by=['ranking_criteria'], ascending=False)
        return ranked_data.head(15)
    except Exception as e:
        print(f"Error ranking colleges: {e}")
        return []

def generate_report(ranked_data):
    """
    Generate a report of top universities
    
    Args:
        ranked_data (DataFrame): Ranked university data
    """
    try:
        with open('output.txt', 'w') as f:
            f.write("Top 15 Universities for M.Tech in Artificial Intelligence in Australia\n")
            f.write("===============================================================\n")
            f.write("University Name\tRanking\tScholarships\tCurriculum\tURL\n")
            f.write("---------------------------------------------------------------\n")
            for index, row in ranked_data.iterrows():
                f.write(f"{row['university_name']}\t{row['ranking']}\t{row['scholarships']}\t{row['curriculum']}\t{row['url']}\n")
    except Exception as e:
        print(f"Error generating report: {e}")

def read_student_data(file_path='students.txt'):
    """
    Read student data from a text file
    
    Args:
        file_path (str): Path to the student data file
    
    Returns:
        dict: Student data
    """
    student_data = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split(':')
                student_data[key.strip()] = value.strip()
        return student_data
    except Exception as e:
        print(f"Error reading student data: {e}")
        return {}

# Gemini LLM configuration with robust error handling
def create_gemini_llm():
    """
    Create a Gemini LLM instance
    
    Returns:
        ChatGoogleGenerativeAI: Configured Gemini LLM instance
    """
    try:
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            raise ValueError("Google API Key not found in environment variables")
        
        return ChatGoogleGenerativeAI(
            google_api_key=google_api_key,
            model="gemini-pro",
            temperature=0.5
        )
    except Exception as e:
        print(f"Error creating Gemini LLM: {e}")
        return None

# Initialize LLM
llm = create_gemini_llm()

# Tools configuration
file_tool = FileReadTool()
search_tool = SerperDevTool()
docs_tool = DirectoryReadTool(directory='./blog-posts')

# Export the tools and functions
__all__ = [
    'search_universities', 
    'rank_colleges', 
    'generate_report', 
    'read_student_data', 
    'file_tool', 
    'search_tool', 
    'docs_tool', 
    'llm'
]
