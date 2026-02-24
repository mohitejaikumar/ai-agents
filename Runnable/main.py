import random

class DummyLLM:

    def __init__(self):
        print("Initializing DummyLLM")

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
        return response
    

class DummyPromtTemplate:

    def __init__(self, template, input_variables):
        self.template = template
        self.input_variables = input_variables

    
    def format(self, input):
        formatted_input = self.template.format(**input)
        return formatted_input
    

model = DummyLLM()

prompt = DummyPromtTemplate(
    template="What is the capital of {country}?",
    input_variables=["country"]
)

input = {"country": "India"}

formatted_input = prompt.format(input)

model_response = model.predict(formatted_input)

print("Model Response:", model_response)