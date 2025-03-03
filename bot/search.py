from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot import dp
from service import SearchService

search_service = SearchService()

class SearchStates(StatesGroup):
    waiting_for_querry = State()
    
@dp.message(Command("search"))
async def search(message: types.Message, state: FSMContext):
    message.answer("Введи запрос для поиска профиля!")
    await state.set_state(SearchStates.waiting_for_query)
    
@dp.message(SearchStates.waiting_for_querry)
def search(message: types.Message):
    query = message.text
    
    