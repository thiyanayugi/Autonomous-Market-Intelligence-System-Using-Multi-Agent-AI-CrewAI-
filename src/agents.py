from crewai import Agent, LLM
from .tools import github_trends_search, rss_feed_reader, wikipedia_search
import os

def create_agents():
    import os
    from pathlib import Path
    from dotenv import load_dotenv
    
    # Load env file safely
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    # Configure LLM using OpenAI compatibility
    # CrewAI/LiteLLM will pick up OPENAI_API_KEY and OPENAI_API_BASE from env automatically
    # We just need to specify the model with 'openai/' prefix if we want to force that path,
    # or just pass the model name if LiteLLM handles it. 
    # For OpenRouter via OpenAI compat, 'openai/<model_name>' usually works best 
    # when API_BASE is set to openrouter.

    model_name = os.getenv("LLM_MODEL", "deepseek/deepseek-r1-0528:free")
    
    llm = LLM(
        model=f"openai/{model_name}",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
        temperature=0.7
    )
    
    # Agent 1: Open Data Collector
    collector = Agent(
        role='Market Data Intelligence Collector',
        goal='Collect high-quality, relevant open-source data for market analysis on {industry}',
        backstory=(
            "You are a senior market researcher skilled at extracting insights from public data sources. "
            "You know how to separate noise from signal. You strictly use open data."
        ),
        tools=[wikipedia_search, github_trends_search, rss_feed_reader],
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    # Agent 2: Trend Analysis Agent
    analyst = Agent(
        role='Market Trend Analyst',
        goal='Identify meaningful market and technology trends from collected data on {industry}',
        backstory=(
            "You specialize in turning raw information into clear trend signals for leadership teams. "
            "You analyze frequency of topics, growth/decline signals, and adoption patterns."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    # Agent 3: Risk & Opportunity Strategist
    strategist = Agent(
        role='Strategic Risk & Opportunity Analyst',
        goal='Convert trends into actionable business risks and opportunities for {industry}',
        backstory=(
            "You advise executives on where to invest, where to be cautious, and what to monitor. "
            "You connect risks and opportunities to specific trends."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    # Agent 4: Executive Intelligence Report Writer
    writer = Agent(
        role='Executive Intelligence Communicator',
        goal='Produce a CEO-level market intelligence brief for {industry}',
        backstory=(
            "You write reports that busy executives actually read and act upon. "
            "You synthesize outputs into clear business language, keeping reports under 2 pages."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    return collector, analyst, strategist, writer
