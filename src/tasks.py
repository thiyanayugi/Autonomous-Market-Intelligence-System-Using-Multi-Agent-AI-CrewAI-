from crewai import Task
from textwrap import dedent

def create_tasks(agents, industry):
    collector, analyst, strategist, writer = agents

    # Task 1: Data Collection
    collection_task = Task(
        description=dedent(f"""
            Collect high-quality, relevant open-source data for market analysis on the industry: {industry}.
            
            Sources to check:
            - Wikipedia (industry overview)
            - Public GitHub repositories (technology trends) - Use the GitHub tool
            - Search for public open datasets or reports using search tool
            - Public RSS feeds or blogs using RSS tool if relevant URLs are found or known
            
            Summarize what data was collected and why it matters.
            
            Rules:
            - Do NOT interpret or analyze trends yet.
            - Do NOT speculate.
            - Output must be structured.
        """),
        expected_output=dedent("""
            DATA SOURCES:
            - Source Name:
              - Type:
              - Key Information Extracted:
              - Relevance:
            ... (repeat for sources)
        """),
        agent=collector
    )

    # Task 2: Trend Analysis
    analysis_task = Task(
        description=dedent(f"""
            Analyze the collected data to identify meaningful market and technology trends for {industry}.
            
            Responsibilities:
            - Analyze frequency of topics
            - Identify growth/decline signals
            - Identify technology adoption patterns
            - Identify 3-5 key trends
            - Clearly explain *why* each trend matters
            
            Rules:
            - Base conclusions strictly on collected data.
            - Avoid buzzwords.
            - Rank trends by impact.
        """),
        expected_output=dedent("""
            TREND:
            - Name:
            - Evidence:
            - Impact Level (High / Medium / Low):
            - Explanation:
            ... (repeat for 3-5 trends)
        """),
        agent=analyst,
        context=[collection_task]
    )

    # Task 3: Strategy
    strategy_task = Task(
        description=dedent(f"""
            Convert the identified trends into actionable business risks and opportunities for {industry}.
            
            Responsibilities:
            - Identify strategic risks
            - Identify growth opportunities
            - Connect each risk/opportunity to a trend
            - Suggest mitigation or exploitation strategies
            
            Rules:
            - Be practical.
            - No vague recommendations.
        """),
        expected_output=dedent("""
            OPPORTUNITY:
            - Description:
            - Supporting Trend:
            - Business Impact:
            - Recommended Action:

            RISK:
            - Description:
            - Supporting Trend:
            - Business Impact:
            - Mitigation Strategy:
            ... (repeat as needed)
        """),
        agent=strategist,
        context=[analysis_task]
    )

    # Task 4: Reporting
    reporting_task = Task(
        description=dedent(f"""
            Synthesize all outputs into a CEO-level market intelligence brief for {industry}.
            
            Responsibilities:
            - Write in clear business language.
            - Keep the report under 2 pages.
            - Use bullet points and headings.
            
            Report Structure:
            TITLE
            Executive Summary
            Market Overview
            Key Trends
            Risks & Opportunities
            Strategic Recommendations
            Data Sources & Assumptions
            
            Rules:
            - No raw data.
            - No technical jargon unless necessary.
            - No repetition.
            - No hallucinated statistics.
        """),
        expected_output="A Markdown formatted executive report.",
        agent=writer,
        context=[collection_task, analysis_task, strategy_task],
        output_file='market_intelligence_report.md'
    )

    return [collection_task, analysis_task, strategy_task, reporting_task]
