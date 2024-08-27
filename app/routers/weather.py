from fastapi import APIRouter, HTTPException
from app.services.weather import WeatherService


class WeatherRouter:
    def __init__(self):
        self.router = APIRouter()
        self._include_routes()

    def _include_routes(self):
        self.router.add_api_route("/insert-weekly-weather", self.insert_weekly_weather, methods=["POST"])

    async def insert_weekly_weather(self):
        try:
            weather_service = WeatherService()
            location = await weather_service.get_location_code()
            short_weathers = await weather_service.get_short_weather(location)
            return short_weathers
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


weather_router = WeatherRouter()
