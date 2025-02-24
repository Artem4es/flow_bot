from aiogram.fsm.storage.redis import DefaultKeyBuilder, Redis, RedisStorage

from src.config.bot import settings

redis = Redis(
    host=settings.redis.host, port=int(settings.redis.port), decode_responses=True
)
storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_bot_id=True))
