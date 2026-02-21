from CustomFramework.crew import Crew
from CustomFramework.tools.tools import tool
from CustomFramework.agent.agent import Agent

@tool
def double(x: int) -> int:
    """Doubles a number."""
    return 2 * x

@tool
def square(x: int) -> int:
    """Squares a number."""
    return x * x

with Crew():
    a = Agent(
        name="DoubleAgent",
        backstory="You're a math agent",
        task_description="Double the number 4",
        tools=[double]
    )
    b = Agent(
        name="SquareAgent",
        backstory="You're a math agent",
        task_description="Now square the result",
        tools=[square]
    )
    a.precedes(b)

    Crew._active.run_all()

