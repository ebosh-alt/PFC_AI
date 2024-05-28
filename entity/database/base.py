import logging
from typing import Any, Sequence

from sqlalchemy import select, update, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from data.config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()

__factory: sessionmaker | None = None

logger = logging.getLogger(__name__)


async def create_async_database():
    global __factory
    engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
    if __factory:
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await create_factory()
    await conn.close()


async def create_factory():
    global __factory
    engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
    __factory = sessionmaker(bind=engine, expire_on_commit=True, class_=AsyncSession)


def get_factory():
    global __factory
    return __factory()


class BaseDB:
    @staticmethod  # __table__ = "accounts"
    async def _get_session() -> AsyncSession:
        async with get_factory() as session:
            return session

    async def _add_obj(self, instance):
        async with await self._get_session() as session:
            session.add(instance)
            logger.info(f"add new {instance.__class__.__name__}: {instance.dict()}")
            await session.commit()

    async def _get_object(self, obj, id):
        async with await self._get_session() as session:
            res = await session.get(obj, id)
            return res

    async def _get_objects(self, obj, filters: dict = None):
        async with await self._get_session() as session:
            sql = select(obj)
            if filters is not None:
                for key in filters:
                    sql = sql.where(key == filters[key])
            result = await session.execute(sql)
            return result.scalars().all()

    async def _update_obj(self, obj, instance):
        async with await self._get_session() as session:
            query = update(obj).where(obj.id == instance.id).values(**instance.dict())
            await session.execute(query)
            logger.info(f"update data {instance.__class__.__name__}: {instance.dict()}")
            await session.commit()

    async def _delete_obj(self, instance):
        async with await self._get_session() as session:
            await session.delete(instance)
            logger.info(f"delete {instance.__class__.__name__}: {instance.dict()}")
            await session.commit()

    async def _get_attributes(self, obj, attribute: str) -> Sequence[Row[tuple[Any, ...] | Any]]:
        # получение всех значений конкретного атрибута сущности
        async with await self._get_session() as session:
            sql = select(obj).column(attribute)
            result = await session.execute(sql)
            return result.all()
