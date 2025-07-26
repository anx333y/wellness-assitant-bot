from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Оценка здоровья"), KeyboardButton(text="Программа оздоровления")],
        [KeyboardButton(text="Индекс массы тела")],
        [KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True
)

def get_gender_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мужской", callback_data="gender_m")],
        [InlineKeyboardButton(text="Женский", callback_data="gender_f")]
    ])

def get_yes_no_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="yes")],
        [InlineKeyboardButton(text="Нет", callback_data="no")]
    ])

def get_cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="cancel_assessment")]
    ])

def get_confirm_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="confirm")],
        [InlineKeyboardButton(text="Изменить", callback_data="change_data")]
    ])

def get_program_options_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Рекомендации по нагрузкам", callback_data="program_load")],
        [InlineKeyboardButton(text="План питания", callback_data="program_nutrition")],
        [InlineKeyboardButton(text="Режим дня", callback_data="program_schedule")],
        [InlineKeyboardButton(text="Все рекомендации", callback_data="program_full")]
    ])