from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from service.database.models.homework import Homework
from service.database.models.lesson import Lesson
from loguru import logger

from service.database.models.subject import Subject


class DbService:
    def __init__(self, db_dsn: str):
        self.db_dsn = db_dsn
        engine = create_async_engine(url=self.db_dsn)
        self.session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async def delete_expired_lessons(self, lessons_ttl_days: int) -> int:
        """
        Метод удаляет из базы данных прошедшие уроки
        :param lessons_ttl_days: Время жизни урока после того, как он прошел
        """
        current_dttm_msc = datetime.now(ZoneInfo("Europe/Moscow"))

        select_stmt = (
            select(Lesson)
            .where(
                Lesson.lesson_dttm < current_dttm_msc - timedelta(days=lessons_ttl_days)
            )
            .join(Subject)
        )

        delete_stmt = delete(Lesson).where(
            Lesson.lesson_dttm < current_dttm_msc - timedelta(days=lessons_ttl_days)
        )

        async with self.session_maker() as session:
            select_result = await session.execute(select_stmt)
            lessons_to_delete = select_result.scalars().all()
            lessons_to_delete_count = len(lessons_to_delete)
            await session.execute(delete_stmt)
            logger.info(
                f"Succesfully deleted {lessons_to_delete_count} lessons from db"
            )
            await session.commit()
            await session.close()
        return lessons_to_delete_count

    async def delete_expired_tasks(self, task_ttl_days: int) -> int:
        """
        Метод удаляет из базы данных неактуальные домашние задания
        :param task_ttl_days: Время жизни домашнего задания после того, как оно было создано
        """
        current_dttm_msc = datetime.now(ZoneInfo("Europe/Moscow"))

        select_stmt = select(Homework).where(
            Homework.created_at < current_dttm_msc - timedelta(days=task_ttl_days)
        )

        delete_stmt = delete(Homework).where(
            Homework.created_at < current_dttm_msc - timedelta(days=task_ttl_days)
        )

        async with self.session_maker() as session:
            select_result = await session.execute(select_stmt)
            homework_to_delete = select_result.scalars().all()
            homework_to_delete_count = len(homework_to_delete)
            await session.execute(delete_stmt)
            logger.info(f"Succesfully deleted {homework_to_delete_count} tasks from db")
            await session.commit()
            await session.close()
        return homework_to_delete_count
