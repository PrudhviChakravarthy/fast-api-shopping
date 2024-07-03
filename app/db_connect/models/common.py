from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __table_args__ = {"schema": None}
    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    pass