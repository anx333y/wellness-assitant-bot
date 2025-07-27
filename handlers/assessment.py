from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
from keyboards.index import (
    main_menu,
    get_gender_keyboard,
    get_yes_no_keyboard,
    get_cancel_keyboard,
    get_confirm_keyboard
)
from database.queries import save_health_data

router = Router()

class AssessmentStates(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
    heart_rate = State()
    blood_pressure_systolic = State()
    blood_pressure_diastolic = State()
    vital_capacity = State()
    training_experience = State()
    smoking = State()
    hardening = State()
    run_2km = State()
    recovery_heart_rate = State()
    strength_tests = State()
    colds_frequency = State()
    chronic_diseases = State()
    confirm = State()

@router.message(F.text == "Оценка здоровья")
async def start_assessment(message: Message, state: FSMContext):
    await state.clear()

    await state.set_state(AssessmentStates.gender)
    await message.answer(
        "Начнем оценку вашего здоровья по методике Белова В.И.\n"
        "Укажите ваш пол:",
        reply_markup=get_gender_keyboard()
    )

@router.callback_query(F.data.startswith("gender_"), AssessmentStates.gender)
async def process_gender(callback: CallbackQuery, state: FSMContext):
    gender = "М" if callback.data == "gender_m" else "Ж"
    await state.update_data(gender=gender)
    await callback.message.edit_text(f"Пол: {gender}")
    await callback.message.answer(
        "Введите ваш возраст (полных лет):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AssessmentStates.age)
    await callback.answer()

@router.message(AssessmentStates.age, F.text.isdigit())
async def process_age(message: Message, state: FSMContext):
    age = int(message.text)
    if not 10 <= age <= 120:
        await message.answer("Пожалуйста, введите возраст от 10 до 120 лет")
        return
    
    await state.update_data(age=age)
    await state.set_state(AssessmentStates.height)
    await message.answer(
        "Введите ваш рост в см:",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.age)
async def incorrect_age(message: Message):
    await message.answer(
        "Пожалуйста, введите возраст цифрами (например, 25):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.height, F.text.isdigit())
async def process_height(message: Message, state: FSMContext):
    height = int(message.text)
    if not 100 <= height <= 250:
        await message.answer("Пожалуйста, введите рост от 100 до 250 см")
        return
    
    await state.update_data(height=height)
    await state.set_state(AssessmentStates.weight)
    await message.answer(
        "Введите ваш вес в кг:",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.height)
async def incorrect_height(message: Message):
    await message.answer(
        "Пожалуйста, введите рост цифрами (например, 175):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.weight, F.text.isdigit())
async def process_weight(message: Message, state: FSMContext):
    weight = int(message.text)
    if not 30 <= weight <= 300:
        await message.answer("Пожалуйста, введите вес от 30 до 300 кг")
        return
    
    await state.update_data(weight=weight)
    await state.set_state(AssessmentStates.heart_rate)
    await message.answer(
        "Введите ваш пульс в покое (уд/мин):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.heart_rate, F.text.isdigit())
async def process_heart_rate(message: Message, state: FSMContext):
    heart_rate = int(message.text)
    if not 40 <= heart_rate <= 120:
        await message.answer("Пожалуйста, введите корректный пульс (40-120 уд/мин)")
        return
    
    await state.update_data(heart_rate=heart_rate)
    await state.set_state(AssessmentStates.blood_pressure_systolic)
    await message.answer(
        "Введите ваше систолическое давление (верхнее число, например 120):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.heart_rate)
async def incorrect_heart_rate(message: Message):
    await message.answer(
        "Пожалуйста, введите пульс цифрами (например, 72):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.blood_pressure_systolic, F.text.isdigit())
async def process_blood_pressure_systolic(message: Message, state: FSMContext):
    systolic = int(message.text)
    if not 80 <= systolic <= 200:
        await message.answer("Пожалуйста, введите корректное значение (80-200)")
        return
    
    await state.update_data(blood_pressure_systolic=systolic)
    await state.set_state(AssessmentStates.blood_pressure_diastolic)
    await message.answer(
        "Введите ваше диастолическое давление (нижнее число, например 80):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.blood_pressure_systolic)
async def incorrect_blood_pressure_systolic(message: Message):
    await message.answer(
        "Пожалуйста, введите значение цифрами (например, 120):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.blood_pressure_diastolic, F.text.isdigit())
async def process_blood_pressure_diastolic(message: Message, state: FSMContext):
    diastolic = int(message.text)
    if not 50 <= diastolic <= 120:
        await message.answer("Пожалуйста, введите корректное значение (50-120)")
        return
    
    await state.update_data(blood_pressure_diastolic=diastolic)
    await state.set_state(AssessmentStates.vital_capacity)
    await message.answer(
        "Введите показатель ЖЕЛ (жизненная ёмкость легких) в мл:",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.blood_pressure_diastolic)
async def incorrect_blood_pressure_diastolic(message: Message):
    await message.answer(
        "Пожалуйста, введите значение цифрами (например, 80):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.weight)
async def incorrect_weight(message: Message):
    await message.answer(
        "Пожалуйста, введите вес цифрами (например, 70):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.vital_capacity, F.text.isdigit())
async def process_vital_capacity(message: Message, state: FSMContext):
    vital_capacity = int(message.text)
    if not 1000 <= vital_capacity <= 7000:
        await message.answer("Пожалуйста, введите ЖЕЛ от 1000 до 7000 мл")
        return
    
    await state.update_data(vital_capacity=vital_capacity)
    await state.set_state(AssessmentStates.training_experience)
    await message.answer(
        "Введите ваш стаж регулярных занятий физкультурой (в годах):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.training_experience, F.text.isdigit())
async def process_training_experience(message: Message, state: FSMContext):
    experience = int(message.text)
    if not 0 <= experience <= 70:
        await message.answer("Пожалуйста, введите стаж от 0 до 70 лет")
        return
    
    await state.update_data(training_experience=experience)
    await state.set_state(AssessmentStates.smoking)
    await message.answer(
        "Курите ли вы?",
        reply_markup=get_yes_no_keyboard()
    )

@router.callback_query(F.data.in_(["yes", "no"]), AssessmentStates.smoking)
async def process_smoking(callback: CallbackQuery, state: FSMContext):
    is_smoking = callback.data == "yes"
    await state.update_data(smoking=is_smoking)
    await callback.message.edit_text(f"Курение: {'Да' if is_smoking else 'Нет'}")
    await callback.message.answer(
        "Практикуете ли вы закаливание?",
        reply_markup=get_yes_no_keyboard()
    )
    await state.set_state(AssessmentStates.hardening)
    await callback.answer()

@router.callback_query(F.data.in_(["yes", "no"]), AssessmentStates.hardening)
async def process_hardening(callback: CallbackQuery, state: FSMContext):
    is_hardening = callback.data == "yes"
    await state.update_data(hardening=is_hardening)
    await callback.message.edit_text(f"Закаливание: {'Да' if is_hardening else 'Нет'}")
    await callback.message.answer(
        "Введите ваше время бега на 2 км (в минутах, например 12.5):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AssessmentStates.run_2km)
    await callback.answer()

@router.message(AssessmentStates.run_2km)
async def process_run_2km(message: Message, state: FSMContext):
    try:
        run_time = float(message.text.replace(",", "."))
        if not 7.0 <= run_time <= 30.0:
            raise ValueError
        await state.update_data(run_2km=run_time)
        await state.set_state(AssessmentStates.recovery_heart_rate)
        await message.answer(
            "Введите время восстановления ЧСС после нагрузки (в минутах до возвращения к норме):",
            reply_markup=get_cancel_keyboard()
        )
    except:
        await message.answer(
            "Пожалуйста, введите время от 7 до 30 минут (например 12.5):",
            reply_markup=get_cancel_keyboard()
        )

@router.message(AssessmentStates.recovery_heart_rate, F.text.isdigit())
async def process_recovery_heart_rate(message: Message, state: FSMContext):
    recovery_time = int(message.text)
    if not 1 <= recovery_time <= 30:
        await message.answer("Пожалуйста, введите время от 1 до 30 минут")
        return
     
    data = await state.get_data()
    answer = "Введите количество подтягиваний за 1 минуту" if data["gender"] == 'М' else "Введите количество подъемов туловища за 1 минуту"
    
    await state.update_data(recovery_heart_rate=recovery_time)
    await state.set_state(AssessmentStates.strength_tests)
    await message.answer(
        answer,
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.strength_tests, F.text.isdigit())
async def process_strength_tests(message: Message, state: FSMContext):
    strength = int(message.text)
    if not 0 <= strength <= 50:
        await message.answer("Пожалуйста, введите количество от 0 до 50 раз")
        return
    
    await state.update_data(strength_tests=strength)
    await state.set_state(AssessmentStates.colds_frequency)
    await message.answer(
        "Как часто вы болеете простудными заболеваниями? (раз в год):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AssessmentStates.colds_frequency, F.text.isdigit())
async def process_colds_frequency(message: Message, state: FSMContext):
    colds = int(message.text)
    if not 0 <= colds <= 12:
        await message.answer("Пожалуйста, введите количество от 0 до 12 раз в год")
        return
    
    await state.update_data(colds_frequency=colds)
    await state.set_state(AssessmentStates.chronic_diseases)
    await message.answer(
        "Есть ли у вас хронические заболевания?",
        reply_markup=get_yes_no_keyboard()
    )

@router.callback_query(F.data.in_(["yes", "no"]), AssessmentStates.chronic_diseases)
async def process_chronic_diseases(callback: CallbackQuery, state: FSMContext):
    has_diseases = callback.data == "yes"
    await state.update_data(chronic_diseases=has_diseases)
    
    data = await state.get_data()
    summary = "\n".join([
        f"Проверьте данные:",
        f"Пол: {'М' if data['gender'] == 'М' else 'Ж'}",
        f"Возраст: {data['age']} лет",
        f"Рост: {data['height']} см",
        f"Вес: {data['weight']} кг",
        f"Пульс: {data['heart_rate']} уд/мин",
        f"Давление: {data['blood_pressure_systolic']}/{data['blood_pressure_diastolic']}",
        f"ЖЕЛ: {data['vital_capacity']} мл",
        f"Стаж тренировок: {data['training_experience']} лет",
        f"Курение: {'Да' if data['smoking'] else 'Нет'}",
        f"Закаливание: {'Да' if data['hardening'] else 'Нет'}",
        f"Бег 2 км: {data['run_2km']} мин",
        f"Восстановление ЧСС: {data['recovery_heart_rate']} мин",
        f"Силовые показатели: {data['strength_tests']} раз",
        f"Простуды: {data['colds_frequency']} раз/год",
        f"Хронические заболевания: {'Да' if has_diseases else 'Нет'}"
    ])
    
    await callback.message.edit_text(summary)
    await callback.message.answer(
        "Подтвердите правильность введенных данных:",
        reply_markup=get_confirm_keyboard()
    )
    await state.set_state(AssessmentStates.confirm)
    await callback.answer()

@router.callback_query(F.data == "confirm", AssessmentStates.confirm)
async def confirm_assessment(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        score = calculate_health_score(data)
        
        data.update({
            'score': score,
            'user_id': callback.from_user.id
        })
        
        await save_health_data(callback.from_user.id, data)        
        health_status = "Отличное" if score >= 8 else "Хорошее" if score >= 6 else "Удовлетворительное"
        
        await callback.message.edit_text(
            f"✅ <b>Оценка здоровья завершена!</b>\n\n"
            f"<i>Ваш результат:</i>\n"
            f"▪ Уровень здоровья: <b>{score:.1f}/10</b> ({health_status})\n"
            f"▪ Рекомендации: нажмите «Программа оздоровления»",
            parse_mode="HTML"
        )
        
        await callback.message.answer(
            "Выберите следующее действие:",
            reply_markup=main_menu
        )
        
    except Exception as e:
        await callback.message.answer(
            "Произошла ошибка при сохранении результатов. Пожалуйста, попробуйте позже.",
            reply_markup=main_menu
        )
        print(e)
    finally:
        await callback.answer()

@router.callback_query(F.data == "cancel_assessment")
async def cancel_assessment(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.message.edit_text("❌ Оценка здоровья отменена")
        await callback.message.answer(
            "Вы можете начать заново, выбрав «Оценка здоровья»",
            reply_markup=main_menu
        )
    except Exception as e:
        await callback.message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте еще раз.",
            reply_markup=main_menu
        )
    finally:
        await callback.answer()

def calculate_health_score(data):
    score = 0
    gender = data.get('gender', 'М')
    
    # Возрастные коэффициенты
    age = data.get('age', 30)
    if age < 30:
        score += 2.0
    elif 30 <= age < 50:
        score += 1.5
    else:
        score += 1.0
    
    # Сердечно-сосудистая система
    # Пульс в покое
    heart_rate = data.get('heart_rate', 72)
    if heart_rate < 60:
        score += 1.5
    elif 60 <= heart_rate < 70:
        score += 1.0
    else:
        score += 0.5
    
    # Артериальное давление
    systolic = data.get('blood_pressure_systolic', 120)
    diastolic = data.get('blood_pressure_diastolic', 80)
    if systolic < 120 and diastolic < 80:
        score += 1.5
    elif 120 <= systolic < 130 and 80 <= diastolic < 85:
        score += 1.0
    else:
        score += 0.5
    
    # Дыхательная система
    vital_capacity = data.get('vital_capacity', 3000)
    if gender == 'М':
        if vital_capacity >= 4500: score += 2.0
        elif 3500 <= vital_capacity < 4500: score += 1.5
        else: score += 1.0
    else:
        if vital_capacity >= 3500: score += 2.0
        elif 2500 <= vital_capacity < 3500: score += 1.5
        else: score += 1.0
    
    # Физическая активность
    # Стаж тренировок
    experience = data.get('training_experience', 0)
    if experience >= 5: score += 1.5
    elif 1 <= experience < 5: score += 1.0
    
    # Время бега
    run_time = data.get('run_2km', 15)
    if gender == 'М':
        if run_time < 10: score += 1.5
        elif 10 <= run_time < 12: score += 1.0
    else:
        if run_time < 12: score += 1.5
        elif 12 <= run_time < 14: score += 1.0
    
    # Образ жизни
    if not data.get('smoking', False): score += 1.0
    if data.get('hardening', False): score += 1.0
    
    # Дополнительные факторы
    if not data.get('chronic_diseases', False): score += 1.0
    if data.get('colds_frequency', 0) <= 2: score += 1.0
    
    # Нормализация до 10 баллов с учетом весовых коэффициентов
    return min(10.0, score * 0.8)