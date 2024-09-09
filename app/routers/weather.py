import logging

from fastapi import APIRouter, HTTPException

from app.services.weekly.short_weather import ShortWeatherService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherRouter:
    def __init__(self):
        self.router = APIRouter()
        self._include_routes()

    def _include_routes(self):
        self.router.add_api_route("/insert-weekly-weather", self.insert_weekly_weather, methods=["POST"])

    async def insert_weekly_weather(self):
        try:
            short_weather_service = ShortWeatherService()

            # location을 먼저 호출하고 값이 유효한지 확인
            location = await short_weather_service.get_location_code()

            if not location:  # location이 없으면 예외 처리
                raise HTTPException(status_code=404, detail="지역 코드를 불러올 수 없습니다.")

            # short weather 조회
            short_weathers = await short_weather_service.get_short_weather(location)

            # middle weather 조회 (주석을 해제하고 사용할 수 있음)
            # middle_weather_service = MiddleWeatherService()
            # await middle_weather_service.middle_temp(location)

            return short_weathers

        except Exception as e:
            logger.error(f"주간 날씨 데이터를 삽입하는 중 오류 발생: {str(e)}")
            raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


weather_router = WeatherRouter()
