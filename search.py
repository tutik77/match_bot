from aiogram import F, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from service import SearchService, gpt_service

router = Router()
search_service = SearchService()

class SearchStates(StatesGroup):
    waiting_for_query = State()
    
@router.message(Command("search"))
async def search(message: types.Message, state: FSMContext):
    await message.answer("Введи запрос для поиска профиля!")
    await state.set_state(SearchStates.waiting_for_query)
    

@router.message(SearchStates.waiting_for_query)
async def search2(message: types.Message):
    query = message.text
    await search_service.add_query_to_db(query, message.from_user.id)
    print("Query added to db!") # DEBUG

    keywords = await gpt_service.get_keywords_from_query(query)
    users = await search_service.search_users_by_keywords(keywords)
 
    if not users:
        await message.answer("По запросу не найдено профилей.")
        return
    
    await message.answer("По запросу найдены профили:")
    for user in users:
        comparison = await gpt_service.compare_query_with_description(query, user.description)
        contact = f"@{user.username}" if user.username else f"ID: {user.user_tg_id}"
        
        message_text = (
            f"Имя пользователя: {user.name}\n"
            f"Описание: {comparison}\n"
            f"Контакт: {contact}"
        )
        
        await message.answer(message_text)