# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    WEEKLY_API_KEY: str = os.getenv("WEEKLY_API_KEY")

    WEEKLY_LOCATION: str = os.getenv("WEEKLY_LOCATION")
    WEEKLY_SHORT_TEMP: str = os.getenv("WEEKLY_SHORT_TEMP")
    WEEKLY_MIDDLE_TEMP: str = os.getenv("WEEKLY_MIDDLE_TEMP")
    WEEKLY_MIDDLE_CONDITION: str = os.getenv("WEEKLY_MIDDLE_CONDITION")

    DAILY_API_KEY: str = os.getenv("DAILY_API_KEY")

    DAILY_CURRENT_WEATHER: str = os.getenv("DAILY_CURRENT_WEATHER")
    DAILY_HOURLY_WEATHER: str = os.getenv("DAILY_HOURLY_WEATHER")


# 마치 context 처럼 settings의 내용이 어플리케이션 전역에서 명시하지않아도 사용이 가능함
settings = Settings()
