from abc import ABC
from datetime import datetime, timedelta
from typing import Dict


class WeatherAbstract(ABC):
    DATE_FORMATTER = "%Y%m%d"
    DATE_TIME_FORMATTER = "%Y%m%d%H"

    def format_date(self, date_time: datetime) -> int:
        return int(date_time.strftime(self.DATE_TIME_FORMATTER))

    def short_days_param(self) -> Dict[str, int]:
        today = datetime.now().date()

        yesterday_noon = datetime.combine(today - timedelta(days=1), datetime.min.time()).replace(hour=12)
        today_noon = datetime.combine(today, datetime.min.time()).replace(hour=12)

        short_date_params = {
            "today": self.format_date(yesterday_noon),
            "2DaysAfter": self.format_date(today_noon)
        }
        return short_date_params

    @staticmethod
    def short_query_params(reg_code: str, short_date_params: Dict[str, int]) -> Dict[str, str]:
        query_params = {
            "reg": reg_code,
            "tmfc1": str(short_date_params["today"]),
            "tmfc2": str(short_date_params["2DaysAfter"]),
            "help": "0"
        }
        return query_params

    def middle_days_param(self) -> Dict[str, int]:
        now = datetime.now().date()

        date_params = {
            "today": self.format_date(datetime.combine(now, datetime.min.time())),
            "tomorrow": self.format_date(datetime.combine(now + timedelta(days=1), datetime.min.time())),
            "sevenDaysAfter": self.format_date(datetime.combine(now + timedelta(days=6), datetime.min.time()))
        }
        return date_params

    @staticmethod
    def middle_query_params(reg_code: str, date_params: Dict[str, int]) -> Dict[str, str]:
        query_params = {
            "reg": reg_code,
            "tmef1": str(date_params["tomorrow"]),
            "tmef2": str(date_params["sevenDaysAfter"]),
            "help": "0"
        }
        return query_params
