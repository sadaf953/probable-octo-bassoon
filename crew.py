from crewai import Crew, Process
from tasks import (
    collect_student_info_task,
    rank_universities_task,
    fetch_curriculum_task,
    fetch_fees_scholarships_task,
    assist_application_process_task,
    coordinate_recommendations_task #Added coordinator task
)
from agents import (
    data_collection_agent,
    university_ranking_agent,
    curriculum_fetching_agent,
    fee_scholarship_agent,
    application_assistance_agent,
    coordinator_agent
)
from utils.data_processing import read_student_data #Import read_student_data function
from utils.web_tools import search_tool, docs_tool, file_tool 

# Function to create and run the CrewAI process
def run_crew_process(student_data=None):
    """Runs the CrewAI process with optional student data."""
    if student_data is None:
        try:
            student_data = read_student_data()
        except (FileNotFoundError, ValueError) as e:
            print(f"Error reading student data: {e}. Using default values.")
            student_data = {} #Using default empty dictionary if error occurs
    
    # Update tasks with student data (example - adapt to your task structure)
    collect_student_info_task.description = collect_student_info_task.description.format(**student_data)
    rank_universities_task.description = rank_universities_task.description.format(**student_data)
    fetch_curriculum_task.description = fetch_curriculum_task.description.format(**student_data)
    fetch_fees_scholarships_task.description = fetch_fees_scholarships_task.description.format(**student_data)
    assist_application_process_task.description = assist_application_process_task.description.format(**student_data)

    crew = Crew(
        agents=[
            data_collection_agent,
            university_ranking_agent,
            curriculum_fetching_agent,
            fee_scholarship_agent,
            application_assistance_agent,
            coordinator_agent
        ],
        tasks=[
            collect_student_info_task,
            rank_universities_task,
            fetch_curriculum_task,
            fetch_fees_scholarships_task,
            assist_application_process_task,
            coordinate_recommendations_task # Added Coordinator Task
        ],
        process=Process.sequential, #Consider changing to concurrent if tasks allow
        verbose=True
    )

    try:
        result = crew.kickoff()
        return result
    except Exception as e:
        return f"An error occurred during crew execution: {e}"



# Automatically run kickoff if script is run directly
if __name__ == "__main__":
    result = run_crew_process()
    print(result)

