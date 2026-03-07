import uuid
from sqlalchemy import Column, String, Float, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from .load_db import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), unique=False, nullable=False)
    email = Column(String(255), nullable=False)
    role =  Column(String(255), nullable=False)


class Games(Base):
    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    appid = Column(String(255), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    developers = Column(String(255))
    publishers = Column(String(255))
    short_description = Column(Text)
    detailed_description = Column(Text)
    categories = Column(String(255))
    release_date = Column(String(255))
    is_free = Column(Boolean, default=False)
    genre = Column(String(255), nullable=False)


class UserGames(Base):
    __tablename__ = "user_games"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False)
    appid = Column(String(255), nullable=False)
    shelf = Column(String(50), default="Wish_List")
    rating = Column(Float, default=0.0)
    review = Column(Text)


class UserRecomendation(Base):
    __tablename__ = "user_recomendation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False)
    appid = Column(String(255), nullable=False)
    similarity = Column(Float)

class GameTags(Base):
    __tablename__ = "game_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appid = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)




