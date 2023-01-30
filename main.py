import telebot
import datetime,calendar
import psycopg2
import asyncio

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


def monday(message):
    cursor.execute('''INSERT INTO users (username,monday,user_id)  VALUES(%s,%s,%s)''',
                   (message.from_user.username,message.text,message.from_user.id))
    conn.commit()
    tuesday_message = bot.send_message(message.chat.id, 'Розклад для Вівторка:')
    bot.register_next_step_handler(tuesday_message, tuesday)


def tuesday(message):
    cursor.execute('''UPDATE users SET tuesday = %s WHERE username = %s''',
                   (message.text,message.from_user.username))
    conn.commit()
    wednesday_message = bot.send_message(message.chat.id, 'Розклад для Середи:')
    bot.register_next_step_handler(wednesday_message, wednesday)


def wednesday(message):
    cursor.execute('''UPDATE users SET wednesday = %s WHERE username = %s''',
                   (message.text, message.from_user.username))
    conn.commit()
    thursday_message = bot.send_message(message.chat.id, 'Розклад для Четверга:')
    bot.register_next_step_handler(thursday_message, thursday)


def thursday(message):
    cursor.execute('''UPDATE users SET thursday = %s WHERE username = %s''',
                   (message.text, message.from_user.username))
    conn.commit()
    thursday_message = bot.send_message(message.chat.id, "Розклад для П'ятниці:")
    bot.register_next_step_handler(thursday_message, friday)


def friday(message):
    cursor.execute('''UPDATE users SET friday = %s WHERE username = %s''',
                   (message.text, message.from_user.username))
    conn.commit()
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    answer_yes = telebot.types.InlineKeyboardButton(text="Так", callback_data="Так")
    answer_no = telebot.types.InlineKeyboardButton(text="Ні", callback_data="Ні")
    markup.add(answer_yes, answer_no)
    bot.send_message(message.chat.id, 'Чи є в тебе заняття в Субботу?', reply_markup=markup)


def saturday(message):
    cursor.execute('''UPDATE users SET saturday = %s WHERE username = %s''',
                   (message.text, message.from_user.username))
    conn.commit()
    bot.send_message(message.chat.id,"Вітаю ви завершили налаштування свого розкладу!\n Якщо бажаєте його змінити впишіть команду /start")


def update_monday(message):
    cursor.execute('''UPDATE users SET monday = %s WHERE username = %s''',
                   (message.text, message.from_user.username))
    conn.commit()


def update_tuesday(message):
    cursor.execute('''UPDATE users SET thuesday = %s WHERE username = %s''',
                   (message.text, message.from_user.username))
    conn.commit()


def update_wednesday(message):
    cursor.execute('''UPDATE users SET wednesday = %s WHERE username = %s''',
                   (message.text, message.from_user.username))
    conn.commit()


def update_thursday(message):
    cursor.execute('''UPDATE users SET thursday = %s WHERE username = %s''',
                   (message.text, message.from_user.username))
    conn.commit()


def update_friday(message):
    cursor.execute('''UPDATE users SET friday = %s WHERE username = %s''',
                   (message.text, message.from_user.username))
    conn.commit()


def update_saturday(message):
    cursor.execute('''UPDATE users SET saturday = %s WHERE username = %s''',
                   (message.text, message.from_user.username))
    conn.commit()


@bot.message_handler(commands=['Пары',])
def get_today_shedule(message):
    user_message =  message.text
    today = calendar.day_name[datetime.date.today().weekday()].lower()
    translate = {'monday':'Понеділок','tuesday':'Вівторок','wednesday':'Середа','thursday':'Четверг','Friday':"П'ятниця",'saturday':'Суббота'}
    cursor.execute("""SELECT username FROM users""")
    query_results = cursor.fetchall()
    for username in text.split():
        if username == message.from_user.username:
            bot.send_message(message.chat.id,f'your username is {username}' )
            bot.send_message(message.chat.id,f'Розклад на сьогодні({translate[today]}):')
            cursor.execute(f"SELECT {today} FROM users WHERE username = '{message.from_user.username}'")
            query_results = cursor.fetchall()
            user_shedule = '\n'.join([', '.join(map(str, x)) for x in query_results])
            bot.send_message(message.chat.id,user_shedule)


@bot.callback_query_handler(func=lambda callback: callback.data)
def shedule_answer(callback):
    if callback.data == "Створити":
        cursor.execute('''SELECT username FROM users''')
        query_results = cursor.fetchall()
        text = '\n'.join([', '.join(map(str, x)) for x in query_results])
        if callback.from_user.username in text.split():
            bot.send_message(callback.message.chat.id,"Ви вже маєте розклад!Спробуйте ввести Пари,чи розклад!")
        else:
            bot.send_message(callback.message.chat.id,
                             "Введіть будь ласка ваш розклад,бажано у форматі (Час-Назва предмету-Ім'я викладача-Аудиторія)"
                             "-почнемо з понеділка.")
            monday_message = bot.send_message(callback.message.chat.id, 'Розклад для Понеділка:')
            bot.register_next_step_handler(monday_message,monday)
            # cursor.execute(f"INSERT INTO users (monday) WHERE username = {callback.from_user.username}  VALUES(%s), 'something'")
            # conn.commit()
    elif callback.data == "Так":
        saturday_message = bot.send_message(callback.message.chat.id, 'Розклад для Субботи:')
        bot.register_next_step_handler(saturday_message, saturday)
    elif callback.data == "Ні":
        bot.send_message(callback.message.chat.id,
                         "Вітаю ви завершили налаштування свого розкладу!\n Якщо бажаєте його змінити впишіть команду /start")
    elif callback.data == "Видалити":
        cursor.execute('''SELECT username FROM users''')
        query_results = cursor.fetchall()
        text = '\n'.join([', '.join(map(str, x)) for x in query_results])
        if not callback.from_user.username in text.split():
            bot.send_message(callback.message.chat.id, 'У користувача немає розкладу,на жаль видаляти нічого!')
        else:
            cursor.execute('''DELETE FROM users WHERE username = ''' + "'" + callback.from_user.username + "'")
            conn.commit()
            bot.send_message(callback.message.chat.id, 'Розклад видалено')
    elif callback.data == "Змінити":
        days = telebot.types.InlineKeyboardMarkup(row_width=1)
        Monday = telebot.types.InlineKeyboardButton(text="Змінити понеділок", callback_data="Понеділок")
        Tuesday = telebot.types.InlineKeyboardButton(text="Змінити Вівторок", callback_data="Вівторок")
        Wednesday = telebot.types.InlineKeyboardButton(text="Змінити Середу", callback_data="Середа")
        Trusday = telebot.types.InlineKeyboardButton(text="Змінити Четверг", callback_data="Четверг")
        Friday = telebot.types.InlineKeyboardButton(text="Змінити П'ятницю", callback_data="П'ятниця")
        Saturday = telebot.types.InlineKeyboardButton(text="Змінити Субботу", callback_data="Суббота")
        days.add(Monday, Tuesday, Wednesday, Trusday, Friday, Saturday)
        bot.send_message(callback.message.chat.id, "Який день ви хочете змінити?", reply_markup=days, )
        return bot.callback_query_handler
    elif callback.data == "Понеділок":
        update_monday_message = bot.send_message(callback.message.chat.id, 'Введіть новий розклад для Понеділка:')
        bot.register_next_step_handler(update_monday_message, update_monday)
    elif callback.data == "Вівторок":
        update_tuesday_message = bot.send_message(callback.message.chat.id, 'Введіть новий розклад для Вівторка:')
        bot.register_next_step_handler(update_tuesday_message, update_tuesday)
    elif callback.data == "Середа":
        update_wednesday_message = bot.send_message(callback.message.chat.id, 'Введіть новий розклад для Середи:')
        bot.register_next_step_handler(update_wednesday_message, update_wednesday)
    elif callback.data == "Четверг":
        update_thursday_message = bot.send_message(callback.message.chat.id, 'Введіть новий розклад для Четверга:')
        bot.register_next_step_handler(update_thursday_message, update_thursday)
    elif callback.data == "П'ятниця":
        update_friday_message = bot.send_message(callback.message.chat.id, "Введіть новий розклад для П'ятниці:")
        bot.register_next_step_handler(update_friday_message, update_thursday)
    elif callback.data == "Суббота":
        update_saturday_message = bot.send_message(callback.message.chat.id, "Введіть новий розклад для Cубботи:")
        bot.register_next_step_handler(update_saturday_message, update_thursday)


bot.polling(non_stop=True)
