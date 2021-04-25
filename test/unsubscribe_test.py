from sqlighter import SQLighter
from loguru import logger
import telebot

TOKEN = None
with open("token.txt") as T:
	TOKEN = T.read().strip()

bot = telebot.TeleBot(TOKEN)
db1520 = SQLighter('db1520.db')

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    try:
        if(not db1520.subscriber_exists(message.from_user.id)):
            # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
            db1520.add_subscriber(message.from_user.id, False)
            bot.send_message(message.from_user.id, "Вы и так не подписаны.")
        else:
            # если он уже есть, то просто обновляем ему статус подписки
            db1520.update_subscription(message.from_user.id, False)
            bot.send_message(message.from_user.id, "Вы успешно отписались.")

    except:
        logger.warning("WARNING with unsubscribe")
        logger.error("ERROR with unsubscribe")
        logger.critical("CRITICAL with unsubscribe")