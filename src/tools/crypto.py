import requests
from .base import BaseTool

class CryptoTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="get_crypto_price",
            description="Get current price of a cryptocurrency in USD."
        )

    def get_parameters_schema(self):
        return {
            "type": "object",
            "properties": {
                "coin_id": {"type": "string", "description": "The API ID of the coin (e.g., bitcoin, ethereum)"},
                "currency": {"type": "string", "description": "Target currency (default: usd)"}
            },
            "required": ["coin_id"]
        }

    def run(self, coin_id, currency="usd", **kwargs):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
            response = requests.get(url).json()
            if coin_id in response:
                return f"The price of {coin_id} is {response[coin_id][currency]} {currency.upper()}"
            else:
                return f"Could not find price for {coin_id}. Check if the coin ID is correct."
        except Exception as e:
            return f"Error fetching crypto price: {str(e)}"
