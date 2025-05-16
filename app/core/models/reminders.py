import datetime
import sqlalchemy
from sqlalchemy import orm
from app.core.db_session import SqlAlchemyBase


class Reminder(SqlAlchemyBase):
    __tablename__ = 'reminders'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship("User", back_populates="reminders")
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String)
    dt = sqlalchemy.Column(sqlalchemy.DateTime,
                           default=datetime.datetime.now)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    notified = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
