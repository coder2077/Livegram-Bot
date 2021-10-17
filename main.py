'''
Copyright 2021. Author Tg: @coder2077
'''

import telebot
import sqlite3
import config
from db import create_db


# Creating db file. Show db.py
create_db()
# Setting Bot
bot = telebot.TeleBot(config.TOKEN, parse_mode='Markdown')


# start command handler
@bot.message_handler(commands=['start'])
def start(message):
	chat_id = message.chat.id
	firstname = message.from_user.first_name
	conn = sqlite3.connect('users.db')
	cursor = conn.cursor()

	answer = f"Hi {firstname}!  Send your question."
	cursor.execute(f"SELECT chat_id FROM USERS WHERE chat_id = ?", (chat_id,))
	data = cursor.fetchone()
	if data:
		bot.send_message(chat_id, answer)

	else:
		bot.send_message(chat_id, answer)

		cursor.execute("INSERT INTO USERS VALUES(?, ?);", (firstname, chat_id,))
		conn.commit()

	conn.close()


# login command handler. It is for be admin. Show config.py file
@bot.message_handler(commands=['login'])
def login(message):
	chat_id = message.chat.id
	conn = sqlite3.connect('users.db')
	cursor = conn.cursor()
	cursor.execute(f"SELECT admin_id FROM ADMINS WHERE admin_id = ?", (chat_id,))
	data = cursor.fetchone()
	if data:
		bot.send_message(chat_id, f"You are already admin.")

	else:
		msg = bot.send_message(chat_id, 'Please, send me login for be admin.')
		bot.register_next_step_handler(msg, process_login_step)
	
	conn.close()


def process_login_step(message):
	chat_id = message.chat.id

	if message.text == config.LOGIN:
		msg = bot.send_message(chat_id, "Login is correct! next step, send me a security password.")
		bot.register_next_step_handler(msg, process_password_step)
	else:
		bot.send_message(chat_id, "Login is incorrect!!! \n\nFor retry, send me /login command.")


def process_password_step(message):
	conn = sqlite3.connect('users.db')
	cursor = conn.cursor()
	chat_id = message.chat.id
	name = message.from_user.first_name

	if message.text == config.PASSWORD:
		bot.send_message(chat_id, "🎉 Congratulations!  You are now admin.")
		cursor.execute("INSERT INTO ADMINS VALUES (?, ?);", (name, chat_id,))
		conn.commit()

	else:
		bot.send_message(chat_id, "Password is incorrect! \n\nFor retry, send me /login command.")

	conn.close()


# post command handler. It is for sending message to all users. For only admins
@bot.message_handler(commands=['post'])
def post(message):
	chat_id = message.chat.id
	conn = sqlite3.connect('users.db') 
	cursor = conn.cursor()

	cursor.execute("SELECT admin_id FROM ADMINS")
	datas = cursor.fetchall()
	for data in datas:
		if chat_id in data:
			answer = f"OK! Send me a message post and I will send it to all users."
			msg = bot.send_message(chat_id, answer)
			bot.register_next_step_handler(msg, process_post_step)

		else:
			bot.send_message(chat_id, "This command is only for admins! \nFor login:  /login")

	conn.close()


def process_post_step(message):
	chat_id = message.chat.id
	conn = sqlite3.connect('users.db')
	cursor = conn.cursor()

	cursor.execute("SELECT chat_id FROM USERS")
	datas = cursor.fetchall()
	for data in datas:
		for i in data:
			try:
				bot.copy_message(i, chat_id, message.message_id)

			except:
				cursor.execute("DELETE FROM USERS WHERE chat_id = ?", (chat_id,))
				conn.commit()

	conn.close()
	
# All messages handler
@bot.message_handler(func=lambda call: True)
def message_handler(message):
	chat_id = message.chat.id
	conn = sqlite3.connect('users.db')
	cursor = conn.cursor()
	cursor.execute("SELECT admin_id FROM ADMINS")
	datas = cursor.fetchall()
	for data in datas:
		if chat_id in data:
			pass
		else:
			for i in data:
				try:
					bot.forward_message(i, chat_id, message.message_id)

				except:
					pass

	if message.reply_to_message:
		try:
			bot.send_message(chat_id=message.reply_to_message.forward_from.id, text=message.text)

		except:
			pass

	conn.close()


# Saving step
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()


# Running bot with polling
bot.polling()

'''
Copyright 2021. Author Tg: @coder2077
'''