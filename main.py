import asyncio

from configuration.arguments import get_arguments
from configuration.configuration import load_config, Configuration
from database.services.database_services import DbService
from loguru import logger


async def main():
    config: Configuration = load_config()
    arguments = get_arguments()
    db_service = DbService(config.db.dsn)
    logger.info(
        f"Cleaner service started. Lessons ttl: {arguments.lessons_ttl_days} days, "
        f"Tasks ttl: {arguments.tasks_ttl_days} days"
    )
    await db_service.delete_expired_lessons(arguments.lessons_ttl_days)
    await db_service.delete_expired_tasks(arguments.tasks_ttl_days)


if __name__ == "__main__":
    asyncio.run(main())
