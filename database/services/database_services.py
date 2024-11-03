from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.models.lesson import Lesson
from loguru import logger

from database.models.subject import Subject


class DbService:
    def __init__(self, db_dsn: str):
        self.db_dsn = db_dsn
        engine = create_async_engine(url=self.db_dsn)
        self.session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async def delete_expired_lessons(
            self,
            lessons_ttl_days: int
    ):
        current_dttm_msc = datetime.now(ZoneInfo('Europe/Moscow'))

        select_stmt = (
            select(Lesson)
            .where(Lesson.lesson_dttm < current_dttm_msc - timedelta(days=lessons_ttl_days))
            .join(Subject)
        )

        delete_stmt = (
            delete(Lesson)
            .where(Lesson.lesson_dttm < current_dttm_msc - timedelta(days=lessons_ttl_days))
        )

        async with self.session_maker() as session:
            select_result = await session.execute(select_stmt)
            lessons_to_delete = select_result.scalars().all()
            for l in lessons_to_delete:
                print(l.lesson_dttm)
            lessons_to_delete_count = len(lessons_to_delete)
            await session.execute(delete_stmt)
            logger.info(f"Succesfully deleted {lessons_to_delete_count} lessons from db")
            await session.commit()
            await session.close()
