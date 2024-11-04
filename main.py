import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from configuration.arguments import get_arguments
from configuration.configuration import load_config, Configuration
from service.database.database_services import DbService
from loguru import logger

from service.sending_service import SendingService


async def main():
    config: Configuration = load_config()
    arguments = get_arguments()
    db_service = DbService(config.db.dsn)
    bot = Bot(
        token=config.telegram.token, default=DefaultBotProperties(parse_mode="HTML")
    )
    sending_service = SendingService(bot, config.telegram.admin_id)
    logger.info(
        f"Cleaner service started. Lessons ttl: {arguments.lessons_ttl_days} days, "
        f"Tasks ttl: {arguments.tasks_ttl_days} days"
    )
    deleted_lessons_cnt = await db_service.delete_expired_lessons(arguments.lessons_ttl_days)
    deleted_tasks_cnt = await db_service.delete_expired_tasks(arguments.tasks_ttl_days)
    await sending_service.send_lessons_notification(deleted_lessons_cnt, deleted_tasks_cnt)


if __name__ == "__main__":
    asyncio.run(main())
