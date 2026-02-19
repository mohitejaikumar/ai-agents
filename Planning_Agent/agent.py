from litellm import completion


class MyAgent:
    def __init__(self, system = ""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})
            
    def complete(self, message=""):
        if message:
            self.messages.append({"role": "user", "content": message})
        result = self.invoke()
        self.messages.append({"role": "assistant", "content": result})
        return result
        
    def invoke(self):
        llm_response = completion(model="ollama/llama3.2:1b", messages=self.messages, api_base="http://localhost:11434")
        return llm_response.choices[0].message.content