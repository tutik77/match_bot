from aiogram import F, types
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot import dp
from service import RegisterService

register_service = RegisterService

class RegisterStates(StatesGroup):
    name = State()
    description = State()

@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    user = await register_service.get_user_by_id(message.from_user.id)
    if user:
        await message.answer("Вы уже зарегистрированы! Можешь искать профили.")
    else:
        await message.answer("Привет! Давай зарегистрируем тебя. Введи свое имя:")
        await state.set_state(RegisterStates.name)
        
@dp.message(F.text, state=RegisterStates.name)
async def enter_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Расскажи о себе! Введи описание своего профиля:")
    await state.set_state(RegisterStates.description)
    
@dp.message(F.text, state=RegisterStates.description)
async def enter_description(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await state.clear()
    
    new_user = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "name": user_data["name"],
        "description": message.text
    }
    
    await register_service.create_user(new_user)
    await message.answer("Ты успешно зарегистрирован! Можешь искать профили.")
    