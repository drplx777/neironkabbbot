import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.keyboards as kb
from app.states import Chat, Image, AddBalance
from aiogram.fsm.context import FSMContext
from app.generations import gpt_text, gpt_image, gpt_vision, Iam_Alive
from app.database.requests import set_user, get_user, calculate, update_balance
from decimal import Decimal
import uuid

user = Router()

@user.message(F.text == 'Отмена')
@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await set_user(message.from_user.id)
    await message.answer('Добро Пожаловать!', reply_markup=kb.main)
    await message.answer('⬇️⬇️⬇️Соц. Сети разработчика⬇️⬇️⬇️', reply_markup=kb.credits)
    await state.clear()
    await Iam_Alive()
    
    
@user.message(F.text == 'Чат')
async def chatting(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        await state.set_state(Chat.text)
        await message.answer('Введите ваш запрос', reply_markup=kb.cancel)
    else:
        await message.answer('Недостаточно средств на балансе')
    
@user.message(Chat.text, F.photo)
async def chat_response(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        await state.set_state(Chat.wait)
        file = await message.bot.get_file(message.photo[-1].file_id)
        file_path = file.file_path
        file_name = uuid.uuid4()
        await message.bot.download_file(file_path, f'{file_name}.jpeg')
        response = await gpt_vision(message.caption, 'gpt-4o', f'{file_name}.jpeg')
        await calculate(message.from_user.id, response['usage'], 'gpt-4o', user)
        await message.answer(response['response'])
        await state.set_state(Chat.text)
        os.remove(f'{file_name}.jpeg')
    else:
        await message.answer('Недостаточно средств на балансе.')


@user.message(Chat.text)
async def chat_response(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        await state.set_state(Chat.wait)
        response = await gpt_text(message.text, 'gpt-4o')
        await calculate(message.from_user.id, response['usage'], 'gpt-4o', user)
        await message.answer(response['responce'])
        await state.set_state(Chat.text)
    else:
        await message.answer('Недостаточно средств на балансе')

@user.message(Image.wait)    
@user.message(Chat.wait)
async def stop_spam(message: Message):
    await message.answer('Подождите пока обработается запрос')
    
    
@user.message(F.text == 'Генерация картинок')
async def chatting(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        await state.set_state(Image.text)
        await message.answer('Введите ваш запрос', reply_markup=kb.cancel)
    else:
        await message.answer('Недостаточно средств на балансе')
    
@user.message(Image.text)
async def chat_response(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        await state.set_state(Image.wait)
        response = await gpt_image(message.text, 'dall-e-3')
        await calculate(message.from_user.id, response['usage'], 'dall-e-3', user)
        print(response)
        try:
            await message.answer_photo(response['responce'])
        except Exception as e:
            print(e)
            await message.answer(response['responce'])
        await state.set_state(Image.text)
    else:
        await message.answer('Недостаточно средств на балансе')
    
@user.message(F.text == 'Пополнить баланс')
async def add_balance(message: Message, state: FSMContext):
    await state.set_state(AddBalance.balance_add)
    await message.answer('Введите сумму на которую вы хотите пополнить баланс')

@user.message(AddBalance.balance_add)
async def add_balance(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    await update_balance(user, Decimal(message.text))
    await state.clear()
    await message.answer('Баланс успешно пополнен')