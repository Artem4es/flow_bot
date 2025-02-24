import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from src.config.bot import settings
from src.config.logging import setup_logging
from src.db.redis import storage
from src.handlers import router as common_router

log = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    commands = [
        BotCommand(command="/start", description="🏄Погнали!"),
    ]
    await bot.set_my_commands(commands)


def main() -> None:
    setup_logging()
    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )
    dp = Dispatcher(storage=storage)
    dp.include_router(common_router)
    dp.startup.register(on_startup)
    dp.run_polling(bot)


if __name__ == "__main__":
    try:
        main()
        log.info("Bot app has been started...")

    except Exception as e:
        log.error(e, exc_info=True)

    finally:
        log.info("Bot app has been STOPPED.")
