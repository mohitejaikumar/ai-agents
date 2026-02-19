from litellm import completion
import os
from dotenv import load_dotenv
import re
from ReAct.tools import lookup_population, math
from ReAct.agent import MyAgent
from ReAct.system_prompt import system_prompt

load_dotenv()



def agent_loop(query, system_prompt: str = ""):

    my_agent = MyAgent(system=system_prompt)

    available_tools = {"math": math,
                       "lookup_population": lookup_population}

    current_prompt = query
    previous_step = ""
  
    while "ANSWER" not in current_prompt:
        llm_response = my_agent.complete(current_prompt)
        print(llm_response)

        if "Answer" in llm_response:
            break

        elif "Thought:" in llm_response:
            previous_step = "Thought"
            current_prompt = ""

        elif "PAUSE" in llm_response and previous_step == "Thought":
            current_prompt = ""
            previous_step = "PAUSE"

        elif "Action:" in llm_response:
            previous_step = "Action"
            pattern = r"Action:\s*(\w+):\s*(.+)"

            match = re.search(pattern, llm_response)

            if match:
                chosen_tool = match.group(1)
                arg = match.group(2)

                if chosen_tool in available_tools:
                    observation = available_tools[chosen_tool](arg)
                    current_prompt = f"Observation: {observation}"

                else:
                    current_prompt = f"Observation: Tool not available. Retry the action."

            else:
                observation = "Observation: Tool not found. Retry the action."


agent_loop("What is double the population of Japan?", system_prompt)