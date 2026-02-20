from typing import Any, Dict
from CustomFramework.tools.function_signature import FunctionSignature


class ArgumentValidator:

    """
    Validates and coerces arguments based on FunctionSignature.
    """

    def __init__(self):
        self._type_map = {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
        }
    
    def validate(self, args: Dict[str, Any], signature: FunctionSignature) -> Dict[str, Any]:
        validated: Dict[str, Any] = {}

        for name, meta in signature.parameters.items():
            if name in args:
                # data type
                val = args[name]
                expected = meta.get("type")

                if expected and expected in self._type_map:

                    target_type = self._type_map[expected]
                    if not isinstance(val, target_type):
                        try:
                            val = target_type(val)
                        except Exception as e:
                            raise TypeError(f"Argument '{name}' should be of type {expected}.")
                validated[name] = val

            else: 
                if "default" in meta:
                    validated[name] = meta["default"]
                else:
                    raise KeyError(f"Missing required argument: {name}")
        return validated


