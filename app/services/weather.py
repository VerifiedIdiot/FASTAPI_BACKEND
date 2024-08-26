import httpx
import logging
from typing import Dict

from app.enums.city import CityEnum

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(self):
        self.api_url = "https://api.example.com/weather"  # 외부 API URL
        self.api_key = "your_api_key"  # API 키 또는 필요한 인증 정보

    async def get_location_code(self) -> Dict[str, str]:
        logger.info("지역코드 가져오기 시작")
        try:
            async with httpx.AsyncClient() as client:
                # 비동기 GET 요청
                response = await client.get(self.api_url, headers={"authKey": {self.api_key}})
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

