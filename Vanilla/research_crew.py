from crewai import LLM, Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool
from currency_conversion_tool import CurrencyConverterInput, CurrencyConversionTool


## Modular Crew class

@CrewBase
class ResearchCrew:
    """A crew for constructing reseach,
    summarizing findings and fact-checking the summary.
    """
    agents_config = 'config/agents.yaml' # auto loads the agents
    tasks_config = 'config/tasks.yaml' # auto loads the tasks

    def __init__(self):
        self.search_tool = SerperDevTool()
        self.currency_conversion_tool = CurrencyConversionTool()
        self.llm = LLM(
            model="ollama/llama3.2:1b",
            base_url="http://localhost:11434"
        )

    
    @agent
    def query_parser_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['query_parser_agent'],
            llm = self.llm
        )
    
    @agent
    def currency_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['currency_analyst'],
            tools=[self.currency_conversion_tool],
            llm = self.llm
        )
    
    @task
    def query_parser_task(self) -> Task:
        return Task(
            config=self.tasks_config['query_parser_task'],
            output_pydantic=CurrencyConverterInput
        )
    
    @task
    def currency_conversion_task(self) -> Task:
        return Task(
            config=self.tasks_config['currency_conversion_task'],
            tools=[self.currency_conversion_tool]
        )
    

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
        )