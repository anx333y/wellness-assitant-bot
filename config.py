TOKEN = "7209979809:AAEockbzv5enrkpREs9vzpuxenUWNp-6rk8"

DATABASE_USER = "postgres"
DATABASE_PASSWORD = "123"
DATABASE_HOST = "localhost"
DATABASE_NAME = "med_assistant"

POSTGRES_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/postgres"
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

WELCOME_TEXT = (
    "Добро пожаловать в 'Персональный оздоровительный помощник'!\n"
    "Я помогу оценить ваш уровень здоровья по методике Белова В.И. "
    "и составлю индивидуальную программу оздоровления.\n\n"
    "Доступные команды:\n"
    "/start - начать работу\n"
    "Оценка здоровья - провести оценку здоровья\n"
    "Программа оздоровления - получить рекомендации\n"
    "Помощь - справка по использованию\n"
    "Индекс массы тела - рассчитать ИМТ"
)