import datetime
import sqlalchemy
from sqlalchemy import orm
from app.core.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    extra_data = sqlalchemy.Column(sqlalchemy.String)
    reminders = orm.relationship("Reminder", back_populates="user")

