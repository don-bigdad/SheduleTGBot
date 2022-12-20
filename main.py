import telebot
import datetime,calendar
import psycopg2

bot = telebot.TeleBot("5833363637:AAGG2abyu-ZA8D21n8o3Y2NrJ4bzAY_Pzss")

conn = psycopg2.connect(host="localhost", port = 5432, database="shedulebot", user="postgres", password="bogdan")
cursor = conn.cursor()
print("Database opened successfully")
cursor.execute("""SELECT * FROM users""")
query_results = cursor.fetchall()
text = '\n'.join([', '.join(map(str, x)) for x in query_results])
print(str(text))

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    add_shedule = telebot.types.InlineKeyboardButton(text="Створити розклад", callback_data="Створити")
    change_shedule = telebot.types.InlineKeyboardButton(text="Виправити розклад", callback_data="Змінити")
    delete_shedule = telebot.types.InlineKeyboardButton(text="Видалити розклад", callback_data="Видалити")
    markup.add(add_shedule, change_shedule, delete_shedule)
    msg = bot.send_message(message.chat.id, 'Привіт! Я бот котрий допоможе тобі зробити твоє студентське життя '
                                            'трішечки легше!Почнемо?', reply_markup=markup)

@bot.message_handler(commands=["Пары",])
def get_today_shedule(message):
    user_message =  message.text
    if user_message.title() in ['Пари','Пары','Сьогодні','Уроки','Розклад']:
        today = calendar.day_name[datetime.date.today().weekday()].lower()
        translate = {'monday':'Понеділок','thuesday':'Вівторок','wednesday':'Середа','thursday':'Четверг','Friday':"П'ятниця",'saturday':'Суббота'}
        cursor.execute("""SELECT username FROM users""")
        query_results = cursor.fetchall()
        for username in text.split():
            if username == message.from_user.username:
                bot.send_message(message.chat.id,f'your username is {username}' )
                bot.send_message(message.chat.id,f'Розклад на сьогодні({translate[today]}):')
    else:
        bot.send_message(message.chat.id,'Введіть ключове слово щоб дізнатись розклад на сьогодні,ключові слова:\nПари,Пары,,Cьогодні,Уроки,Розклад')

@bot.callback_query_handler(func=lambda callback: callback.data)
def shedule_answer(callback):
    if callback.data == "Створити":
        cursor.execute('''SELECT username FROM users''')
        query_results = cursor.fetchall()
        text = '\n'.join([', '.join(map(str, x)) for x in query_results])
        if callback.from_user.username in text.split():
            bot.send_message(callback.message.chat.id,"Ви вже маєте розклад!Спробуйте ввести Пари,чи розклад!")
        else:
            cursor.execute('''INSERT INTO users (username)  VALUES(%s)''', (callback.from_user.username,))
            conn.commit()
            bot.send_message(callback.message.chat.id,
                             "Введіть будь ласка ваш розклад,бажано у форматі (Час-Назва-Ім'я викладача-Аудиторія)"
                             "назву пар чередувати через зап'яту-почнемо з понеділка.")
            bot.send_message(callback.message.chat.id, "Розклад для понеділка:")
            @bot.message_handler()
            def set_my_week_shedule(message):
                print(message.text)
                cursor.execute("""UPDATE users SET monday = %s WHERE username = %s""", (message.text,message.from_user.username,))
                conn.commit()
    elif callback.data == "Видалити":
        cursor.execute('''SELECT username FROM users''')
        query_results = cursor.fetchall()
        text = '\n'.join([', '.join(map(str, x)) for x in query_results])
        if not callback.from_user.username in text.split():
            bot.send_message(callback.message.chat.id,'У користувача немає розкладу,на жаль видаляти нічого!')
        else:
            cursor.execute('''DELETE FROM users WHERE username = '''+"'"+callback.from_user.username+"'")
            conn.commit()
            bot.send_message(callback.message.chat.id,'Розклад видалено')
    elif callback.data == "Змінити":
        days = telebot.types.InlineKeyboardMarkup(row_width=1)
        Monday = telebot.types.InlineKeyboardButton(text="Змінити понеділок", callback_data="Понеділок")
        Tuesday = telebot.types.InlineKeyboardButton(text="Змінити Вівторок", callback_data="Вівторок")
        Wednesday = telebot.types.InlineKeyboardButton(text="Змінити Середу", callback_data="Середа")
        Trusday = telebot.types.InlineKeyboardButton(text="Змінити Четверг", callback_data="Четверг")
        Friday = telebot.types.InlineKeyboardButton(text="Змінити П'ятницю", callback_data="П'ятниця")
        Saturday = telebot.types.InlineKeyboardButton(text="Змінити Субботу", callback_data="Суббота")
        days.add(Monday,Tuesday,Wednesday,Trusday,Friday,Saturday)
        bot.send_message(callback.message.chat.id,"Який день ви хочете змінити?",reply_markup=days,)
        return bot.callback_query_handler
    elif callback.data =="Понеділок":
        bot.send_message(callback.message.chat.id, "Введіть новий розклад для понеділка:")
    elif callback.data == "Вівторок":
        bot.send_message(callback.message.chat.id, "Введіть новий розклад для Вівторка:")
    elif callback.data =="Середа":
        bot.send_message(callback.message.chat.id, "Введіть новий розклад для Середи:")
    elif callback.data =="Четверг":
        bot.send_message(callback.message.chat.id, "Введіть новий розклад для Четверга:")
    elif callback.data =="П'ятниця":
        bot.send_message(callback.message.chat.id, "Введіть новий розклад для П'ятниці;")
    elif callback.data =="Суббота":
        bot.send_message(callback.message.chat.id, "Введіть новий розклад для Суботи:")


bot.polling(non_stop=True)
