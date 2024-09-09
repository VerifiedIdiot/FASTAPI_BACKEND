import logging
from datetime import datetime, timedelta
from typing import Union

import httpx

from app.config.settings import settings
from app.services.weekly.weather_abstract import WeatherAbstract
from app.models.weekly_weather import WeeklyWeatherData, ErrorResponse

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MiddleWeatherService(WeatherAbstract):

    def __init__(self):
        self.api_key = settings.WEEKLY_API_KEY
        self.api_location = settings.WEEKLY_LOCATION
        self.middle_temp = settings.WEEKLY_MIDDLE_TEMP
        self.middle_condition = settings.WEEKLY_MIDDLE_CONDITION

    async def get_middle_temp(self, location_code: dict[str, str]) -> Union[
        dict[str, list[WeeklyWeatherData]], ErrorResponse]:
        logger.info("중기온도 취합 시작")

        try:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')
            seven_days_later = (datetime.now() + timedelta(days=6)).strftime('%Y%m%d')

            middle_temp = {}

            async with httpx.AsyncClient() as client:
                middle_date_params = self.middle_days_param()
                print(middle_date_params)

                for city_name, reg_code in location_code.items():
                    query_params = self.middle_query_params(reg_code, middle_date_params)
                    query_params["authKey"] = self.api_key

                    response = await client.get(self.middle_temp, params=query_params)
                    response.raise_for_status()
                    response_text = response.text
                    print(response_text)

        except httpx.RequestError as e:
            logger.error(f"중기온도 취합 실패: {e}")
            return ErrorResponse(error=f"중기예보 취합 실패: {str(e)}")
