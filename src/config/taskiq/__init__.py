"""Для работы функций-задач нужно импортировать их сюда"""

from src.config.taskiq.config import broker, scheduler
from src.tasks.book import booking_task

# manager = TaskiqManager()

__all__ = ("broker", "scheduler")
