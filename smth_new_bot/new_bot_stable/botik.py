import telebot
import sqlite3
import random as r
from telebot import types

botik = telebot.TeleBot("your bot token")

global length
lenght = 20

pw = ''
# abcsl = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# abcsu = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
# syms = ['~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']

lists = [nums]

def generator():
    global pw
    if pw == '':
        i = 1
        pw = ''
        while i <= lenght:

            pw = pw + nums[r.randint(0, len(nums) - 1)]
            i = i + 1

@botik.message_handler(commands=['start'])
def start(message):
    
    connect = sqlite3.connect('new_bot_stable/main_db_stable.db')
    cursor = connect.cursor()
    generator()
    
    global user_id
    user_id = pw
    print(f"current user_id is: {user_id}")
    cursor.execute(f"SELECT personal_id FROM users WHERE personal_id = {user_id}")
    data = cursor.fetchone()
    print(f"current data is: {data}")
    
    if data is None:
        global users_list
        users_list = [message.chat.id]
        print(f"current user_id is: {user_id}")
        botik.send_message(message.chat.id, f'Ваш ID: {user_id}' + '\nКапець, сам в шокі но я бота зробив.\nніпон пон\n/nickname [нік] - міняє ваш нік\n/find [айді] - показує профіль гравця по айді\n/delete - видаляє ваш акк разом з ніком і айді\n(якшо захочете зарегатися знов перезапустіть бота)\n/profile - показує всі ваші данні')
        cursor.execute("INSERT INTO users (personal_id) VALUES(?)", [user_id])
        connect.commit()
    else:
        botik.send_message(message.chat.id, f'Hе спамте!\n Ваш ID: {user_id}')


@botik.message_handler(commands=['nickname'])
def nickname(message):
    connect = sqlite3.connect('new_bot_stable/main_db_stable.db')
    cursor = connect.cursor()
   
    nickname_com = message.text
    nickname = nickname_com.replace("/nickname ",'')
    global user_id

    cursor.execute(f"""
        UPDATE users
        SET usernames = '{nickname}'
        WHERE personal_id = {user_id}
    """)
    connect.commit()
    botik.send_message(message.chat.id, 'ваш нік ' + nickname + "\nПриємної гри )")


@botik.message_handler(commands=['find'])
def find(message):
    connect = sqlite3.connect('new_bot_stable/main_db_stable.db')
    cursor = connect.cursor()

    search_id = message.text.replace("/find ",'')
    try:
        search_id = int(search_id)
    except:
        pass
  

    if isinstance(search_id,int) != True:
        botik.send_message(message.chat.id, "айді ж наче з чифр тільки складається 😎")
    elif isinstance(search_id,str) != True:
        cursor.execute(f"SELECT usernames FROM users WHERE personal_id = {search_id}")
        result_data = str(cursor.fetchone())
        if result_data == "None":
            botik.send_message(message.chat.id, f"по айді: {search_id}\n не знайдено жодного профілю ☹️")
        else:
            result_nick1 = result_data.replace("('", " ")
            result_nick2 = result_nick1.replace("',)", " ")

            print(result_nick2)
            connect.commit()

            botik.send_message(message.chat.id, f"по айді: {search_id} знайдено профіль:" + f"\nнік: {result_nick2}")


@botik.message_handler(commands=["delete"])
def delete(message):
    connect = sqlite3.connect('new_bot_stable/main_db_stable.db')
    cursor = connect.cursor()
    global user_id
    cursor.execute(f''' DELETE FROM users
                        WHERE personal_id = {user_id}
                    ''')
    connect.commit()
    botik.send_message(message.chat.id,"Аккаунт видалено")


@botik.message_handler(commands=["profile"])
def profile(message):

    connect = sqlite3.connect('new_bot_stable/main_db_stable.db')
    cursor = connect.cursor()

    
    cursor.execute(f"SELECT usernames FROM users WHERE personal_id = {user_id}")
    result_data = str(cursor.fetchone())

    result_nick1 = result_data.replace("('", " ")
    result_nick2 = result_nick1.replace("',)", " ")

    botik.send_message(message.chat.id, f"Ваш нік: {result_nick2}\nВаш ID: {user_id}")


botik.polling(none_stop=True)
