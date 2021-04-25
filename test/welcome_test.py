from sqlighter import SQLighter
from loguru import logger
import telebot

TOKEN = None
with open("token.txt") as T:
	TOKEN = T.read().strip()

bot = telebot.TeleBot(TOKEN)
db1520 = SQLighter('db1520.db')

@bot.message_handler(commands=['start'])
def welcome2(message):
    try:
        # keyboard
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("👀 О школе")
        item2 = types.KeyboardButton("🧑‍🏫 Расписание")
        item3 = types.KeyboardButton("🐵 Поговорим?")
        item4 = types.KeyboardButton("Связаться с...")
     
        markup.add(item1, item2, item3, item4)
     
        bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы помогать вам с информацией о школе".format(message.from_user, bot.get_me()),
            parse_mode='html', reply_markup=markup)

        if(not db1520.subscriber_exists(message.from_user.id)):
            # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
            db1520.add_subscriber(message.from_user.id, False)

        while True:
            subscriptions = db1520.get_subscriptions()

            bot.send_message(message.from_user.id, 'https://www.instagram.com/kaptsovka/?hl=ru\n{0.first_name}, загляни в инстаграм Капцовки.\nВозможно там появилось что-то интересное!'.format(message.from_user, bot.get_me()),
            parse_mode='html')

            bot.send_message(message.from_user.id, 'https://www.instagram.com/kaptsovschool/\n{0.first_name}, загляни в инстаграм Школы 1520 им. Капцовых.\nВозможно там появилось что-то интересное!'.format(message.from_user, bot.get_me()),
            parse_mode='html')

            time.sleep(172800)

    except:
        logger.warning("WARNING with welcome2")
        logger.error("ERROR with welcome2")
        logger.critical("CRITICAL with welcome2")