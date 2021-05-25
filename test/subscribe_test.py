from sqlighter import SQLighter
from loguru import logger
import telebot

TOKEN = None
with open("../sweater/token.txt") as T:
	TOKEN = T.read().strip()

bot = telebot.TeleBot(TOKEN)
db1520 = SQLighter('db1520.db')

class Subscribe:
    @bot.message_handler(commands=['subscribe'])
    def subscribe(message):
        try:
            if(not db1520.subscriber_exists(message.from_user.id)):
                # если юзера нет в базе, добавляем его
                db1520.add_subscriber(message.from_user.id)
            else:
                # если он уже есть, то просто обновляем ему статус подписки
                db1520.update_subscription(message.from_user.id, True)

            bot.send_message(message.from_user.id, "Вы успешно подписались на новости Капцовки!  😝\nСкоро выйдут новые события и вы узнаете о них первыми =)")

        except:
            logger.warning("WARNING with subscribe")
            logger.error("ERROR with subscribe")
            logger.critical("CRITICAL with subscribe")