from fastmcp import FastMCP
import requests
import json
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
load_dotenv()

mcp = FastMCP("WeatherHub")
def get_weather_api_key():
    api_key = os.getenv("WEATHER_API_KEY")
    return api_key

@mcp.tool()
async def get_current_weather(location: str) -> Dict[str, Any]:
    api_key = get_weather_api_key()
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'q': location,'appid': api_key,'units': 'metric'}
    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status() 
    data = response.json()
    if data.get('cod') != 200:
        return {"error": data.get('message', 'Unknown error')}
    weather_info = {
        "location": data.get("name"),
        "country": data.get("sys", {}).get("country"),
        "temperature_celsius": data.get("main", {}).get("temp"),
        "feels_like_celsius": data.get("main", {}).get("feels_like"),
        "description": data.get("weather", [{}])[0].get("description"),
        "humidity": data.get("main", {}).get("humidity"),
        "wind_speed_mps": data.get("wind", {}).get("speed")
    }
    return weather_info

@mcp.tool()
async def get_weather_forecast(location: str, days: int = 1) -> List[Dict[str, Any]]:
    # Forecast is only available for 1 to 5 days.
    api_key = get_weather_api_key()
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {'q': location,'appid': api_key,'units': 'metric'}
    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get('cod') != '200':
        return {"error": data.get('message', 'Unknown error')}
    forecast_list = []
    daily_forecasts = {}
    for item in data['list']:
        date = item['dt_txt'].split(' ')[0]
        if date not in daily_forecasts:
            daily_forecasts[date] = []
        daily_forecasts[date].append(item)
    for i, date in enumerate(sorted(daily_forecasts.keys())):
        if i >= days:
            break
        day_data = daily_forecasts[date]
        temps = [item['main']['temp'] for item in day_data]
        descriptions = [item['weather'][0]['description'] for item in day_data]
        forecast_list.append({
            "date": date,
            "location": data['city']['name'],
            "min_temperature_celsius": min(temps),
            "max_temperature_celsius": max(temps),
            "description": descriptions[0]  
        })
    return forecast_list

if __name__ == "__main__":
    mcp.run(transport="stdio")