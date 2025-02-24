from datetime import datetime
from typing import Final

FLOW_MAIN_URL: Final[str] = "https://moscowflow.ru"
BOOKING_URL: Final[str] = "https://moscowflow.ru/volna/booking"
SCHEDULE_URL: Final[str] = (
    "https://crm.moscowflow.ru/api/tariff/registration_wave?date_start=2025-02-22&date_end=2025-02-28&count_people=1&user_type=prodvinutyj"
)
PEOPLE_AMOUNT: Final[int] = 1
SCHEDULE_URL_TEMPLATE: Final[str] = (
    "https://crm.moscowflow.ru/api/tariff/registration_wave?date_start={date_start}&date_end={date_end}&count_people=1&user_type=prodvinutyj"
)
DATE_FROM: Final[str] = datetime.strftime(
    datetime(year=2025, month=2, day=23), "%Y-%m-%d"
)
DATE_TO: Final[str] = datetime.strftime(
    datetime(year=2025, month=2, day=23), "%Y-%m-%d"
)
LEVEL: Final[str] = "prodvinutyj"
TARGET_GROUP: Final[str] = "Для тех, кто не в первый раз и уверенно стартует с борта"

BOT_STATE_PREFIX: Final[str] = "flow"
