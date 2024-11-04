from argparse import Namespace

from aiogram import Bot
from loguru import logger


class SendingService:
    def __init__(self, bot: Bot, arguments: Namespace, admin_id: str):
        self.bot = bot
        self.arguments = arguments
        self.admin_id = admin_id

    async def send_lessons_notification(self, deleted_lessons_count: int, deleted_tasks_count: int):
        msg = "<b>Сервис очистки базы данных</b>.\n\n" + \
              f"Удалено прошедших уроков {deleted_lessons_count}.\n" + \
              f"Удалено устаревших заданий {deleted_tasks_count}.\n\n" + \
              f"Время хранения прошедших уроков {self.arguments.lessons_ttl_days} дней.\n" + \
              f"Время хранения устаревших заданий {self.arguments.tasks_ttl_days} дней.\n"
        await self.bot.send_message(chat_id=self.admin_id, text=msg)
        logger.info(f"Successfully sent notification to user {self.admin_id}")
        await self.bot.session.close()
