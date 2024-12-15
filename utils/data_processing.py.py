import pandas as pd
from langchain.vectorstores import FAISS # Example - replace with your choice
from langchain.embeddings import OpenAIEmbeddings # Example - replace with your choice

def read_student_data(file_path='students.txt'):
    """Reads student data from a text file with error handling."""
    student_data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # Added encoding for better compatibility
            for line in file:
                key, value = line.strip().split(':', 1) # Split only at the first ':'
                student_data[key.strip()] = value.strip()
        return student_data
    except FileNotFoundError:
        raise FileNotFoundError(f"Student data file not found at: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading student data: {e}")

def parse_university_data(file_path):
    """Parses university data from a CSV file."""
    try:
        df = pd.read_csv(file_path)  # Reads the CSV file into a Pandas DataFrame
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV file is empty: {file_path}")
    except pd.errors.ParserError:
        raise ValueError(f"Error parsing CSV file: {file_path}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {e}")

def create_vector_store(data, embedding_model=None):
    """Creates a vector store from university data."""
    if embedding_model is None:
        embedding_model = SentenceTransformer('all-mpnet-base-v2') # Example - replace with your choice

    try:
        # Example using FAISS - replace with your preferred vector store
        vectorstore = FAISS.from_documents(data, embedding_model)
        return vectorstore
    except Exception as e:
        raise ValueError(f"Error creating vector store: {e}")

def generate_report(ranked_data, output_file='output.txt'):
    """Generates a report of top universities."""
    try:
        ranked_data.to_csv(output_file, sep='\t', index=False)
        return f"Report generated successfully to {output_file}"
    except Exception as e:
        raise ValueError(f"Error generating report: {e}")
from crewai_tools import FileReadTool, DirectoryReadTool

file_tool = FileReadTool()
docs_tool = DirectoryReadTool(directory='./storage') #Assumes blog-posts directory exists