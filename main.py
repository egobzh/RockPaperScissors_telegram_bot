from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import random
from bot_config import *
import sqlite3
from datetime import date

conn = sqlite3.connect('rsp.db')  # sql connection
cur = conn.cursor()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def main():
    #BUTTONS:
    #START KEYBOARD=======================================================================
    start_buttons=['Играть!▶️','Профиль📱','Таблица Лидеров📈','Правила📝']
    start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    start_kb.add(*start_buttons)
    #=====================================================================================
    #PLAY KEYBOARD========================================================================
    play_buttons=['Камень🗿','Ножницы✂','Бумага🔖','Стартовое меню🗨']
    play_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    play_kb.add(*play_buttons)
    #=====================================================================================
    #Next Game Keyboard===================================================================
    ng_buttons=['Сыграть еще раз!🕹','Стартовое меню🗨']
    ng_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    ng_kb.add(*ng_buttons)
    #=====================================================================================
    # Leaders Keyboard====================================================================
    lk_buttons = ['Матчи🤼', 'Победы🏆', 'Кредиты💰', 'Стартовое меню🗨']
    lk_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    lk_kb.add(*lk_buttons)
    # ====================================================================================
    # Profile Keyboard====================================================================
    profile_buttons = ['Изменить имя✏', 'Стартовое меню🗨']
    pf_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    pf_kb.add(*profile_buttons)

    # =====================================================================================

    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        await message.answer(f"Привет, {message.from_user.first_name}! Это бот для игры в 'Камень, Ножницы, Бумага!'", reply_markup=start_kb)
        await message.answer("Стартовое меню:", reply_markup=start_kb)

        user_id = message.from_user.id
        cur.execute(f'SELECT EXISTS(SELECT id FROM users WHERE id = {user_id}) ;')
        one_result = cur.fetchone()
        if one_result[0] == True:
            pass
        else:
            cur.execute(f"""INSERT INTO users(id, name, regdate, games, wins, draws,loses, credits)
            VALUES('{message.from_user.id}', '{message.from_user.first_name}', '{date.today()}', '0','0','0','0', '0');""")
            conn.commit()

    @dp.message_handler(Text(equals="Правила📝"))
    async def with_puree(message: types.Message):
        await message.reply("""Победитель определяется по следующим правилам:\n
Бумага побеждает камень («бумага обёртывает камень»).\n
Камень побеждает ножницы («камень затупляет или ломает ножницы»).\n
Ножницы побеждают бумагу («ножницы разрезают бумагу»).\n
Если игроки показали одинаковый знак, то засчитывается ничья и игра переигрывается.""")



    @dp.message_handler(Text(equals="Профиль📱"))
    async def profile(message: types.Message):
        user_id = message.from_user.id
        cur.execute(f"""SELECT * FROM users WHERE id={user_id};""")
        one_result = cur.fetchone()
        await message.reply(f'Ваш профиль📱:\nДата регистрации: {one_result[2]}\nИмя: {one_result[1]}\nМатчи: {one_result[3]}\nПобеды: {one_result[4]}\nНичьи: {one_result[5]}\nПоражения: {one_result[6]}\nБаланс кредитов💰: {one_result[7]}\n', reply_markup=pf_kb)

    @dp.message_handler(Text(equals="Изменить имя✏"))
    async def setname_guide(message: types.Message):
        await message.answer("Для того, чтобы изменить имя воспользуйся командой /setname. Имя не должно содержать ссылок и быть длинной до 15 символов. Пример: /setname Иван Грозный", reply_markup=pf_kb)

    @dp.message_handler(commands=['setname'])
    async def process_start_command(message: types.Message):
        new_name=message.text[9:]
        if len(new_name)>15:
            await message.answer(f"Длина имени не должна превышать 15 символов!❌", reply_markup=pf_kb)
        elif len(new_name)==0 or new_name.isspace():
            await message.answer(f"Имя не может состоять только из пробелов и пустых символов!❌", reply_markup=pf_kb)
        else:
            user_id = message.from_user.id
            cur.execute(f"""UPDATE users SET name = '{new_name}' WHERE id = {user_id} ;""")
            conn.commit()
            await message.answer(f"Ваше имя успешно изменено!✅", reply_markup=pf_kb)

    @dp.message_handler(Text(equals="Таблица Лидеров📈"))
    async def leaders(message: types.Message):
        await message.answer("Выбери таблицу лидеров, которую хочешь увидеть:", reply_markup=lk_kb)

    @dp.message_handler(Text(equals="Матчи🤼"))
    async def games_leaders(message: types.Message):
        cur.execute(f"""SELECT * FROM users ORDER BY games DESC;""")
        one_result = cur.fetchmany(10)
        msgg = ''
        for indx, i in enumerate(one_result):
            if indx != 10:
                msgg += f'#{indx + 1} {i[1]}. Матчи: {i[3]}\n'
            else:
                msgg += f'#{indx + 1} {i[1]}. Матчи: {i[3]}'

        await message.answer(msgg, reply_markup=lk_kb)

    @dp.message_handler(Text(equals="Победы🏆"))
    async def wins_leaders(message: types.Message):
        cur.execute(f"""SELECT * FROM users ORDER BY wins DESC;""")
        one_result = cur.fetchmany(10)
        msgg = ''
        for indx, i in enumerate(one_result):
            if indx != 10:
                msgg += f'#{indx + 1} {i[1]}. Победы: {i[4]}\n'
            else:
                msgg += f'#{indx + 1} {i[1]}. Победы: {i[4]}'

        await message.answer(msgg, reply_markup=lk_kb)

    @dp.message_handler(Text(equals="Кредиты💰"))
    async def credits_leaders(message: types.Message):
        cur.execute(f"""SELECT * FROM users ORDER BY credits DESC;""")
        one_result = cur.fetchmany(10)
        msgg = ''
        for indx, i in enumerate(one_result):
            if indx != 10:
                msgg += f'#{indx + 1} {i[1]}. Кредиты: {i[7]}\n'
            else:
                msgg += f'#{indx + 1} {i[1]}. Кредиты: {i[7]}'

        await message.answer(msgg, reply_markup=lk_kb)

    @dp.message_handler(Text(equals="Играть!▶️"))
    async def play_command(message: types.Message):
        await message.answer("Выбери то,чем собираешься ходить:", reply_markup=play_kb)

    @dp.message_handler(Text(equals='Сыграть еще раз!🕹'))
    async def playagain_command(message: types.Message):
        await message.answer("Выбери то,чем собираешься ходить:", reply_markup=play_kb)

    @dp.message_handler(Text(equals='Стартовое меню🗨'))
    async def start_menu(message: types.Message):
        await message.answer("Стартовое меню:", reply_markup=start_kb)

    @dp.message_handler(Text(equals='Камень🗿'))
    async def rock_bot_logik(message: types.Message):

        hod_comp=random.randint(1,3)

        user_id = message.from_user.id

        if hod_comp == 1:
            HOD_COMP = 'Камень'
        elif hod_comp == 2:
            HOD_COMP = 'Ножницы'
        elif hod_comp == 3:
            HOD_COMP = 'Бумага'
        await message.reply(f'Ваш ход - Камень\nХод компьютера - {HOD_COMP}')

        if hod_comp==1:
            await message.answer("Ничья!\nКредиты💰: +25", reply_markup=ng_kb)
            cur.execute(f"""UPDATE users SET draws = draws + 1, games = games + 1,credits = credits + 25 WHERE id = {user_id} ;""")
            conn.commit()
        elif hod_comp==2:
            await message.answer("Победа!!\nКамень бьет ножницы!\nКредиты💰: +50", reply_markup=ng_kb)
            cur.execute(f"""UPDATE users SET wins = wins + 1, games = games + 1,credits = credits + 50 WHERE id = {user_id} ;""")
            conn.commit()
        elif hod_comp==3:
            await message.answer("Поражение(\nБумага бьет камень!!\nКредиты💰: +10", reply_markup=ng_kb)
            cur.execute(f"""UPDATE users SET loses = loses + 1, games = games + 1,credits = credits + 10 WHERE id = {user_id} ;""")
            conn.commit()
        await message.answer("Желаешь сыграть еще раз? ", reply_markup=ng_kb)

    @dp.message_handler(Text(equals='Ножницы✂'))
    async def scissors_bot_logik(message: types.Message):

        hod_comp = random.randint(1, 3)

        user_id = message.from_user.id

        if hod_comp == 1:
            HOD_COMP = 'Камень'
        elif hod_comp == 2:
            HOD_COMP = 'Ножницы'
        elif hod_comp == 3:
            HOD_COMP = 'Бумага'
        await message.reply(f'Ваш ход - Ножницы\nХод компьютера - {HOD_COMP}')

        if hod_comp == 1:
            await message.answer("Поражение(\nКамень бьет ножницы!!\nКредиты💰: +10", reply_markup=ng_kb)
            cur.execute(f"""UPDATE users SET loses = loses + 1, games = games + 1,credits = credits + 10 WHERE id = {user_id} ;""")
            conn.commit()
        elif hod_comp == 2:
            await message.answer("Ничья!\nКредиты💰: +25", reply_markup=ng_kb)
            cur.execute(f"""UPDATE users SET draws = draws + 1, games = games + 1,credits = credits + 25 WHERE id = {user_id} ;""")
            conn.commit()
        elif hod_comp == 3:
            await message.answer("Победа!!\nНожницы бьют бумагу!\nКредиты💰: +50", reply_markup=ng_kb)
            cur.execute(f"""UPDATE users SET wins = wins + 1, games = games + 1,credits = credits + 50 WHERE id = {user_id} ;""")
            conn.commit()
        await message.answer("Желаешь сыграть еще раз? ", reply_markup=ng_kb)

    @dp.message_handler(Text(equals='Бумага🔖'))
    async def paper_bot_logik(message: types.Message):

        hod_comp = random.randint(1, 3)

        user_id = message.from_user.id

        if hod_comp == 1:
            HOD_COMP = 'Камень'
        elif hod_comp == 2:
            HOD_COMP = 'Ножницы'
        elif hod_comp == 3:
            HOD_COMP = 'Бумага'
        await message.reply(f'Ваш ход - Бумага\nХод компьютера - {HOD_COMP}')

        if hod_comp == 1:
            await message.answer("Победа!!\nБумага бьет камень!\nКредиты💰: +50", reply_markup=ng_kb)
            cur.execute(f"""UPDATE users SET wins = wins + 1, games = games + 1,credits = credits + 50 WHERE id = {user_id} ;""")
            conn.commit()
        elif hod_comp == 2:
            await message.answer("Поражение(\nНожницы бьют камень!!\nКредиты💰: +10", reply_markup=ng_kb)
            cur.execute(f"""UPDATE users SET loses = loses + 1, games = games + 1,credits = credits + 10 WHERE id = {user_id} ;""")
            conn.commit()
        elif hod_comp == 3:
            await message.answer("Ничья!\nКредиты💰: +25", reply_markup=ng_kb)
            cur.execute(f"""UPDATE users SET draws = draws + 1, games = games + 1,credits = credits + 25 WHERE id = {user_id} ;""")
            conn.commit()
        await message.answer("Желаешь сыграть еще раз? ", reply_markup=ng_kb)


    executor.start_polling(dp,skip_updates=True)

if __name__=='__main__':
    main()
