from aiogram import F, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import get_session
from service import RegisterService

router = Router()

class RegisterStates(StatesGroup):
    name = State()
    description = State()


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    async for session in get_session():
        user = await RegisterService.get_user_by_tg_id(message.from_user.id, session)
    
    if user:
        await message.answer("Вы уже зарегистрированы! Чтоб искать профили, введи команду /search.")
    else:
        await message.answer("Привет! Давай зарегистрируем тебя. Введи свое имя:")
        await state.set_state(RegisterStates.name)
        

@router.message(F.text, RegisterStates.name)
async def enter_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Расскажи о себе! Введи описание своего профиля:")
    await state.set_state(RegisterStates.description)
    

@router.message(F.text, RegisterStates.description)
async def enter_description(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await state.clear()
    
    new_user = {
        "user_tg_id": message.from_user.id,
        "username": message.from_user.username,
        "name": user_data["name"],
        "description": message.text
    }
    
    async for session in get_session():
        await RegisterService.create_user(new_user, session)
    
    await message.answer("Ты успешно зарегистрирован! Чтоб искать профили, введи команду /search.")
