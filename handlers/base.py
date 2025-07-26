from aiogram import Router, F
from aiogram.types import Message
from config import WELCOME_TEXT
from database.queries import save_user
from keyboards.index import main_menu

router = Router()

@router.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer(
        WELCOME_TEXT,
        reply_markup=main_menu
      )

    user = message.from_user;
    await save_user(user.id, user.full_name, user.username);

@router.message(F.text == "Помощь")
async def help_command(message: Message):
    await message.answer(WELCOME_TEXT)