import sys
import os
from dotenv import load_dotenv
from src.crew import run_market_intelligence_crew

# Load environment variables
load_dotenv()

def main():
    print("Welcome to the Autonomous Market Intelligence Agent")
    print("---------------------------------------------------")
    
    # Default industry
    default_industry = "Artificial Intelligence Tools Market (2024–2026)"
    
    if len(sys.argv) > 1:
        industry = " ".join(sys.argv[1:])
    else:
        print(f"No industry provided. Using default: {default_industry}")
        industry = default_industry
        
    print(f"\nStarting analysis for: {industry}\n")
    
    try:
        result = run_market_intelligence_crew(industry)
        print("\n\n########################")
        print("## ANALYSIS COMPLETED ##")
        print("########################\n")
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
