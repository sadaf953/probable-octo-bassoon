import json
import os
import streamlit as st

def read_student_data(data=None):
    """
    Read student data from a dictionary or JSON file.
    
    Args:
        data (dict, optional): Dictionary of student data. 
                                If None, tries to read from a JSON file.
    
    Returns:
        dict: Student data dictionary
    """
    # First, try to read from Streamlit session state
    if 'student_data' in st.session_state and st.session_state.student_data:
        print("Reading from Streamlit session state")
        return st.session_state.student_data
    
    if data is not None:
        return data
    
    # Try reading from a JSON file
    student_data_path = os.path.join(os.path.dirname(__file__), '..', 'student_data.json')
    
    try:
        with open(student_data_path, 'r') as f:
            data = json.load(f)
            print(f"Read data from JSON: {data}")
            return data
    except FileNotFoundError:
        print(f"No student data file found at {student_data_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {student_data_path}")
        return {}

def save_student_data(data):
    """
    Save student data to Streamlit session state and a JSON file.
    
    Args:
        data (dict): Student data dictionary
    """
    # Save to Streamlit session state
    st.session_state.student_data = data
    print(f"Saved to Streamlit session state: {data}")
    
    # Save to JSON file
    student_data_path = os.path.join(os.path.dirname(__file__), '..', 'student_data.json')
    
    try:
        with open(student_data_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Saved to JSON file: {student_data_path}")
    except Exception as e:
        print(f"Error saving student data: {e}")
