from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database.queries import save_imt_data, get_last_imt_data

router = Router()

class IMTStates(StatesGroup):
    weight = State()
    height = State()

@router.message(F.text == "Индекс массы тела")
async def start_imt(message: Message, state: FSMContext):
    await state.set_state(IMTStates.weight)
    await message.answer("Введите ваш вес в кг:")

@router.message(IMTStates.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text.replace(",", "."))
        if weight < 20 or weight > 300:
            raise ValueError
        await state.update_data(weight=weight)
        await state.set_state(IMTStates.height)
        await message.answer("Введите ваш рост в см:")
    except:
        await message.answer("Пожалуйста, введите корректный вес (20-300 кг)")

@router.message(IMTStates.height)
async def process_height(message: Message, state: FSMContext):
    try:
        height = float(message.text.replace(",", "."))
        if height < 100 or height > 250:
            raise ValueError
        
        data = await state.get_data()
        weight = data["weight"]
        imt = weight / ((height / 100) ** 2)
        
        if imt < 16:
            conclusion = "Выраженный дефицит массы тела"
        elif 16 <= imt < 18.5:
            conclusion = "Недостаточная масса тела"
        elif 18.5 <= imt < 25:
            conclusion = "Нормальная масса тела"
        elif 25 <= imt < 30:
            conclusion = "Избыточная масса тела"
        elif 30 <= imt < 35:
            conclusion = "Ожирение 1 степени"
        elif 35 <= imt < 40:
            conclusion = "Ожирение 2 степени"
        else:
            conclusion = "Ожирение 3 степени"

        saved_data = await get_last_imt_data(message.from_user.id);
        
        if not saved_data:
          await message.answer(
              f"Ваш ИМТ: {imt:.1f}\n"
              f"Заключение: {conclusion}"
          )
        else:
          await message.answer(
            f"Ваш прошлый ИМТ: {saved_data.imt:.1f}\n"
            ""
            f"Ваш актуальный ИМТ {imt:.1f}\n"
            f"Заключение: {conclusion}"
          )
          
        

        await save_imt_data(message.from_user.id, {
            'height': height,
            'weight': weight,
            'imt': imt
        })

        await state.clear()
    except:
        await message.answer("Пожалуйста, введите корректный рост (100-250 см)")