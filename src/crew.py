from crewai import Crew, Process
from .agents import create_agents
from .tasks import create_tasks
import os
from datetime import datetime

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
    
    # Save output to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"market_intelligence_report_{timestamp}.md"
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# Market Intelligence Report: {industry}\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write(str(result))
    
    print(f"\n✅ Report saved to: {output_filename}")
    
    return result
