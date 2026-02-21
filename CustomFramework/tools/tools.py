from typing import Callable, Any
from CustomFramework.tools.argument_validator import ArgumentValidator
from CustomFramework.tools.function_signature import FunctionSignature


class Tool:

    """
    Wraps a callable for standardized signature introspection and invocation.
    """

    def __init__(
        self, 
        function: Callable,
        signature: FunctionSignature,
        validator: ArgumentValidator
    ) -> None:
        
        self._fn = function
        self.signature = signature
        self._validator = validator

    
    def __call__(
        self, 
        **kwargs: Any
    ) -> Any:
        args = self._validator.validate(kwargs, self.signature)
        print("Invoking '%s' with arguments: %s", self.signature.name, args)
        return self._fn(**args)
    
    def info(self) -> str:
    
        """Returns the JSON representation of this tool's signature."""
    
        return self.signature.to_json()



def tool(func: Callable) -> Tool:
    """
    Decorator that converts a function into a Tool with introspected signature.
    """
    
    sig = FunctionSignature(func)
    
    validator = ArgumentValidator()
    
    return Tool(function=func, signature=sig, validator=validator)
