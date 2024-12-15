from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

# Load environment variables
load_dotenv()

# Get the API key
groq_api_key = os.getenv('GROQ_API_KEY')

# Check if API key is present
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

try:
    llm = ChatGroq(model="mixtral-8x7b-32768",
        verbose=True,
        temperature=0.5,
        api_key=groq_api_key
    )

    # Use invoke instead of direct call
    response = llm.invoke("Test message to verify ChatGroq functionality.")
    print(response)
except Exception as e:
    print(f"An error occurred: {e}")

