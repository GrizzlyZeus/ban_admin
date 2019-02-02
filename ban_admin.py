import sqlite3
import telebot
 
class DataConn:
    def __init__(self, db_name):
        self.db_name = db_name
   
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn
   
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise

bot = telebot.TeleBot("token")
 
msgid1 = bot.send_message(-1001160331786, "Бот включен.")
 
@bot.message_handler(commands=['banad'])
def pussi(msg):
	if msg.reply_to_message is not None:
		if bot.get_chat_member(msg.chat.id, msg.from_user.id).status != "member":
			with DataConn('database.db') as conn:
				cursor = conn.cursor()
				cursor.execute("INSERT INTO ban VALUES (?)", (str(msg.reply_to_message.from_user.id),))
				conn.commit()

@bot.message_handler(commands=['unbanad'])
def pussi(msg):
	if msg.reply_to_message is not None:
		if bot.get_chat_member(msg.chat.id, msg.from_user.id).status != "member":
			with DataConn('database.db') as conn:
				cursor = conn.cursor()
				cursor.execute("DELETE FROM ban WHERE id = ?", (str(msg.reply_to_message.from_user.id),))
				conn.commit()

@bot.message_handler(content_types=['text'])
def msg(msg):
	with DataConn('database.db') as conn:
		cursor = conn.cursor()
		print(msg.from_user.id)
		cursor.execute("SELECT * FROM ban WHERE id = ?", (str(msg.from_user.id),))
		row = cursor.fetchone()
		print(row)
		if row is not None:
			bot.delete_message(msg.chat.id, msg.message_id)


if __name__ == '__main__':
	bot.polling(none_stop=True)
