from __future__ import annotations

import datetime

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy_serializer import SerializerMixin

from data.db_session import Base, create_session


class Player(Base, SerializerMixin):
    __tablename__ = 'Player'
    id: Mapped[int] = mapped_column(primary_key=True)
    coins: Mapped[int] = mapped_column(nullable=False, default=0)
    voice_activity: Mapped[datetime.timedelta] = mapped_column(nullable=False, default=datetime.timedelta())
    joined_vc: Mapped[datetime.datetime] = mapped_column(nullable=True)
    last_seen: Mapped[datetime.datetime] = mapped_column(nullable=True)

    def __init__(self, uid):
        self.id = uid

    def __eq__(self, other):
        return isinstance(other, Player) and other.id == self.id

    def __repr__(self):
        return f'<Player id={self.id} coins={self.coins}>'

    @classmethod
    async def get_player(cls, pid: int) -> Player:
        async with create_session() as session:
            async with session.begin():
                result = await session.execute(select(Player).where(Player.id == pid))
                player: Player = result.scalars().first()
        return player


    def get_voice_activity(self) -> str:
        """
        :return: `str` - String representation of voice activity in hours.
        """
        return f'{self.voice_activity.total_seconds() / 3600:.1f}'


class PrivateRoom(Base, SerializerMixin):
    __tablename__ = 'PrivateRoom'
    id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped[int] = mapped_column(nullable=False)

    def __init__(self, channel_id, owner):
        self.id = channel_id
        self.owner = owner

    def __repr__(self):
        return f'<PrivateRoom id={self.id} owner={self.owner}>'

    @classmethod
    async def get_room(cls, uid: int) -> PrivateRoom:
        async with create_session() as session:
            async with session.begin():
                room = await session.execute(select(PrivateRoom).where(PrivateRoom.owner == uid))
                room = room.scalars().one_or_none()
        return room
