from pydantic import BaseModel, Field
from typing import Type
from crewai.tools import BaseTool
import os
from dotenv import load_dotenv
import requests

load_dotenv()

class CurrencyConverterInput(BaseModel):
    amount: float = Field(..., description="The amount of money to convert")
    from_currency: str = Field(..., description="The source currency code to convert from (e.g., USD)")
    to_currency: str = Field(..., description="The target currency code to convert to (e.g., EUR)")


class CurrencyConversionTool(BaseTool):
    name: str = "Currency Converter Tool"
    description: str = "Convert an amount from one currency to another"
    args_schema: Type[BaseTool] = CurrencyConverterInput
    api_key: str = os.getenv("EXCHANGE_RATE_API_KEY")


    def _run(self, amount: float, from_currency: str, to_currency: str) -> str:
        
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{from_currency}"
        response = requests.get(url)

        if response.status_code != 200:
            return f"Error fetching exchange rates: {response.status_code}"
        
        data = response.json()

        if "conversion_rates" not in data or to_currency not in data["conversion_rates"]:
            return f"Error: Invalid currency code: {to_currency}"
        
        rate = data["conversion_rates"][to_currency]
        conversion_result = amount * rate

        return f"{amount} {from_currency} is approximately {conversion_result:.2f} {to_currency} at the current exchange rate of {rate:.4f}."
