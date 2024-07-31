from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button_count = KeyboardButton("Рассчитать")
button_info = KeyboardButton("Информация")
kb1.add(button_info)
kb1.add(button_count)

kb2 = InlineKeyboardMarkup()
button_countIn = InlineKeyboardButton(text= "Рассчитать норму калорий", callback_data = 'calories')
button_formulaIn = InlineKeyboardButton(text= "Формула расчёта", callback_data = 'formula')
kb2.add(button_countIn)
kb2.add(button_formulaIn)

#Домашнее задание по теме "Хендлеры обработки сообщений" и Домашнее задание по теме "Методы отправки сообщений".
class UserState(StatesGroup):
    age = State()
    weight = State()
    growth = State()
@dp.message_handler(commands=['start'])
async def start(message):
    print("Привет! Я бот помогающий твоему здоровью.")
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb1)
@dp.message_handler(text = "Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup = kb2)
@dp.callback_query_handler(text = 'formula')
async def get_formulas(call):
    await call.message.answer("(10 × вес в килограммах) + (6,25 × рост в сантиметрах) − (5 × возраст в годах) - 161")
    await call.answer()
@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()
@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = float(message.text))
    data = await state.get_data()
    await message.answer("Введите свой вес:")
    await UserState.weight.set()
@dp.message_handler(state = UserState.weight)
async def set_weight(message, state):
    await state.update_data(weight = float(message.text))
    data = await state.get_data()
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def send_calories(message, state):
    await state.update_data(growth = float(message.text))
    data = await state.get_data()
    #(10 × вес в килограммах) + (6,25 × рост в сантиметрах) − (5 × возраст в годах) - 161
    await message.answer(f"Ваша норма калорий {(10 * data['weight']) + (6.25 * data['growth']) - (5 * data['age']) - 161}")
    await state.finish()
@dp.message_handler()
async def all_massages(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
