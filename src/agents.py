from crewai import Agent, LLM
from .tools import github_trends_search, rss_feed_reader, wikipedia_search
import os

def create_agents():
    # Configure DeepSeek R1 LLM via OpenRouter
    llm = LLM(
        model="deepseek/deepseek-r1-0528:free",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
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
