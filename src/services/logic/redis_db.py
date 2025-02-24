import json
import logging

from src.db.redis import storage as redis_storage, redis
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import DefaultKeyBuilder, StorageKey


log = logging.getLogger(__name__)


class RedisDatesServ:
    def __init__(self, prefix: str):
        self.prefix = prefix
        # self.key = DefaultKeyBuilder().build(StorageKey(bot_id=bot_id,chat_id=chat_id,user_id=user_id)

    async def get_all_keys(self) -> list[str]:
        try:
            cursor = 0
            keys = []

            while True:
                cursor, batch = await redis.scan(
                    cursor=cursor, match=f"{self.prefix}*", count=100
                )
                keys.extend(batch)
                if cursor == 0:
                    break

            return keys

        except Exception as e:
            log.error("Ошибка получения записей из redis %r", e)
            raise

    async def get_data(self, redis_key: str) -> dict:
        try:
            return json.loads(await redis.get(redis_key))

        except Exception as e:
            log.error("Ошибка получения записи для %s,  %r", redis_key, e)
            raise

    async def update_book_data(self, redis_key: str, new_res: str) -> None:
        try:
            curr_data = await self.get_data(redis_key)
            curr_data["book_data"] = new_res
            await redis.set(redis_key, json.dumps(curr_data))

        except Exception as e:
            log.error("Ошибка обновления записи для %s,  %r", redis_key, e)
            raise
