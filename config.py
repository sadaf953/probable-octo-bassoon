import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Securely retrieve API keys with default values
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def validate_api_keys():
    """
    Validate that required API keys are set.
    Raises a ValueError if any required key is missing.
    """
    required_keys = ['GOOGLE_API_KEY']
    for key in required_keys:
        if not os.getenv(key):
            raise ValueError(f"{key} is not set. Please set it in your .env file.")

# Call validation when this module is imported
validate_api_keys()
