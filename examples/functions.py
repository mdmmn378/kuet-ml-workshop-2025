import os
import requests
import dotenv

dotenv.load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

assert OPENWEATHER_API_KEY, "Please set OPENWEATHER_API_KEY environment variable"

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]


def get_weather(location: str) -> str | None:
    print("Fetching weather data for", location)
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            output = ""
            output += f"{data['weather'][0]['description'].title()} in {location}. "
            output += f"Temperature is {data['main']['temp']}°C. "
            output += f"Feels like {data['main']['feels_like']}°C. "
            return output
        else:
            return None

    except requests.RequestException as e:
        print("Error fetching weather data:", e)
        return None


REGISTERED_FUNCTIONS = {
    "get_weather": get_weather
}

if __name__ == "__main__":
    location = "khulna"
    print(get_weather(location))