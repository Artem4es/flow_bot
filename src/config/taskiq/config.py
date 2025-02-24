from taskiq_redis import RedisAsyncResultBackend, ListQueueBroker, RedisScheduleSource
from taskiq.schedule_sources import LabelScheduleSource
from taskiq import TaskiqScheduler

from src.config.bot import settings


redis_async_result = RedisAsyncResultBackend(
    redis_url=f"redis://{settings.redis.host}:{settings.redis.port}",
)


broker = ListQueueBroker(
    url=f"redis://{settings.redis.host}:{settings.redis.port}",
).with_result_backend(result_backend=redis_async_result)


redis_source = RedisScheduleSource(
    f"redis://{settings.redis.host}:{settings.redis.port}"
)

# And here's the scheduler that is used to query scheduled sources
scheduler = TaskiqScheduler(broker, sources=[LabelScheduleSource(broker)])
