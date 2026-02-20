import inspect
import json
import logging
from typing import Any, Dict, Callable, Optional, Type


class FunctionSignature:
    def __init__(self, func: Callable) -> None:
        sig = inspect.signature(func)
        self.name = func.__name__
        self.description = (func.__doc__ or "").strip() or None
        self.parameters = {}

        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            
            info = {}
            if param.annotation is not inspect._empty:
                annot = param.annotation
                if hasattr(annot, "__name__"):
                    info["type"] = annot.__name__
                else:
                    info["type"] = str(annot)
            
            if param.default is not inspect._empty:
                info["default"] = param.default

            self.parameters[param_name] = info
            
        self.return_type: Optional[str] = None
        if sig.return_annotation is not inspect._empty:
            ret_annot = sig.return_annotation
            if hasattr(ret_annot, "__name__"):
                self.return_type = ret_annot.__name__
            else:
                self.return_type = str(ret_annot)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "return_type": self.return_type
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())


