from collections import defaultdict
from pprint import pprint
from typing import Any, Self

from pydantic import BaseModel, Field, RootModel, model_validator
import requests

from constants import (
    PEOPLE_AMOUNT,
    SCHEDULE_URL_TEMPLATE,
    DATE_FROM,
    DATE_TO,
    TARGET_GROUP,
)


def parse_resp(resp_json: dict):  # ->:
    found_dates = defaultdict(list)
    for hour, date_dict in resp_json.items():
        for date, data in date_dict.items():
            if data["enable"] != "active":
                continue

            if TARGET_GROUP in data["short_description"]:
                if data["max_count_people"] >= PEOPLE_AMOUNT:
                    found_dates[date].append(
                        {hour: f"Осталось {data['max_count_people']} места"}
                    )

    return found_dates


def main() -> None:
    url = SCHEDULE_URL_TEMPLATE.format(date_start=DATE_FROM, date_end=DATE_TO)
    resp = requests.get(url, headers=AUTH_HEADERS)
    parsed_res = parse_resp(resp.json())
    pprint(parsed_res)


if __name__ == "__main__":
    main()
