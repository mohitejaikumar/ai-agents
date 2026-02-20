from typing import Callable
from CustomFramework.tools.argument_validator import ArgumentValidator
from CustomFramework.tools.function_signature import FunctionSignature
from CustomFramework.tools.tools import Tool

def tool(func: Callable) -> Tool:
    """
    Decorator that converts a function into a Tool with introspected signature.
    """
    
    sig = FunctionSignature(func)
    
    validator = ArgumentValidator()
    
    return Tool(function=func, signature=sig, validator=validator)


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b


print(multiply(a=True))  # Should print 12