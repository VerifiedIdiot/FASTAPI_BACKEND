from app.enums.city import CityEnum
from app.enums.region import RegionEnum

def location_mapper() -> dict[RegionEnum, list[CityEnum]]:

    region_to_cities = {
        RegionEnum.SEOUL_GYEONGGI: [CityEnum.SEOUL.value, CityEnum.SUWON.value, CityEnum.INCHEON.value],
        RegionEnum.GANGWON_YOUNGSEO: [CityEnum.CHUNCHEON.value],
        RegionEnum.GANGWON_YOUNGDONG: [CityEnum.GANGNEUNG.value],
        RegionEnum.CHUNGCHEONG_BUKDO: [CityEnum.CHUNGJU.value],
        RegionEnum.CHUNGCHEONG_NAMDO: [CityEnum.DAEJEON.value],
        RegionEnum.GYEONGSANG_BUKDO: [CityEnum.ANDONG.value, CityEnum.DAEGU.value],
        RegionEnum.GYEONGSANG_NAMDO: [CityEnum.BUSAN.value, CityEnum.ULSAN.value],
        RegionEnum.JEOLLA_BUKDO: [CityEnum.JEONJU.value],
        RegionEnum.JEOLLA_NAMDO: [CityEnum.GWANGJU.value, CityEnum.YEOSU.value, CityEnum.MOKPO.value],
        RegionEnum.JEJU: [CityEnum.JEJU.value],
    }
    return region_to_cities