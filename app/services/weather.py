import re
from datetime import datetime, timedelta
import httpx
import logging
from typing import Dict, List
from app.enums.city import CityEnum
from app.config.settings import settings
from app.services.weather_abstract import WeatherAbstract

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherService(WeatherAbstract):
    def __init__(self):
        self.api_key = settings.WEEKLY_API_KEY  # API 키 또는 필요한 인증 정보
        self.api_location = settings.WEEKLY_LOCATION  # 외부 API URL
        self.api_short = settings.WEEKLY_SHORT_TEMP  # 외부 API 중 오늘 ~ 3일까지의 날씨&온도정보

    async def get_location_code(self) -> Dict[str, str]:
        logger.info("지역코드 가져오기 시작")
        try:
            async with httpx.AsyncClient() as client:
                # 비동기 GET 요청
                response = await client.get(self.api_location, params={"authKey": self.api_key})
                response.raise_for_status()  # HTTP 오류 발생 시 예외를 발생시킵니다.

                # 응답 데이터 처리
                response_text = response.text
                location_code = {}
                lines = response_text.splitlines()
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 5:
                        reg_id = parts[0]
                        reg_name = parts[4]
                        # CityEnum에 해당하는 이름만 매핑
                        if CityEnum.has_value(reg_name):
                            location_code[reg_name] = reg_id

                logger.info("지역코드 가져오기 성공")
                return location_code
        except httpx.RequestError as e:
            logger.error(f"API 요청 오류: {e}")
            return {}

    async def get_short_weather(self, location_code: Dict[str, str]) -> Dict[str, List[List[str]]]:
        logger.info("단기예보 취합 시작")
        try:
            today = datetime.now().strftime('%Y%m%d')
            two_days_later = (datetime.now() + timedelta(days=2)).strftime('%Y%m%d')

            complete_short = {}

            async with httpx.AsyncClient() as client:
                short_date_params = self.short_days_param()
                print(short_date_params)
                for city_name, reg_code in location_code.items():
                    query_params = self.short_query_params(reg_code, short_date_params)
                    query_params["authKey"] = self.api_key
                    print(query_params)
                    response = await client.get(self.api_short, params=query_params)
                    response.raise_for_status()
                    response_text = response.text

                    filtered_lines = [
                        line for line in response_text.splitlines()
                        if "#" not in line and "-99" not in line
                    ]

                    morning_data = {}
                    afternoon_data = {}

                    for line in filtered_lines:
                        fields = self.parse_line(line)
                        if not fields:
                            continue

                        date_str = fields[2][:8]
                        if today <= date_str <= two_days_later:
                            if fields[2].endswith("0000"):
                                morning_data[date_str] = [fields[12], fields[13], fields[16]]
                            elif fields[2].endswith("1200"):
                                afternoon_data[date_str] = [fields[12], fields[13], fields[16]]

                    city_weather = []
                    for date in morning_data.keys():
                        combined_weather = [date] + morning_data[date] + afternoon_data.get(date, ["", "", ""])
                        city_weather.append(combined_weather)

                    complete_short[city_name] = city_weather

            logger.info("단기예보 취합 성공")
            return complete_short
        except httpx.RequestError as e:
            logger.error(f"단기예보 취합 실패: {e}")
            return {}

    @staticmethod
    def parse_line(line: str) -> List[str]:
        try:
            data_fields = []
            matcher = re.finditer(r'[^"\s]+|"([^"]*)"', line)
            for match in matcher:
                data_fields.append(match.group(1) if match.group(1) else match.group(0))
            return data_fields
        except Exception as e:
            logger.warn(f"라인 파싱 실패: {e}")
            return []
