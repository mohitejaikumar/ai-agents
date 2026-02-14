from research_crew import ResearchCrew
from dotenv import load_dotenv

load_dotenv()

research_crew = ResearchCrew()

result = research_crew.crew().kickoff(inputs={"query": "How much i will get if i convert 100 USD to INR?"})