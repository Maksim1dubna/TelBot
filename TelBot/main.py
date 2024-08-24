from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from crud_functions import *

initiate_db()

api = '7215043429:AAG_uzDkLgv7e9LrzVKydxHdx5GVdHlHcYg'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button_count = KeyboardButton("Рассчитать")
button_info = KeyboardButton("Информация")
button_buy = KeyboardButton("Купить")
kb1.add(button_info)
kb1.add(button_count)
kb1.add(button_buy)

kb2 = InlineKeyboardMarkup()
button_countIn = InlineKeyboardButton(text= "Рассчитать норму калорий", callback_data = 'calories')
button_formulaIn = InlineKeyboardButton(text= "Формула расчёта", callback_data = 'formula')
kb2.add(button_countIn)
kb2.add(button_formulaIn)

kb_goods = InlineKeyboardMarkup()
Product1 = InlineKeyboardButton(text= "Product1", callback_data="product_buying")
Product2 = InlineKeyboardButton(text= "Product2", callback_data="product_buying")
Product3 = InlineKeyboardButton(text= "Product3", callback_data="product_buying")
Product4 = InlineKeyboardButton(text= "Product4", callback_data="product_buying")
kb_goods.add(Product1)
kb_goods.add(Product2)
kb_goods.add(Product3)
kb_goods.add(Product4)

#Домашнее задание по теме "Хендлеры обработки сообщений" и Домашнее задание по теме "Методы отправки сообщений".
class UserState(StatesGroup):
    age = State()
    weight = State()
    growth = State()
# Базовые функции -------------------------------------------
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
# -------------------------------------------
# Покупки -----------------------------------
@dp.message_handler(text = "Купить")
async def get_buying_list(message):
    goods_list = get_all_products()
    for i in range(len(goods_list)):
        await message.answer(f'Название: {goods_list[i][1]} | Описание: {goods_list[i][2]} | Цена: {goods_list[i][3]}')
        # await bot.send_photo(message.chat.id, 'https://tula.rus-sport.net/upload/iblock/6e5/rmq6jstf9su9enzravs130slx7gwswxu.jpg')
    await message.answer("Выберите продукт для покупки:", reply_markup = kb_goods)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
# -------------------------------------------

@dp.message_handler()
async def all_massages(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
