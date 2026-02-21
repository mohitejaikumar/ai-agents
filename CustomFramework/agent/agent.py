from typing import Dict, List, Optional
import os
from textwrap import dedent
from dotenv import load_dotenv
import litellm
import json
import logging
from CustomFramework.tools.tools import Tool
from CustomFramework.agent.utils import TagParser, MessageHistory, create_message
from CustomFramework.agent.prompt import REACT_PROMPT

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class Agent:
    def __init__(
        self,
        name: str,
        backstory: str,
        task_description: str,
        expected_output_format: Optional[str] = None,
        tools: Optional[list[Tool]] = None,
        llm_model: str = "gpt-4o"
    ) -> None:
        load_dotenv()
        self.model = f"{llm_model}"

        self.name = name
        self.backstory = backstory
        self.task_description = task_description
        self.expected_output_format = expected_output_format
        self.tools = tools or []
        self.llm_model = llm_model

        self.tools_dict = {t.signature.name: t for t in self.tools}

        self._parse_response = TagParser("response")
        self._parse_thought = TagParser("thought")
        self._parse_tool = TagParser("tool_call")

        self.dependencies = []
        self.dependents = []
        self.context_messages = []

    def precedes(self, other):
        self.dependents.append(other)
        other.dependencies.append(self)
        return other
    
    def succeeds(self, other):
        other.dependents.append(self)
        self.dependencies.append(other)
        return other
    
    def receive_context(self, data):
        message = f"From {self.name}'s dependency: {data}"

        self.context_messages.append(message)

    def _build_prompt(self) -> str:

        context_block = "\n".join(self.context_messages)

        prompt = dedent(
            f"""
            <task_description>
            {self.task_description}
            </task_description>

            <task_expected_output>
            {self.expected_output_format or ""}
            </task_expected_output>

            <context>
            {context_block}
            </context>
            """
        ).strip()
        return prompt
    
    def _react_prompt(self):

        tools_block = "\n".join(t.info() for t in self.tools)
        return REACT_PROMPT % tools_block
    
    def _run_tool_calls(self, calls):
        observations = {}

        for call_str in calls:
            print("Processing tool call: %s", call_str)
            call = json.loads(call_str)
            name = call["name"]
            tool = self.tools_dict.get(name)
            args = call["arguments"]
            
            result = tool(**args)
            observations[int(call["id"])] = result

        return observations
    
    def _generate_response(self, conversation: List[Dict[str, str]]) -> str:
        """
        Uses LiteLLM to generate a response from OpenAI models.
        """
        try:
            response = litellm.completion(
                model=self.model,
                messages=conversation,
                api_base="http://localhost:11434"
            )
            return response["choices"][0]["message"]["content"]
        except Exception:
            logger.exception("Error calling OpenAI via LiteLLM")
            raise
    
    def run(self, user_message: Optional[str] = None, max_rounds = 5):

        prompt = self._build_prompt() if user_message is None else user_message
        logger.info("Agent %s running with prompt: %s", self.name, prompt)

        if self.tools:
            history = MessageHistory()
            system_prompt = self.backstory + "\n" + self._react_prompt()
            history.append(create_message("system", system_prompt))
            history.append(create_message("user", prompt, tag="question"))

            for round_idx in range(max_rounds):
                completion = self._generate_response(history.all())
                resp = self._parse_response.parse(completion)
                if resp.found:
                    result = resp.items[0]
                    break
                print("Agent completion: %s", completion)
                thought = self._parse_thought.parse(completion)
                tool_calls = self._parse_tool.parse(completion)
                history.append(create_message("assistant", completion))
                if thought.found:
                    logging.debug("Agent thought: %s", thought.items[0])
                if tool_calls.found:
                    observations = self._run_tool_calls(tool_calls.items)
                    logging.debug("Observations: %s", observations)
                    history.append(create_message("user", json.dumps(observations)))
                    continue
            else:
                # Fallback
                logging.warning("Max rounds reached without a final response.")
                result = self._generate_response(history.all())
        else:
            # Standard LLM agent
            system_prompt = self.backstory
            history = MessageHistory()
            history.append(create_message("system", system_prompt))
            history.append(create_message("user", user_message))
            result = self._generate_response(history.all())
        
        logging.info("Agent '%s' final response: %s", self.name, result)
        for dep in self.dependents:
            dep.receive_context(result)
        return result
            
                    
