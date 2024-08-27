from enum import Enum


class RegionEnum(Enum):
    SEOUL_GYEONGGI = "서울.인천.경기"
    JEJU = "제주도"
    CHUNGCHEONG_BUKDO = "충청북도"
    CHUNGCHEONG_NAMDO = "충청남도"
    GANGWON_YOUNGSEO = "강원영서"
    GANGWON_YOUNGDONG = "강원영동"
    JEOLLA_BUKDO = "전라북도"
    JEOLLA_NAMDO = "전라남도"
    GYEONGSANG_BUKDO = "경상북도"
    GYEONGSANG_NAMDO = "경상남도"

    @classmethod
    def has_value(cls, value):
        """Check if the enum contains the given value."""
        return any(value == item.value for item in cls)
