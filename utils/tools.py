import os
from dotenv import load_dotenv
from config import GOOGLE_API_KEY

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
def search_universities(query, country=None):
    """
    Use SerperDevTool to search for universities with enhanced specificity
    
    Args:
        query (str): Search query for universities
        country (str, optional): Country to filter universities
    
    Returns:
        list: Search results with enhanced filtering
    """
    search_tool = SerperDevTool()
    try:
        # Enhance query with additional context
        full_query = f"{query} top universities for masters in artificial intelligence"
        if country:
            full_query += f" in {country}"
        
        search_results = search_tool.search(full_query)
        
        # Additional filtering to ensure relevance
        filtered_results = []
        for result in search_results:
            # Check for keywords that indicate university or academic content
            if any(keyword in result.get('title', '').lower() or 
                   keyword in result.get('snippet', '').lower() for keyword in 
                   ['university', 'college', 'school', 'institute', 'academic', 'ranking', 'program']):
                filtered_results.append(result)
        
        return filtered_results
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
        google_api_key = GOOGLE_API_KEY
        if not google_api_key:
            raise ValueError("Google API Key not found in environment variables")
        
        return ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=google_api_key,
            temperature=0.5,
            provider="google"  # Explicitly specify the provider
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
