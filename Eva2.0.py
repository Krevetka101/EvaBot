import telebot

bot = telebot.TeleBot("5740263278:AAFTyI5d5q5DyT5SwiH6yfGOQHKeazR26EU")

# Обработка команды start
@bot.message_handler(commands=['start'])
def send_start(message):
	bot.reply_to(message, "Hey, what’s up?")

# Запуск бота
bot.infinity_polling()