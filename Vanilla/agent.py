from crewai import LLM, Agent, Crew, Agent, Process, Task
import yaml
import os
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

serper_dev_tool = SerperDevTool()

llm = LLM(
    model="ollama/llama3.2:1b",
    base_url="http://localhost:11434"
)

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)



research_agent = Agent(
    role=config["agents"]["research_agent"]["role"],
    goal=config["agents"]["research_agent"]["goal"],
    backstory=config["agents"]["research_agent"]["backstory"],
    tools=[serper_dev_tool],
    llm=llm,
    verbose=True
)

research_task = Task(
    description=config["tasks"]["research_task"]["description"],
    agent=research_agent,
    tools=[serper_dev_tool],
    expected_output=config["tasks"]["research_task"]["expected_output"]
)


summarization_agent = Agent(
    role=config["agents"]["summarization_agent"]["role"],
    goal=config["agents"]["summarization_agent"]["goal"],
    backstory=config["agents"]["summarization_agent"]["backstory"],
    llm=llm,
    verbose=True
)

fact_checker_agent = Agent(
    role=config["agents"]["fact_checker_agent"]["role"],
    goal=config["agents"]["fact_checker_agent"]["goal"],
    backstory=config["agents"]["fact_checker_agent"]["backstory"],
    tools=[serper_dev_tool],
    llm=llm,
    verbose=True
)

summarization_task = Task(
    description=config["tasks"]["summarization_task"]["description"],
    agent=summarization_agent,
    expected_output=config["tasks"]["summarization_task"]["expected_output"],
)

fact_checking_task = Task(
    description=config["tasks"]["fact_checking_task"]["description"],
    agent=fact_checker_agent,
    tools=[serper_dev_tool],
    expected_output=config["tasks"]["fact_checking_task"]["expected_output"],
)

research_crew = Crew(
    agents=[research_agent, summarization_agent, fact_checker_agent],
    tasks=[research_task, summarization_task, fact_checking_task],
    process=Process.sequential,
    verbose=True
)

result = research_crew.kickoff(inputs={"search_query": "What is LLM?"})
# result = serper_dev_tool.run(search_query="What is LLM?")
print("\nFinal Verified Summary:\n", result)