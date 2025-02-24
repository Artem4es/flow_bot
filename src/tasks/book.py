import asyncio
import logging
from collections import defaultdict
from datetime import datetime
from typing import Final

import httpx
from aiogram import Bot


from src.config.bot import settings
from src.config.taskiq import broker
from src.constants import SCHEDULE_URL_TEMPLATE, PEOPLE_AMOUNT, TARGET_GROUP
from src.services.logic.redis_db import RedisDatesServ

log = logging.getLogger(__name__)


class BookingChecker:
    url_template: Final[str] = SCHEDULE_URL_TEMPLATE

    def __init__(
        self, token: str, db_serv: RedisDatesServ, persons: int, target_group: str
    ):
        self.db_serv = db_serv
        self.headers = self._get_headers(token)
        self.bot = self._get_bot()
        self.persons = persons
        self.target_group = target_group

    async def start_scanning(self) -> None:
        records = await self.db_serv.get_all_keys()
        for key in records:
            user_data = await self.db_serv.get_data(key)
            await self._process_data(key, user_data)

    async def _process_data(self, redis_key: str, user_data: dict) -> None:
        dates = list(user_data.values())[0]
        new_res = await self._process_dates(dates)
        message = self._format_message(new_res)
        if await self._resp_changed(message, user_data):
            await self.db_serv.update_book_data(redis_key, message)
            user_id: int = int(redis_key.split(":")[-2])
            log.info("Отправляю сообщение: %s пользователю ", message, user_id)
            await self.bot.send_message(text=message, chat_id=user_id)

    @staticmethod
    def _format_message(new_res: dict) -> str:
        mes = "Хей, я тут нашёл кое-что для тебя:\n"
        for date, times in new_res.items():
            times = "\n".join(
                [[f"На {k} {v}" for k, v in time.items()][0] for time in times]
            )
            mes += f"{date} есть такие варианты:\n{times}\n\n"

        return mes

    @staticmethod
    async def _resp_changed(new_res: str, user_data: dict) -> bool:
        prev_result = user_data.get("book_data")
        return new_res != prev_result

    async def _process_dates(self, dates: list[str]) -> dict:
        res = dict()
        for date in dates:
            date_formatted = self._format_date(date)
            url = self.url_template.format(
                date_start=date_formatted, date_end=date_formatted
            )
            response = await self._make_req(url)
            parsed_res = self._parse_resp(response)
            res.update(parsed_res)

        return res

    @staticmethod
    def _format_date(date: str) -> str:
        try:
            date_python = datetime.strptime(date, "%d/%m/%Y")
            return datetime.strftime(date_python, "%Y-%m-%d")

        except Exception as e:
            log.error("Ошибка приведения дат: %r", e)
            raise

    async def _make_req(self, url: str) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(url, headers=self.headers)
                res.raise_for_status()
                return res.json()

        except Exception as e:
            log.error("Ошибка отправки запроса %r", e)

    def _parse_resp(self, resp_json: dict) -> defaultdict:
        found_dates = defaultdict(list)
        for hour, date_dict in resp_json.items():
            for date, data in date_dict.items():
                if data["enable"] != "active":
                    continue

                if self.target_group in data["short_description"]:
                    if data["max_count_people"] >= PEOPLE_AMOUNT:
                        found_dates[date].append(
                            {hour: f"Осталось {data['max_count_people']} места"}
                        )

        return found_dates

    @staticmethod
    def _get_bot() -> Bot:
        return Bot(
            token=settings.bot.token,
        )

    @staticmethod
    def _get_headers(token: str) -> dict:
        return {"X-Authorization": f"Bearer {token}"}


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def booking_task() -> None:
    checker = BookingChecker(
        token=settings.user.token,
        db_serv=RedisDatesServ(prefix="fsm"),
        persons=PEOPLE_AMOUNT,
        target_group=TARGET_GROUP,
    )
    await checker.start_scanning()


if __name__ == "__main__":
    asyncio.run(booking_task())
