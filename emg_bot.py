from aiogram.dispatcher import filters
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.types import KeyboardButton,ReplyKeyboardRemove,ReplyKeyboardMarkup
from config import TOKEN_API
from emg_query import execute_query
from emg_all_pats_query import execute_query_all_pats
from emg_query import dt
from users import useridlist



kbd= ReplyKeyboardMarkup (resize_keyboard=True) 
kbd.add (KeyboardButton('Пациенты с временем ожидания более 2-х часов'))
kbd.add (KeyboardButton('Отчет по всем пациентам'))

bot= Bot(TOKEN_API)
dp= Dispatcher (bot)


@dp.message_handler (commands=['start'])
async def start_command (message:Message):
    await bot.send_message(chat_id=message.from_user.id, text='Отчет по времени ожидания в приемном Сформирован.',reply_markup=kbd)

@dp.message_handler(filters.Text(['Пациенты с временем ожидания более 2-х часов']))
async def report_button (message:Message):
    if message.from_user.id not in useridlist:
        await bot.send_message(chat_id=message.from_user.id, text=f'<b>Вы не авторизованы!</b> ❌\n<b>Ваш ID:{message.from_user.id}</b>', parse_mode='html')
    else:
       execute_query()
       await bot.send_document (chat_id=message.chat.id,
                               document=open(f'/opt/emg_bot/emgg/Пациенты с ожиданием больше 120 минут_{dt}.xlsx', 'rb'),
                               parse_mode='', reply_markup=ReplyKeyboardRemove())
@dp.message_handler(filters.Text(['Отчет по всем пациентам']))
async def report_button_2 (message:Message):
    if message.from_user.id not in useridlist:
        await bot.send_message(chat_id=message.from_user.id, text=f'<b>Вы не авторизованы!</b> ❌\n<b>Ваш ID:{message.from_user.id}</b>', parse_mode='html')
    else:
       execute_query_all_pats()
       await bot.send_document (chat_id=message.chat.id,
                               document=open(f'/opt/emg_bot/emgg/Поступившие пациенты за сутки_{dt}.xlsx', 'rb'),
                               parse_mode='', reply_markup=ReplyKeyboardRemove())





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)