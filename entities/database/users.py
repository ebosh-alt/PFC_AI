import logging

from sqlalchemy import Column, BigInteger, Integer, DateTime, String

from .base import BaseTable, BaseDB

logger = logging.getLogger(__name__)


class User(BaseTable):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    available_request = Column(Integer, default=None)
    expired_date_subscription = Column(DateTime, default=None)
    vector_store_id = Column(String, default=None)
    thread_id = Column(String, default=None)

    refs = []

    def dict(self):
        return {"id": self.id,
                "available_request": self.available_request,
                "expired_date_subscription": self.expired_date_subscription,
                "vector_store_id": self.vector_store_id,
                "thread_id": self.thread_id,
                }


class Users(BaseDB):
    def __init__(self):
        super().__init__(User)

    async def new(self, user: User):
        await self._add_obj(user)

    async def get(self, id: int) -> User | None:
        result = await self._get_object(id)
        return result

    async def update(self, user: User) -> None:
        await self._update_obj(instance=user)

    async def delete(self, user: User) -> None:
        await self._delete_obj(instance=user)

    async def in_(self, id: int) -> User | bool:
        result = await self.get(id)
        if type(result) is User:
            return result
        return False
