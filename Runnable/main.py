import random
from abc import ABC, abstractmethod

class Runnable(ABC):

    @abstractmethod
    def invoke(self, input):
        pass

class DummyLLM(Runnable):

    def __init__(self):
        print("Initializing DummyLLM")

    def invoke(self, input):
        return self.predict(input)

    def predict(self, input):
        print("Predicting with DummyLLM for input:", input)
        response_list = [
            "Delhi is capital of India",
            "Mumbai is financial capital of India",
            "Bangalore is IT hub of India",
            "Chennai is cultural capital of India",
            "Kolkata is city of joy"
        ]
        response = random.choice(response_list)
        if input[0] == 0:
            return {'country': 'USA'}
        return {"response": response}
    

class DummyPromptTemplate(Runnable):

    def __init__(self, template, input_variables):
        self.template = template
        self.input_variables = input_variables

    
    def format(self, input):
        formatted_input = self.template.format(**input)
        if input["country"] == "India":
            return (0, formatted_input)
        return (1, formatted_input)
    

    def invoke(self, input):
        return self.format(input)
    

class StrOutputParser(Runnable):

    def __init__(self):
        pass

    def invoke(self, input):
        print("Parsing output:", input)
        if "country" in input:
            return input
        return input["response"]

class RunnableCompose(Runnable):

    def __init__(self, runnable_list):
        self.runnable_list = runnable_list
    
    def invoke(self, input):

        for runnable in self.runnable_list:
            input = runnable.invoke(input)
        return input


model = DummyLLM()

prompt1 = DummyPromptTemplate(
    template="What is the capital of {country}?",
    input_variables=["country"]
)

prompt2 = DummyPromptTemplate(
    template="Population of {country}?",
    input_variables=["country"]
)

output_parser = StrOutputParser()


runnable1 = RunnableCompose([prompt1, model, output_parser])
runnable2 = RunnableCompose([prompt2, model, output_parser])
combined_runnable = RunnableCompose([runnable1, runnable2])

input1 = {"country": "India"}

model_response = combined_runnable.invoke(input1)

print("Model Response:", model_response)