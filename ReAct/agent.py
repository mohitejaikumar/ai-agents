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
        llm_response = completion(model="gemini/gemini-2.0-flash", messages=self.messages)
        return llm_response.choices[0].message.content