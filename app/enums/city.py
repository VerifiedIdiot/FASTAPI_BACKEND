from enum import Enum


class CityEnum(Enum):
    # SEOUL_GYEONGGI
    SEOUL = "서울"
    SUWON = "수원"
    INCHEON = "인천"
    # GANGWON_YOUNGSEO
    CHUNCHEON = "춘천"
    # GANGWON_YOUNGDONG
    GANGNEUNG = "강릉"
    # CHUNGCHEONG_BUKDO
    CHUNGJU = "청주"
    # CHUNGCHEONG_NAMDO
    DAEJEON = "대전"
    # GYEONGSANG_BUKDO
    ANDONG = "안동"
    DAEGU = "대구"
    # GYEONGSANG_NAMDO
    BUSAN = "부산"
    ULSAN = "울산"
    # JEOLLA_BUKDO
    JEONJU = "전주"
    # JEOLLA_NAMDO
    GWANGJU = "광주"
    YEOSU = "여수"
    MOKPO = "목포"
    # JEJU
    JEJU = "제주"

    @classmethod
    def has_value(cls, value):
        """Check if the enum contains the given value."""
        return any(value == item.value for item in cls)
