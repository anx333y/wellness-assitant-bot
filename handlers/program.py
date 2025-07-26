from aiogram import Router, F
from aiogram.types import Message
from keyboards.index import main_menu
from database.queries import get_last_health_data

router = Router()

@router.message(F.text == "Программа оздоровления")
async def get_program(message: Message):
    user_id = message.from_user.id
    saved_data = await get_last_health_data(user_id)
    
    if not saved_data or not saved_data.score:
        await message.answer("❌ Сначала пройдите оценку здоровья")
        return
    
    score = saved_data.score    
    program = generate_program(score)
    
    await message.answer(
        f"🏆 Ваш уровень здоровья: {score:.1f}/10\n\n"
        f"📋 Рекомендации:\n{program}",
        reply_markup=main_menu
    )

def generate_program(score: float) -> str:
    """Генерация персонализированной программы"""
    if score >= 8:
        return (
            "✅ Отличное здоровье!\n\n"
            "• 3-4 тренировки в неделю\n"
            "• Продолжительность: 40-50 минут\n"
            "• Кардионагрузки: 30%\n"
            "• Силовые: 40%\n"
            "• Растяжка: 30%"
        )
    elif 6 <= score < 8:
        return (
            "👍 Хорошее здоровье\n\n"
            "• 4 тренировки в неделю\n"
            "• Продолжительность: 30-45 минут\n"
            "• Кардионагрузки: 40%\n"
            "• Силовые: 40%\n"
            "• Растяжка: 20%"
        )
    else:
        return (
            "💪 Требуется улучшение\n\n"
            "• 5 тренировок в неделю\n"
            "• Продолжительность: 20-30 минут\n"
            "• Кардионагрузки: 50%\n"
            "• Растяжка: 50%"
        )