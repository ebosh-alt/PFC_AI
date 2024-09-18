import logging
from typing import Any, Sequence

from sqlalchemy import select, update, Row
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import selectinload, DeclarativeBase
from sqlalchemy.orm import sessionmaker

from data.config import DATABASE_URL


class BaseTable(AsyncAttrs, DeclarativeBase):
    pass


__factory: sessionmaker | None = None
logger = logging.getLogger(__name__)


async def create_async_database():
    global __factory
    engine = create_async_engine(DATABASE_URL)
    if __factory:
        return
    async with engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.create_all)
    await create_factory()
    await conn.close()
    await engine.dispose()


async def create_factory():
    global __factory
    engine = create_async_engine(DATABASE_URL)
    __factory = sessionmaker(bind=engine, expire_on_commit=True, class_=AsyncSession)
    await engine.dispose()


def get_factory():
    global __factory
    return __factory()


class BaseDB:
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    async def _get_session() -> AsyncSession:
        async with get_factory() as session:
            return session

    async def _add_obj(self, instance):
        async with await self._get_session() as session:
            session.add(instance)
            await session.flush()
            logger.info(f"add new {instance.__class__.__name__}: {instance.dict()}")
            await session.commit()
        await session.bind.dispose()

    async def _get_object(self, id: int | str):
        async with await self._get_session() as session:
            sql = select(self.obj).where(self.obj.id == id)
            for ref in self.obj.refs:
                sql = sql.options(selectinload(ref))
            result = await session.execute(sql)
            result = result.scalars().one_or_none()
        await session.bind.dispose()
        return result

    async def _get_objects(self, filters: dict | list = None):
        async with await self._get_session() as session:
            sql = select(self.obj)
            if filters is dict:
                for key in filters:
                    sql = sql.where(key == filters[key])
            elif filters is list:
                for flt in filters:
                    sql = sql.where(flt)
            for ref in self.obj.refs:
                sql = sql.options(selectinload(ref))
            result = await session.execute(sql)
            result = result.scalars().all()
        await session.bind.dispose()
        return result

    async def _update_obj(self, instance):
        async with await self._get_session() as session:
            query = update(self.obj).where(self.obj.id == instance.id).values(**instance.dict())
            await session.execute(query)
            logger.info(f"update data {instance.__class__.__name__}: {instance.dict()}")
            await session.commit()
        await session.bind.dispose()

    async def _delete_obj(self, instance):
        async with await self._get_session() as session:
            await session.delete(instance)
            logger.info(f"delete {instance.__class__.__name__}: {instance.dict()}")
            await session.commit()
        await session.bind.dispose()

    async def _get_attributes(self, attribute: str) -> Sequence[Row[tuple[Any, ...] | Any]]:
        # получение всех значений конкретного атрибута сущности
        async with await self._get_session() as session:
            sql = select(self.obj).column(attribute)
            result = await session.execute(sql)
            result = result.scalars().all()
        await session.bind.dispose()
        return result

    async def get_by_query(self, query):
        async with await self._get_session() as session:
            result = await session.execute(query)
            result = result.scalars().all()
        await session.bind.dispose()
        return result
