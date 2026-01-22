from crewai import Crew, Process
from .agents import create_agents
from .tasks import create_tasks

def run_market_intelligence_crew(industry: str):
    # Create Agents
    agents = create_agents()
    
    # Create Tasks
    tasks = create_tasks(agents, industry)
    
    # Instantiate Crew
    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    # Kickoff
    result = crew.kickoff()
    return result
