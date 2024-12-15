from crewai import Crew, Process
from task import (
    collect_student_info_task,
    rank_universities_task,
    fetch_curriculum_task,
    fetch_fees_scholarships_task,
    assist_application_process_task
)
from agents import (
    data_collection_agent,
    university_ranking_agent,
    curriculum_fetching_agent,
    fee_scholarship_agent,
    application_assistance_agent,
    coordinator_agent
)

# Forming the tech-focused crew with enhanced configuration
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
        assist_application_process_task
    ],
    process=Process.sequential,
    verbose=True  # Changed from 2 to True
)

# Optional: Add a method to kickoff the crew with default or provided inputs
def kickoff_crew(inputs=None):
    """
    Kickoff the crew with optional input overrides
    
    Args:
        inputs (dict, optional): Student information dictionary
    
    Returns:
        str: Crew's recommendation result
    """
    try:
        # If inputs are provided, you might want to update tasks or agents
        if inputs:
            # Placeholder for potential input handling
            pass
        
        # Kickoff the crew and get the result
        result = crew.kickoff()
        return result
    except Exception as e:
        print(f"An error occurred during crew kickoff: {e}")
        return None

# Automatically run kickoff if script is run directly
if __name__ == "__main__":
    result = kickoff_crew()
    print(result)
