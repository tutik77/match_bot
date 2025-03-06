from sqlalchemy import Column, Integer, String, Boolean, Text, BigInteger, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    user_tg_id = Column(BigInteger, primary_key=True, unique=True)
    username = Column(String)
    name = Column(String, unique=True)
    description = Column(String)
    description_keywords = Column(String)

class UserQuery(Base):
    __tablename__ = "UserQueries"
    id = Column(Integer, primary_key=True, index=True)
    user_tg_id = Column(BigInteger, nullable=False)
    query_text = Column(String, nullable=False)