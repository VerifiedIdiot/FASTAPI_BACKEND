import logging
import re
from typing import Union

import httpx

from app.config.settings import settings
from app.enums.region import RegionEnum
from app.models.weekly_weather import MiddleTemp, MiddleCondition, ErrorResponse
from app.services.weekly.weather_abstract import WeatherAbstract

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

    async def get_middle_condition(self) -> Union[dict[str, list[MiddleCondition]], ErrorResponse]:
        """ 중기 예보 날씨 상태 데이터를 가져오는 메서드 """
        logger.info("중기예보 날씨 상태 시작")

        try:
            middle_condition = {}

            async with httpx.AsyncClient() as client:
                middle_date_params = self.middle_days_param()  # 날짜 파라미터 계산 함수 호출

                # Query params 생성
                query_params = self.middle_query_params(reg_code=None, date_params=middle_date_params)
                query_params["authKey"] = self.api_key

                # API 요청
                response = await client.get(self.middle_condition, params=query_params)
                response.raise_for_status()  # 오류가 발생하면 예외 발생
                response_text = response.text

                # 응답에서 불필요한 데이터 필터링
                filtered_lines = response_text.splitlines()[2:-1]

                # RegionEnum을 순회하면서 데이터 분리
                for region in RegionEnum:
                    region_conditions = []

                    for i in range(0, len(filtered_lines), 2):  # 아침/저녁 데이터가 짝을 이룬다고 가정
                        pattern = re.compile(r'[^"\s]+|"(.*?)"')
                        morning_fields = [m.group(1) if m.group(1) else m.group(0) for m in pattern.finditer(filtered_lines[i])]
                        afternoon_fields = [m.group(1) if m.group(1) else m.group(0) for m in pattern.finditer(filtered_lines[i+1])]

                        # 날짜는 아침과 저녁에 동일하므로 하나만 사용
                        date = morning_fields[2]
                        morning_rain_percent = morning_fields[10]
                        morning_weather_condition = morning_fields[9]
                        afternoon_rain_percent = afternoon_fields[10]
                        afternoon_weather_condition = afternoon_fields[9]

                        # MiddleCondition 인스턴스를 생성
                        daily_condition = MiddleCondition(
                            date=date,
                            morning_rain_percent=morning_rain_percent,
                            morning_weather_condition=morning_weather_condition,
                            afternoon_rain_percent=afternoon_rain_percent,
                            afternoon_weather_condition=afternoon_weather_condition
                        )

                        region_conditions.append(daily_condition)

                    middle_condition[region.name] = region_conditions

            logger.info("중기예보 날씨 상태 성공")
            return middle_condition

        except httpx.RequestError as e:
            logger.error(f"중기예보 취합 실패: {e}")
            return ErrorResponse(error=f"중기예보 취합 실패: {str(e)}")
