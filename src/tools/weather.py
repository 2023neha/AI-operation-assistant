import requests
from .base import BaseTool

class WeatherTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get current weather for a city. Returns temperature and conditions."
        )

    def get_parameters_schema(self):
        return {
            "type": "object",
            "properties": {
                "latitude": {"type": "number", "description": "Latitude of the location"},
                "longitude": {"type": "number", "description": "Longitude of the location"},
                "city": {"type": "string", "description": "Name of the city (e.g., London, Tokyo)"}
            },
            "required": ["city"]
        }

    def _get_lat_long(self, city):
        try:
            url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            response = requests.get(url).json()
            if "results" in response and response["results"]:
                return response["results"][0]["latitude"], response["results"][0]["longitude"]
            return None, None
        except Exception:
            return None, None

    def run(self, city=None, latitude=None, longitude=None, **kwargs):
        if not latitude or not longitude:
            if city:
                latitude, longitude = self._get_lat_long(city)
                if not latitude:
                    return f"Could not find coordinates for city: {city}"
            else:
                return "Please provide a city or latitude/longitude."

        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
            response = requests.get(url).json()
            current = response.get("current_weather", {})
            return f"Current weather in {city or 'coordinates'}: {current.get('temperature')}°C, Windspeed: {current.get('windspeed')} km/h"
        except Exception as e:
            return f"Error fetching weather: {str(e)}"
