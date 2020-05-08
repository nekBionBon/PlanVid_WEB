import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Movie(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'movies'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    id_author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='-')
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    year = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='-')
    duration = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='-')
    watched = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    timecode = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    review = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=' ')

    user = orm.relation('User')
