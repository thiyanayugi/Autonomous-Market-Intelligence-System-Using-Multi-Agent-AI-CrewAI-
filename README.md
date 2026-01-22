# Autonomous Market Intelligence Agent

An advanced multi-agent AI system using CrewAI to collect, analyze, and synthesize market intelligence using ONLY open-source and publicly available data.

## Description
This system employs four specialized agents:
1. **Open Data Collector**: Gathers data from Wikipedia, GitHub, and RSS feeds.
2. **Trend Analysis Agent**: Identifies key trends from the collected data.
3. **Risk & Opportunity Strategist**: Analyzes implications of the trends.
4. **Executive Intelligence Report Writer**: Synthesizes everything into a CEO-level report.

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up environment variables in `.env` (see `.env.example`).
3. Run the analysis:
   ```bash
   python -m src.main "Your Industry Here"
   ```
   If no industry is provided, it defaults to "Artificial Intelligence Tools Market (2024–2026)".

## License
MIT

---
“This project demonstrates autonomous multi-agent market intelligence using only open-source data, designed for executive decision-making.”
