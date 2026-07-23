import os

from dotenv import load_dotenv

load_dotenv()


class ComScore:

    URL_BASE = "https://api.comscore.com/mediaratings/digital/v1/"

    TOKEN = os.getenv("COMSCORE_TOKEN")

    HEADER = {
        "Authorization": TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    @staticmethod
    def parameter(key, value):
        return {
            "KeyId": key,
            "Value": value,
        }

print("COMSCORE TOKEN:", ComScore.TOKEN)
print("COMSCORE HEADER:", ComScore.HEADER)


class DataSource:
    KEY = "dataSource"

    MULTI_PLATFORM = "25"
    DESKTOP_ONLY = "1"


class TargetType:
    KEY = "targetType"

    SIMPLE = "0"


class Target:
    KEY = "target"

    BRAZIL = "-1"
    NORTHEAST = "793"

    PERSONS_6_14 = "743"
    PERSONS_15_17 = "2201"
    PERSONS_18_24 = "2202"
    PERSONS_25_34 = "717"
    PERSONS_35_44 = "718"
    PERSONS_45_ = "721"

    ALL_MALES = "723"
    ALL_FEMALES = "733"


class GEO:
    KEY = "geo"

    BRAZIL = "76"


class TimeType:
    KEY = "timeType"

    MONTHS = "1"


class TimePeriod:
    KEY = "timePeriod"


class MediaSetType:
    KEY = "mediaSetType"

    SAVED_MEDIA_LISTS = "0"


class MediaSet:
    KEY = "mediaSet"

    RANKING_PORTAIS = "488607"


class Measure:
    KEY = "measure"

    TOTAL_UNIQUE_VISITORS_VIEWERS_TOTAL_POPULATION = "276"
    REACH_TOTAL_POPULATION = "277"
    TOTAL_VIEWS_TOTAL_POPULATION = "280"
    TOTAL_VISITS_TOTAL_POPULATION = "281"
    PAGE_VIEWS_TOTAL_POPULATION = "570"
    TOTAL_MINUTES_TOTAL_POPULATION = "284"
    AVERAGE_MINUTES_PER_VISITOR_TOTAL_POPULATION = "287"

    TOTAL_DIGITAL_POPULATION_IXI = "306"
    TOTAL_DIGITAL_POPULATION_IXII = "307"
    TOTAL_DIGITAL_POPULATION_IXIII = "310"
    TOTAL_DIGITAL_POPULATION_IXIIII = "315"
    TOTAL_DIGITAL_POPULATION_IXIIIII = "659"
    TOTAL_DIGITAL_POPULATION_IXIIIIII = "660"

    COMPOSITION_UV = "278"

    SHARED_AUDIENCE = "401"
    VERTICAL = "402"
    HORIZONTAL = "403"
    INDEX = "404"


class MediaRowType:
    KEY = "mediaRowType"

    PASSING_OR_MEDIAROW = "1"