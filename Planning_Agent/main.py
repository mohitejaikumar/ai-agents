from dotenv import load_dotenv
from Planning_Agent.agent import MyAgent
from Planning_Agent.system_prompt import system_prompt
from Planning_Agent.tools import lookup_population, math
import re 

load_dotenv()

def agent_loop(query, system_prompt: str = ""):

    my_agent = MyAgent(system=system_prompt)

    available_tools = {
        "math": math,
        "lookup_population": lookup_population
    }
    
    current_prompt = query
    
    while "ANSWER" not in current_prompt:
    
        llm_response = my_agent.complete(current_prompt)
        print(llm_response)

        if "Answer" in llm_response:
            break
              
        elif "Plan:" in llm_response or "Step:" in llm_response:
            current_prompt = ""
        
        elif "Execute:" in llm_response:
            pattern = r"Step\s+\d+:\s*(\w+):\s*(.*)"
            match = re.search(pattern, llm_response)
            
            if match:
                chosen_tool = match.group(1)
                arg = match.group(2)

                if chosen_tool in available_tools:
                    observation = available_tools[chosen_tool](arg)
                    current_prompt = f"Observation: {observation}"

                else:
                    current_prompt = f"Observation: Tool not available. Retry!"


agent_loop("What is the population of Japan plus the population of India?", system_prompt)