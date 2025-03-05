from sqlalchemy import Column, Integer, String, Boolean, Text, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    user_tg_id = Column(BigInteger, unique=True)
    username = Column(String)
    name = Column(String, unique=True)
    description = Column(String)
    description_keywords = Column(String)


class Query(Base):
    __tablename__ = "Queries"
    id = Column(Integer, primary_key=True, index=True)
    