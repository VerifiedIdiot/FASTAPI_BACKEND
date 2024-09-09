# app/models/weekly_weather.py
from pydantic import BaseModel


class WeeklyWeatherData(BaseModel):
    date: str
    morning_temperature: str
    morning_rain_percent: str
    morning_weather_condition: str
    afternoon_temperature: str
    afternoon_rain_percent: str
    afternoon_weather_condition: str


class ErrorResponse(BaseModel):
    error: str
