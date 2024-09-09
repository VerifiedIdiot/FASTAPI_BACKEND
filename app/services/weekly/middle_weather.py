import logging
from datetime import datetime, timedelta
from typing import Union
from app.enums.region import RegionEnum

import httpx

from app.config.settings import settings
from app.services.weekly.weather_abstract import WeatherAbstract
from app.models.weekly_weather import MiddleTemp, MiddleCondition, ErrorResponse

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MiddleWeatherService(WeatherAbstract):

    def __init__(self):
        self.api_key = settings.WEEKLY_API_KEY
        self.api_location = settings.WEEKLY_LOCATION
        self.middle_temp = settings.WEEKLY_MIDDLE_TEMP
        self.middle_condition = settings.WEEKLY_MIDDLE_CONDITION

    async def get_middle_temp(self, location_code: dict[str, str]) -> Union[dict[str, list[MiddleTemp]], ErrorResponse]:
        logger.info("중기온도 취합 시작")

        try:
            middle_temp = {}

            async with httpx.AsyncClient() as client:
                middle_date_params = self.middle_days_param()  # assuming this method is defined in the class

                for city_name, reg_code in location_code.items():
                    query_params = self.middle_query_params(reg_code, middle_date_params)  # assuming this method is defined
                    query_params["authKey"] = self.api_key

                    response = await client.get(self.middle_temp, params=query_params)
                    response.raise_for_status()  # raise an exception for bad responses
                    response_text = response.text

                    # 필터링된 라인 추출 (불필요한 데이터 제외)
                    filtered_lines = [
                        line for line in response_text.splitlines()
                        if "#" not in line and "-99" not in line
                    ]

                    city_weather_data = []
                    for line in filtered_lines:
                        fields = self.parse_line(line)
                        print(fields)
                        if not fields:
                            continue

                        date_str = fields[2][:8]
                        min_temp = fields[6]
                        max_temp = fields[7]

                        # Pydantic 모델로 변환
                        weather_data = MiddleTemp(
                            date=date_str,
                            morning_temperature=min_temp,
                            afternoon_temperature=max_temp,
                        )
                        city_weather_data.append(weather_data)

                    middle_temp[city_name] = city_weather_data

            logger.info("중기온도 취합 성공")
            return middle_temp

        except httpx.RequestError as e:
            logger.error(f"중기온도 취합 실패: {e}")
            return ErrorResponse(error=f"중기예보 취합 실패: {str(e)}")

        # async def get_middle_condition(self, location_code: dict[str, str]) -> Union[
        #     dict[str, list[MiddleCondition]], ErrorResponse]:
        #     logger.info("중기온도 취합 시작")
        #
        #     try:
        #         middle_temp = {}
        #
        #         async with httpx.AsyncClient() as client:
        #             middle_date_params = self.middle_days_param()  # assuming this method is defined in the class
        #
        #             for city_name, reg_code in location_code.items():
        #                 query_params = self.middle_query_params(reg_code,
        #                                                         middle_date_params)  # assuming this method is defined
        #                 query_params["authKey"] = self.api_key
        #
        #                 response = await client.get(self.middle_temp, params=query_params)
        #                 response.raise_for_status()  # raise an exception for bad responses
        #                 response_text = response.text
        #
        #                 # 필터링된 라인 추출 (불필요한 데이터 제외)
        #                 filtered_lines = [
        #                     line for line in response_text.splitlines()
        #                     if "#" not in line and "-99" not in line
        #                 ]
        #
        #                 city_weather_data = []
        #                 for line in filtered_lines:
        #                     fields = self.parse_line(line)
        #                     print(fields)
        #                     if not fields:
        #                         continue
        #
        #                     date_str = fields[2][:8]
        #                     min_temp = fields[6]
        #                     max_temp = fields[7]
        #
        #                     # Pydantic 모델로 변환
        #                     weather_data = MiddleTemp(
        #                         date=date_str,
        #                         morning_temperature=min_temp,
        #                         afternoon_temperature=max_temp,
        #                     )
        #                     city_weather_data.append(weather_data)
        #
        #                 middle_temp[city_name] = city_weather_data
        #
        #         logger.info("중기온도 취합 성공")
        #         return middle_temp
        #
        #     except httpx.RequestError as e:
        #         logger.error(f"중기온도 취합 실패: {e}")
        #         return ErrorResponse(error=f"중기예보 취합 실패: {str(e)}")
