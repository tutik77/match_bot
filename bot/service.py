import os
from openai import AsyncOpenAI
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import case

from database import get_session
from settings import settings
from tables import User, UserQuery


os.environ['OPENAI_API_KEY'] = settings.openai_api_key
openai_api_key = settings.openai_api_key

class GPTService:
    def __init__(self):
        self.client = AsyncOpenAI()

    async def initialize_assistant(self):
        self.assistant = await self.client.beta.assistants.create(
            name="Помощник для выделения ключевый слов из текста.",
            instructions = "Из получаемого текста ты должен выделять ключевые слова, по которым можно будет искать профили в базе данных.",
            model="gpt-4o",
        )

        self.thread = await self.client.beta.threads.create()

    async def get_keywords_from_description(self, description):
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{'role':'user', 'content': f"Из описания профиля пользователя: '{description}', выдели ключевые слова, фразы, обобщения интересов, параметры внешности, черты характера. Форматировать не нужно, просто перечисляй все ключевые слова, которые в наибольшей степени описывают челоевека."}],
        )
        keywords = response.choices[0].message.content
        return keywords  

    async def get_keywords_from_query(self, query):
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{'role':'user', 'content': f"Из полученного запроса: '{query}' помоги выделить ключевые слова для поиска профилей пользователей по интересам, занятиям, параметрам внешности. Нужно получить наиболее релевантные слова, их синонимы, различные формулировки, которые люди могут использовать для описания себя, чтобы потом по этим словам искать профили в базе данных. В ответе укажи ТОЛЬКО сами слова, перечисленные через запятую."}])
        keywords_list = response.choices[0].message.content.split(", ")
        return keywords_list

    async def compare_query_with_description(self, query: str, description: str):
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{'role':'user', 'content': f"По запросу {query} был получен профиль с описанием: {description}. Сопоставь их и кратко (до 70 слов) расскажи ищущему, чем подходит ему найденный профиль."}])
        comparison = response.choices[0].message.content
        return comparison

gpt_service = GPTService()

class RegisterService:
    @staticmethod
    async def get_user_by_tg_id(user_tg_id: int, session: AsyncSession):
        result = await session.execute(select(User).where(User.user_tg_id == user_tg_id))
        return result.scalars().first()

    @staticmethod
    async def create_user(user_data: dict, session: AsyncSession):
        user_data["description_keywords"] = await gpt_service.get_keywords_from_description(user_data["description"])
        new_user = User(
            user_tg_id=user_data["user_tg_id"],
            username=user_data["username"],
            name=user_data["name"],
            description=user_data["description"],
            description_keywords=user_data["description_keywords"]
        )

        session.add(new_user)
        await session.commit()
        return new_user


class SearchService:
    @staticmethod
    async def search_users_by_keywords(keywords: list):
        async for session in get_session():
            match_count = func.sum(
                case(
                    *[(User.description_keywords.ilike(f'%{kw}%'), 1) for kw in keywords],
                    else_=0
                )
            ).label("match_count")

            query = (
                select(User, match_count)
                .filter(or_(*[User.description_keywords.ilike(f'%{kw}%') for kw in keywords]))
                .group_by(User.user_tg_id)
                .order_by(match_count.desc())
                .limit(7)
            )

            result = await session.execute(query)
            users = result.scalars().all()

        return users

    @staticmethod
    async def add_query_to_db(query: str, user_tg_id: int):
        async for session in get_session():
            user_query = UserQuery(query_text=query, user_tg_id=user_tg_id)
            session.add(user_query)
            await session.commit()