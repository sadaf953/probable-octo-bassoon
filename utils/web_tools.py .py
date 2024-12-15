from crewai_tools import SerperDevTool
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI # Or your chosen LLM
import requests
from bs4 import BeautifulSoup


import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def create_gemini_llm():
    """Creates a Gemini LLM instance with error handling."""
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    try:
        return ChatGoogleGenerativeAI(
            google_api_key=google_api_key,
            model="gemini-pro",
            temperature=0.5,
            verbose=False  # Set verbose to False for cleaner output
        )
    except Exception as e:
        raise ValueError(f"Error creating Gemini LLM: {e}")

llm = create_gemini_llm() # Initialize LLM here


search_tool = SerperDevTool()

def search_universities(query):
    """Searches for universities using SerperDevTool."""
    try:
        results = search_tool.search(query)
        return results
    except Exception as e:
        raise ValueError(f"Error searching for universities: {e}")

def scrape_university_website(url):
    """Scrapes university data from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # ... (your web scraping logic here) ...
        return extracted_data
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error scraping website: {e}")
    except Exception as e:
        raise ValueError(f"Error processing website data: {e}")

def initialize_langchain_agent(llm):
    """Initializes a Langchain agent with various tools."""
    tools = load_tools(["serpapi", "llm-math"], llm=llm)
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent


def scrape_website(url, timeout_seconds=10):
    """Scrapes a website and extracts key information with error handling and timeout."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout_seconds)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error fetching URL: {e}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {e}")


def extract_text_content(soup):
    """Extracts text content from a BeautifulSoup object, cleaning it up."""
    for element in soup(["script", "style"]):
        element.extract()
    text = soup.get_text(separator="\n")
    cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    return cleaned_text


def validate_url(url):
    """Validates a URL using a regular expression."""
    url_pattern = re.compile(
        r"^https?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return bool(url_pattern.match(url))