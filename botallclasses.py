#-*- coding: utf-8 -*-
#! /usr/bin/e# nv python

import telebot
import config
import random
import sqlite3
import time
 
from telebot import types
from loguru import logger
from sqlighter import SQLighter
from datetime import datetime

bot = telebot.TeleBot(config.TOKEN)
db1520 = SQLighter('db1520.db')

# add filemode="w" to overwrite
logger.add("bot1520log.log", format = "{time} {level} {message}", level = "WARNING", rotation = "1 week", compression = "zip")

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

# Команда отписки
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    try:
        if(not db1520.subscriber_exists(message.from_user.id)):
            # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
            db1520.add_subscriber(message.from_user.id, False)
            bot.send_message(message.from_user.id, "Вы итак не подписаны.")
        else:
            # если он уже есть, то просто обновляем ему статус подписки
            db1520.update_subscription(message.from_user.id, False)
            bot.send_message(message.from_user.id, "Вы успешно отписаны.")

    except:
        logger.warning("WARNING with unsubscribe")
        logger.error("ERROR with unsubscribe")
        logger.critical("CRITICAL with unsubscribe")

@bot.message_handler(commands=['start'])
def welcome2(message):
    try:
        # keyboard
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("👀 Что у нас за школа такая?")
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

            time.sleep(345600)

    except:
        logger.warning("WARNING with welcome2")
        logger.error("ERROR with welcome2")
        logger.critical("CRITICAL with welcome2")
 
@bot.message_handler(content_types=['text'])
def lalala(message):
    try:
        if message.chat.type == 'private':
            if message.text == '👀 Что у нас за школа такая?':
                bot.send_message(message.chat.id, "👨‍🏫 «Школа № 1520 имени Капцовых» — одно из старейших образовательных учреждений Москвы! У истоков современной школы — городское начальное училище для мальчиков имени Сергея Алексеевича Капцова, подаренное городу в мае 1892 года гласным Московской городской Думы, купцом первой гильдии, потомственным почетным гражданином, меценатом Александром Сергеевичем Капцовым в память о своем отце С. А. Капцове. Сейчас во главе нашей школы находится замечательный человек и талантливый директор\nКириченко Вита Викторовна 👏")
            elif message.text == '🧑‍🏫 Расписание':
     
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("1 класс", callback_data='1')
                item2 = types.InlineKeyboardButton("2 класс", callback_data='2')
                item3 = types.InlineKeyboardButton("3 класс", callback_data='3')
                item4 = types.InlineKeyboardButton("4 класс", callback_data='4')
                item5 = types.InlineKeyboardButton("5 класс", callback_data='5')
                item6 = types.InlineKeyboardButton("6 класс", callback_data='6')
                item7 = types.InlineKeyboardButton("7 класс", callback_data='7')
                item8 = types.InlineKeyboardButton("8 класс", callback_data='8')
                item9 = types.InlineKeyboardButton("9 класс", callback_data='9')
                item10 = types.InlineKeyboardButton("10 класс", callback_data='10')
                item11 = types.InlineKeyboardButton("11 класс", callback_data='11')
     
                markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11)

                bot.send_message(message.chat.id, "👩‍🏫 В каком вы классе?", reply_markup=markup)

            elif message.text == '🐵 Поговорим?':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("good", callback_data='good')
                item2 = types.InlineKeyboardButton("bad", callback_data='bad')

                markup.add(item1, item2)

                bot.send_message(message.chat.id, '🐻 How are you?', reply_markup=markup)

            elif message.text == 'Связаться с...':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Педагоги", callback_data='КР')
                item2 = types.InlineKeyboardButton("Зам. Директора", callback_data='АД')
                item3 = types.InlineKeyboardButton("Директор", callback_data='Д')

                markup.add(item1, item2, item3)

                bot.send_message(message.chat.id, 'Связаться с...', reply_markup=markup)

            else:
                bot.send_message(message.chat.id, '😸 Пожалуйста, нажимайте на кнопки')

    except:
        logger.warning("WARNING with lalala")
        logger.error("ERROR with lalala")
        logger.critical("CRITICAL with lalala")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == '1':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А", callback_data='a')
                item2 = types.InlineKeyboardButton("Б", callback_data='b')
                item3 = types.InlineKeyboardButton("В", callback_data='v')
                item4 = types.InlineKeyboardButton("Г", callback_data='g')
                item5 = types.InlineKeyboardButton("Д", callback_data='d')
                item6 = types.InlineKeyboardButton("Е", callback_data='e')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, '🧑‍🎓 Какая буква у вашего 1 класса?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '🧑‍🏫 Расписание',
                reply_markup=None)

            elif call.data == '2':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А", callback_data='a2')
                item2 = types.InlineKeyboardButton("Б", callback_data='b2')
                item3 = types.InlineKeyboardButton("В", callback_data='v2')
                item4 = types.InlineKeyboardButton("Г", callback_data='g2')
                item5 = types.InlineKeyboardButton("Д", callback_data='d2')
                item6 = types.InlineKeyboardButton("Е", callback_data='e2')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, '🧑‍🎓 Какая буква у вашего 2 класса?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '🧑‍🏫 Расписание',
                reply_markup=None)

            elif call.data == '3':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А", callback_data='a3')
                item2 = types.InlineKeyboardButton("Б", callback_data='b3')
                item3 = types.InlineKeyboardButton("В", callback_data='v3')
                item4 = types.InlineKeyboardButton("Г", callback_data='g3')
                item5 = types.InlineKeyboardButton("Д", callback_data='d3')
                item6 = types.InlineKeyboardButton("Е", callback_data='e3')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, '🧑‍🎓 Какая буква у вашего 3 класса?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '🧑‍🏫 Расписание',
                reply_markup=None)

            elif call.data == '4':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А", callback_data='a4')
                item2 = types.InlineKeyboardButton("Б", callback_data='b4')
                item3 = types.InlineKeyboardButton("В", callback_data='v4')
                item4 = types.InlineKeyboardButton("Г", callback_data='g4')
                item5 = types.InlineKeyboardButton("Д", callback_data='d4')
                item6 = types.InlineKeyboardButton("Е", callback_data='e4')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, '🧑‍🎓 Какая буква у вашего 4 класса?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '🧑‍🏫 Расписание',
                reply_markup=None)

            elif call.data == '5':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А", callback_data='a5')
                item2 = types.InlineKeyboardButton("Б", callback_data='b5')
                item3 = types.InlineKeyboardButton("В", callback_data='v5')
                item4 = types.InlineKeyboardButton("Г", callback_data='g5')
                item5 = types.InlineKeyboardButton("Д", callback_data='d5')
                item6 = types.InlineKeyboardButton("Е", callback_data='e5')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, '🧑‍🎓 Какая буква у вашего 5 класса?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '🧑‍🏫 Расписание',
                reply_markup=None)

            elif call.data == '6':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А", callback_data='a6')
                item2 = types.InlineKeyboardButton("Б", callback_data='b6')
                item3 = types.InlineKeyboardButton("В", callback_data='v6')
                item4 = types.InlineKeyboardButton("Г", callback_data='g6')
                item5 = types.InlineKeyboardButton("Д", callback_data='d6')
                item6 = types.InlineKeyboardButton("Е", callback_data='e6')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, '🧑‍🎓 Какая буква у вашего 6 класса?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '🧑‍🏫 Расписание',
                reply_markup=None)

            elif call.data == '7':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А", callback_data='a7')
                item2 = types.InlineKeyboardButton("Б", callback_data='b7')
                item3 = types.InlineKeyboardButton("В", callback_data='v7')
                item4 = types.InlineKeyboardButton("Г", callback_data='g7')
                item5 = types.InlineKeyboardButton("Д", callback_data='d7')
                item6 = types.InlineKeyboardButton("Е", callback_data='e7')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, '🧑‍🎓 Какая буква у вашего 7 класса?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '🧑‍🏫 Расписание',
                reply_markup=None)

            elif call.data == '8':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А", callback_data='a8')
                item2 = types.InlineKeyboardButton("Б", callback_data='b8')
                item3 = types.InlineKeyboardButton("В", callback_data='v8')
                item4 = types.InlineKeyboardButton("Г", callback_data='g8')
                item5 = types.InlineKeyboardButton("Д", callback_data='d8')
                item6 = types.InlineKeyboardButton("Е", callback_data='e8')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, '🧑‍🎓 Какая буква у вашего 8 класса?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '🧑‍🏫 Расписание',
                reply_markup=None)

            elif call.data == '9':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А", callback_data='a9')
                item2 = types.InlineKeyboardButton("Б", callback_data='b9')
                item3 = types.InlineKeyboardButton("В", callback_data='v9')
                item4 = types.InlineKeyboardButton("Г", callback_data='g9')
                item5 = types.InlineKeyboardButton("Д", callback_data='d9')
                item6 = types.InlineKeyboardButton("Е", callback_data='e9')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, '🧑‍🎓 Какая буква у вашего 9 класса?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '🧑‍🏫 Расписание',
                reply_markup=None)

            elif call.data == '10':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А", callback_data='a10')
                item2 = types.InlineKeyboardButton("Б", callback_data='b10')
                item3 = types.InlineKeyboardButton("В", callback_data='v10')
                item4 = types.InlineKeyboardButton("Г", callback_data='g10')
                item5 = types.InlineKeyboardButton("Д", callback_data='d10')
                item6 = types.InlineKeyboardButton("Е", callback_data='e10')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, '🧑‍🎓 Какая буква у вашего 10 класса?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '🧑‍🏫 Расписание',
                reply_markup=None)

            elif call.data == '11':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А", callback_data='a11')
                item2 = types.InlineKeyboardButton("Б", callback_data='b11')
                item3 = types.InlineKeyboardButton("В", callback_data='v11')
                item4 = types.InlineKeyboardButton("Г", callback_data='g11')
                item5 = types.InlineKeyboardButton("Д", callback_data='d11')
                item6 = types.InlineKeyboardButton("Е", callback_data='e11')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, '🧑‍🎓 Какая буква у вашего 11 класса?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '🧑‍🏫 Расписание',
                reply_markup=None)

            elif call.data == 'a':

                    a = open("1class/rasp_1a.pdf", "rb")
                    bot.send_document(call.message.chat.id, a)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'b':
                    
                    b = open("1class/rasp_1b.pdf", "rb")
                    bot.send_document(call.message.chat.id, b)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'v':

                    v = open("1class/rasp_1v.pdf", "rb")
                    bot.send_document(call.message.chat.id, v)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)
                    
            elif call.data == 'g':

                    g = open("1class/rasp_1g.pdf", "rb")
                    bot.send_document(call.message.chat.id, g)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'd':
                    
                    d = open("1class/rasp_1d.pdf", "rb")
                    bot.send_document(call.message.chat.id, d)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'e':
                    
                    e = open("1class/rasp_1e.pdf", "rb")
                    bot.send_document(call.message.chat.id, e)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'a2':

                    a = open("2class/rasp_2a.pdf", "rb")
                    bot.send_document(call.message.chat.id, a)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'b2':
                    
                    b = open("2class/rasp_2b.pdf", "rb")
                    bot.send_document(call.message.chat.id, b)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'v2':

                    v = open("2class/rasp_2v.pdf", "rb")
                    bot.send_document(call.message.chat.id, v)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)
                    
            elif call.data == 'g2':

                    g = open("2class/rasp_2g.pdf", "rb")
                    bot.send_document(call.message.chat.id, g)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'd2':
                    
                    d = open("2class/rasp_2d.pdf", "rb")
                    bot.send_document(call.message.chat.id, d)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'e2':
                    
                    e = open("2class/rasp_2e.pdf", "rb")
                    bot.send_document(call.message.chat.id, e)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'a3':

                    a = open("3class/rasp_3a.pdf", "rb")
                    bot.send_document(call.message.chat.id, a)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'b3':
                    
                    b = open("3class/rasp_3b.pdf", "rb")
                    bot.send_document(call.message.chat.id, b)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'v3':

                    v = open("3class/rasp_3v.pdf", "rb")
                    bot.send_document(call.message.chat.id, v)
                    
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)
                    
            elif call.data == 'g3':

                    g = open("3class/rasp_3g.pdf", "rb")
                    bot.send_document(call.message.chat.id, g)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'd3':
                    
                    d = open("3class/rasp_3d.pdf", "rb")
                    bot.send_document(call.message.chat.id, d)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'e3':
                    
                    e = open("3class/rasp_3e.pdf", "rb")
                    bot.send_document(call.message.chat.id, e)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'a4':

                    a = open("4class/rasp_4a.pdf", "rb")
                    bot.send_document(call.message.chat.id, a)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'b4':
                    
                    b = open("4class/rasp_4b.pdf", "rb")
                    bot.send_document(call.message.chat.id, b)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'v4':

                    v = open("4class/rasp_4v.pdf", "rb")
                    bot.send_document(call.message.chat.id, v)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)
                    
            elif call.data == 'g4':

                    g = open("4class/rasp_4g.pdf", "rb")
                    bot.send_document(call.message.chat.id, g)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'd4':
                    
                    d = open("4class/rasp_4d.pdf", "rb")
                    bot.send_document(call.message.chat.id, d)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'e4':
                    
                    e = open("4class/rasp_4e.pdf", "rb")
                    bot.send_document(call.message.chat.id, e)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'a5':

                    a = open("5class/rasp_5a2.pdf", "rb")
                    bot.send_document(call.message.chat.id, a)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'b5':
                    
                    b = open("5class/rasp_5b3.pdf", "rb")
                    bot.send_document(call.message.chat.id, b)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'v5':

                    v = open("5class/rasp_5v1.pdf", "rb")
                    bot.send_document(call.message.chat.id, v)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)
                    
            elif call.data == 'g5':

                    g = open("5class/rasp_5g1.pdf", "rb")
                    bot.send_document(call.message.chat.id, g)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'd5':
                    
                    d = open("5class/rasp_5d3.pdf", "rb")
                    bot.send_document(call.message.chat.id, d)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'e5':
                    
                    e = open("5class/rasp_5e3.pdf", "rb")
                    bot.send_document(call.message.chat.id, e)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'a6':

                    a = open("6class/rasp_6a2.pdf", "rb")
                    bot.send_document(call.message.chat.id, a)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'b6':
                    
                    b = open("6class/rasp_6b1.pdf", "rb")
                    bot.send_document(call.message.chat.id, b)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'v6':

                    v = open("6class/rasp_6v1.pdf", "rb")
                    bot.send_document(call.message.chat.id, v)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)
                    
            elif call.data == 'g6':

                    g = open("6class/rasp_6g.pdf", "rb")
                    bot.send_document(call.message.chat.id, g)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'd6':
                    
                    d = open("6class/rasp_6d1.pdf", "rb")
                    bot.send_document(call.message.chat.id, d)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'e6':
                    
                    e = open("6class/rasp_6e2.pdf", "rb")
                    bot.send_document(call.message.chat.id, e)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'a7':

                    a = open("7class/rasp_7a1.pdf", "rb")
                    bot.send_document(call.message.chat.id, a)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'b7':
                    
                    b = open("7class/rasp_7b1.pdf", "rb")
                    bot.send_document(call.message.chat.id, b)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'v7':

                    v = open("7class/rasp_7v1.pdf", "rb")
                    bot.send_document(call.message.chat.id, v)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)
                    
            elif call.data == 'g7':

                    g = open("7class/rasp_7g1.pdf", "rb")
                    bot.send_document(call.message.chat.id, g)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'd7':
                    
                    d = open("7class/rasp_7d1.pdf", "rb")
                    bot.send_document(call.message.chat.id, d)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'e7':
                    
                    e = open("7class/rasp_7e1.pdf", "rb")
                    bot.send_document(call.message.chat.id, e)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'a8':

                    a = open("8class/rasp_8a1.pdf", "rb")
                    bot.send_document(call.message.chat.id, a)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'b8':
                    
                    b = open("8class/rasp_8b1.pdf", "rb")
                    bot.send_document(call.message.chat.id, b)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'v8':

                    v = open("8class/rasp_8v1.pdf", "rb")
                    bot.send_document(call.message.chat.id, v)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)
                    
            elif call.data == 'g8':

                    g = open("8class/rasp_8g1.pdf", "rb")
                    bot.send_document(call.message.chat.id, g)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'd8':
                    
                    d = open("8class/rasp_8d1.pdf", "rb")
                    bot.send_document(call.message.chat.id, d)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'e8':
                    
                    e = open("8class/rasp_8e1.pdf", "rb")
                    bot.send_document(call.message.chat.id, e)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'a9':

                    a = open("9class/rasp_9a2.pdf", "rb")
                    bot.send_document(call.message.chat.id, a)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'b9':
                    
                    b = open("9class/rasp_9b2.pdf", "rb")
                    bot.send_document(call.message.chat.id, b)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'v9':

                    v = open("9class/rasp_9v2.pdf", "rb")
                    bot.send_document(call.message.chat.id, v)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)
                    
            elif call.data == 'g9':

                    g = open("9class/rasp_9g2.pdf", "rb")
                    bot.send_document(call.message.chat.id, g)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'd9':
                    
                    d = open("9class/rasp_9d2.pdf", "rb")
                    bot.send_document(call.message.chat.id, d)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'e9':
                    
                    e = open("9class/rasp_9e1.pdf", "rb")
                    bot.send_document(call.message.chat.id, e)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'a10':

                    a = open("10class/rasp_10a1.pdf", "rb")
                    bot.send_document(call.message.chat.id, a)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'b10':
                    
                    b = open("10class/rasp_10b1.pdf", "rb")
                    bot.send_document(call.message.chat.id, b)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'v10':

                    v = open("10class/rasp_10v1.pdf", "rb")
                    bot.send_document(call.message.chat.id, v)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)
                    
            elif call.data == 'g10':

                    g = open("10class/rasp_10g1.pdf", "rb")
                    bot.send_document(call.message.chat.id, g)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'd10':
                    
                    d = open("10class/rasp_10d1.pdf", "rb")
                    bot.send_document(call.message.chat.id, d)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'e10':
                    
                    e = open("10class/rasp_10e1.pdf", "rb")
                    bot.send_document(call.message.chat.id, e)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'a11':

                    a = open("11class/rasp_11a1.pdf", "rb")
                    bot.send_document(call.message.chat.id, a)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'b11':
                    
                    b = open("11class/rasp_11b1.pdf", "rb")
                    bot.send_document(call.message.chat.id, b)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'v11':

                    v = open("11class/rasp_11v1.pdf", "rb")
                    bot.send_document(call.message.chat.id, v)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)
                    
            elif call.data == 'g11':

                    g = open("11class/rasp_11g1.pdf", "rb")
                    bot.send_document(call.message.chat.id, g)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'd11':
                    
                    d = open("11class/rasp_11d1.pdf", "rb")
                    bot.send_document(call.message.chat.id, d)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)

            elif call.data == 'e11':
                    
                    e = open("11class/rasp_11e1.pdf", "rb")
                    bot.send_document(call.message.chat.id, e)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🧑‍🏫 Вот ваше расписание",
                        reply_markup=None)                    
    
            elif call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🐻 How are you?",
                reply_markup=None)

            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🐻 How are you?",
                reply_markup=None)

            elif call.data == 'Д':
                bot.send_message(call.message.chat.id, '1.Директор\n2.+7(495)800-15-20 или +7(916)541-58-01\nПочта: KirichenkoVV@edu.mos.ru', parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Кириченко Вита Викторовна",
                reply_markup=None)

            elif call.data == 'АД':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А.Ю.Комаров", callback_data='auk')
                item2 = types.InlineKeyboardButton("М.В.Веревкина", callback_data='mvv')
                item3 = types.InlineKeyboardButton("М.Ю.Петрик", callback_data='mup')
                item4 = types.InlineKeyboardButton("Ю.А.Михалев", callback_data='uam')

                markup.add(item1, item2, item3, item4)

                bot.send_message(call.message.chat.id, 'С кем хотите связаться?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Связаться с...",
                reply_markup=None)

            elif call.data == 'auk':
                bot.send_message(call.message.chat.id, '1.Первый заместитель директора\n2.+7(495)800-15-20 доб 3006\nПочта: a.komarov@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Комаров Александр Юрьевич",
                reply_markup=None)

            elif call.data == 'mvv':
                bot.send_message(call.message.chat.id, '1.Заместитель директора по содержанию образования\n2.+7(495)800-15-20 доб 2110\nПочта: m.verevkina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Веревкина Марина Викторовна",
                reply_markup=None)

            elif call.data == 'mup':
                bot.send_message(call.message.chat.id, '1.Заместитель директора по оценке качества образования\n2.+7(495)800-15-20 доб 2111\nПочта: m.petrik@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Петрик Максим Юрьевич",
                reply_markup=None)

            elif call.data == 'uam':
                bot.send_message(call.message.chat.id, '1.Заместитель директора по воспитанию и социализации\n2.+7(495)800-15-20 доб 2103\nПочта: y.mihalev@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Михалев Юрий Анатольевич",
                reply_markup=None)

            elif call.data == 'КР':
                markup = types.InlineKeyboardMarkup(row_width=3)
                item1 = types.InlineKeyboardButton("Рус. Яз.", callback_data='rus')
                item2 = types.InlineKeyboardButton("Математика", callback_data='mat')
                item3 = types.InlineKeyboardButton("Англ. Яз.", callback_data='eng')
                item4 = types.InlineKeyboardButton("Нем. Яз.", callback_data='ger')
                item5 = types.InlineKeyboardButton("Франц. Яз.", callback_data='fren')
                item6 = types.InlineKeyboardButton("Биология", callback_data='bio')
                item7 = types.InlineKeyboardButton("Физика", callback_data='phys')
                item8 = types.InlineKeyboardButton("История", callback_data='hist')
                item9 = types.InlineKeyboardButton("Обществ.", callback_data='soc')
                item10 = types.InlineKeyboardButton("Физк-ра", callback_data='physk')
                item11 = types.InlineKeyboardButton("География", callback_data='geo')
                item12 = types.InlineKeyboardButton("Музыка", callback_data='mus')
                item13 = types.InlineKeyboardButton("Информат.", callback_data='info')
                item14 = types.InlineKeyboardButton("Химия", callback_data='chem')
                item15 = types.InlineKeyboardButton("ОБЖ", callback_data='obj')
                item16 = types.InlineKeyboardButton("Нач. Классы", callback_data='startclass')
                item17 = types.InlineKeyboardButton("Доп. обр.", callback_data='moreclass')

                markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13, item14, item15, item16, item17)

                bot.send_message(call.message.chat.id, 'Какой предмет преподает нужный вам учитель?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Связаться с...",
                reply_markup=None)

            elif call.data == 'rus':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А.Н. Бабич", callback_data='bab')
                item2 = types.InlineKeyboardButton("П.А. Гармаш", callback_data='garm')
                item3 = types.InlineKeyboardButton("С.А. Дьякова", callback_data='diak')
                item4 = types.InlineKeyboardButton("О.В. Зырянова", callback_data='zyr')
                item5 = types.InlineKeyboardButton("Е.К. Иванова", callback_data='ivan')
                item6 = types.InlineKeyboardButton("Е.С. Каримова", callback_data='kar')
                item7 = types.InlineKeyboardButton("И.Л. Перевозчикова", callback_data='perev')
                item8 = types.InlineKeyboardButton("А.Н. Попова", callback_data='pop')
                item9 = types.InlineKeyboardButton("М.А. Черушева", callback_data='cheru')

                markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)

                bot.send_message(call.message.chat.id, 'Какой учитель?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какой предмет?",
                reply_markup=None)

            elif call.data == 'bab':
                bot.send_message(call.message.chat.id, '1.Учитель Русского языка и Литературы\nПочта: a.babich@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Бабич Алексей Николаевич",
                reply_markup=None)

            elif call.data == 'garm':
                bot.send_message(call.message.chat.id, '1.Учитель Русского языка и Литературы\nПочта: p.garmash@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Гармаш Полина Александровна",
                reply_markup=None)

            elif call.data == 'diak':
                bot.send_message(call.message.chat.id, '1.Учитель Русского языка и Литературы\nПочта: s.dyakova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Дьякова Светлана Анатольевна",
                reply_markup=None)

            elif call.data == 'zyr':
                bot.send_message(call.message.chat.id, '1.Учитель Русского языка и Литературы\nПочта: o.zyryanova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Зырянова Ольга Владимировна",
                reply_markup=None)

            elif call.data == 'ivan':
                bot.send_message(call.message.chat.id, '1.Учитель Русского языка и Литературы\nПочта: e.ivanova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Иванова Елена Константиновна",
                reply_markup=None)

            elif call.data == 'kar':
                bot.send_message(call.message.chat.id, '1.Учитель Русского языка и Литературы\nПочта: e.karimova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Каримова Елена Сергеевна",
                reply_markup=None)

            elif call.data == 'perev':
                bot.send_message(call.message.chat.id, '1.Учитель Русского языка и Литературы\nПочта: i.perevozchikova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Перевозчикова Ирина Людвиговна",
                reply_markup=None)

            elif call.data == 'pop':
                bot.send_message(call.message.chat.id, '1.Учитель Русского языка и Литературы\nПочта: a.popova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Попова Альбина Назиповна",
                reply_markup=None)

            elif call.data == 'cheru':
                bot.send_message(call.message.chat.id, '1.Учитель Русского языка и Литературы\nПочта: m.cherusheva@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Черушева Мария Александровна",
                reply_markup=None)

            elif call.data == 'mat':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("И.Ю. Ананьева", callback_data='anan')
                item2 = types.InlineKeyboardButton("Т.В. Веденькина", callback_data='veden')
                item3 = types.InlineKeyboardButton("А.В. Доронин", callback_data='doron')
                item4 = types.InlineKeyboardButton("О.А. Дробот", callback_data='drobot')
                item5 = types.InlineKeyboardButton("Е.Г. Козлова", callback_data='kozl')
                item6 = types.InlineKeyboardButton("П.Н. Пронин", callback_data='pron')
                item7 = types.InlineKeyboardButton("И.А. Романова", callback_data='roman')
                item8 = types.InlineKeyboardButton("М.А. Цыбанов", callback_data='tsyban')
                item9 = types.InlineKeyboardButton("Т.Г. Шигина", callback_data='shig')
                item10 = types.InlineKeyboardButton("Д.П. Якушкина", callback_data='yakushk')

                markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)

                bot.send_message(call.message.chat.id, 'Какой учитель?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какой предмет?",
                reply_markup=None)

            elif call.data == 'anan':
                bot.send_message(call.message.chat.id, '1.Учитель Математики\nПочта: i.ananyeva@1520edu.ru',
               parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ананьева Ирина Юрьевна",
                reply_markup=None)

            elif call.data == 'veden':
                bot.send_message(call.message.chat.id, '1.Учитель Математики\nПочта: t.vedenkina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Веденькина Татьяна Юрьевна",
                reply_markup=None)

            elif call.data == 'doron':
                bot.send_message(call.message.chat.id, '1.Учитель Математики\nПочта: a.doronin@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Доронин Алексей Владимирович",
                reply_markup=None)

            elif call.data == 'drobot':
                bot.send_message(call.message.chat.id, '1.Учитель Математики\nПочта: o.drobot@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Дробот Ольга Алексеевна",
                reply_markup=None)

            elif call.data == 'kozl':
                bot.send_message(call.message.chat.id, '1.Учитель Математики\nПочта: e.kozlova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Козлова Екатерина Геннадьевна",
                reply_markup=None)

            elif call.data == 'pron':
                bot.send_message(call.message.chat.id, '1.Учитель Математики\nПочта: p.pronin@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пронин Петр Николоевич",
                reply_markup=None)

            elif call.data == 'roman':
                bot.send_message(call.message.chat.id, '1.Учитель Математики\nПочта: i.romanova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Романова Ирина Александровна",
                reply_markup=None)

            elif call.data == 'tsyban':
                bot.send_message(call.message.chat.id, '1.Учитель Математики\nПочта: m.tsybanov@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Цыбанов Максим Александрович",
                reply_markup=None)

            elif call.data == 'shig':
                bot.send_message(call.message.chat.id, '1.Учитель Математики\nПочта: t.shigina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Шигина Татьяна Геннадьевна",
                reply_markup=None)

            elif call.data == 'yakushk':
                bot.send_message(call.message.chat.id, '1.Учитель Математики\nПочта: d.yakushkina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Якушкина Дарья Павловна",
                        reply_markup=None)

            elif call.data == 'eng':
                markup = types.InlineKeyboardMarkup(row_width=2)

                item1 = types.InlineKeyboardButton("М.А. Богданова", callback_data='bogdan')
                item2 = types.InlineKeyboardButton("Е.Н. Бондарева", callback_data='bondar')
                item3 = types.InlineKeyboardButton("Е.Ю. Вавилова", callback_data='vavil')
                item4 = types.InlineKeyboardButton("И.Л. Вигдорович", callback_data='vigdor')
                item5 = types.InlineKeyboardButton("С.С. Гаврик", callback_data='gavrik')
                item6 = types.InlineKeyboardButton("О.В. Геринг", callback_data='gering')
                item7 = types.InlineKeyboardButton("И.В. Громов", callback_data='grom')
                item8 = types.InlineKeyboardButton("Е.Э. Ермолаева", callback_data='ermol')
                item9 = types.InlineKeyboardButton("М.В. Жаркова", callback_data='zhark')
                item10 = types.InlineKeyboardButton("А.А. Заварзина", callback_data='zavar')
                item11 = types.InlineKeyboardButton("З.А. Кузикян", callback_data='kuzik')
                item12 = types.InlineKeyboardButton("И.Н. Леонтьева", callback_data='leon')
                item13 = types.InlineKeyboardButton("Е.Ю. Лецис", callback_data='lezis')
                item14 = types.InlineKeyboardButton("Е.С. Луткова", callback_data='lutkova')
                item15 = types.InlineKeyboardButton("А.А. Максименко", callback_data='maximenko')
                item16 = types.InlineKeyboardButton("Л.М. Милованова", callback_data='milov')
                item17 = types.InlineKeyboardButton("Ю.Б. Мукосеева", callback_data='mukos')
                item18 = types.InlineKeyboardButton("Е.В. Муштаева", callback_data='musht')
                item19 = types.InlineKeyboardButton("Е.А. Нелюбина", callback_data='nelub')
                item20 = types.InlineKeyboardButton("К.А. Петросян", callback_data='petros')
                item21 = types.InlineKeyboardButton("А.А. Сергеева", callback_data='sergeeva')
                item22 = types.InlineKeyboardButton("Т.Г. Сокольская", callback_data='sokol')
                item23 = types.InlineKeyboardButton("Д.С. Чернобродова", callback_data='chernoborod')
                item24 = types.InlineKeyboardButton("Т.С. Ширяева", callback_data='shir')

                markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13, item14, item15, item16, item17, item18, item19, item20, item21, item22, item23, item24) 
                bot.send_message(call.message.chat.id, 'Какой учитель?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какой предмет?",
                reply_markup=None)

            elif call.data == 'bogdan':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: m.bogdanova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Богданова Мария Алексеевна",
                reply_markup=None)

            elif call.data == 'bondar':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: e.bondareva@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Бондарева Екатерина Николаевна",
                reply_markup=None)

            elif call.data == 'vavil':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: e.vavilova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вавилова Екатерина Юрьевна",
                reply_markup=None)

            elif call.data == 'vigdor':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: i.vigdorovich@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вигдорович Ирина Лазаревна",
                reply_markup=None)

            elif call.data == 'gavrik':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: s.gavrik@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Гаврик Светлана Сергеевна",
                reply_markup=None)

            elif call.data == 'gering':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: o.gering@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Геринг Ольга Владимировна",
                reply_markup=None)

            elif call.data == 'grom':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: i.gromov@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Громов Илья Валерьевич",
                reply_markup=None)

            elif call.data == 'ermol':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: e.ermolaeva@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ермолаева Елизавета Эдуардовна",
                reply_markup=None)

            elif call.data == 'zhark':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: m.zharkova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Жаркова Марина Викторовна",
                reply_markup=None)

            elif call.data == 'zavar':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: a.zavarzina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Заварзина Анна Александровна",
                reply_markup=None)

            elif call.data == 'kuzik':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: z.kuzikyan@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Кузикян Зара Ахметовна",
                reply_markup=None)

            elif call.data == 'leon':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: i.leonteva@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Леонтьева Ирина Николаевна",
                reply_markup=None)

            elif call.data == 'lezis':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: e.letsis@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Лецис Елена Юрьевна",
                reply_markup=None)

            elif call.data == 'lutkova':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: e.lutkova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Луткова Елена Сергеевна",
                reply_markup=None)

            elif call.data == 'maximenko':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: a.maximenko@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Максименко Анжелика Андреевна",
                reply_markup=None)

            elif call.data == 'milov':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: l.milovanova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Милованова Людмила Михайловна",
                reply_markup=None)

            elif call.data == 'mukos':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: y.mukoseeva@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Мукосеева Юлия Борисовна",
                reply_markup=None)

            elif call.data == 'musht':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: e.mushtaeva@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Муштаева Елена Витальевна",
                reply_markup=None)

            elif call.data == 'nelub':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: e.neliubina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Нелюбина Елена Александровна",
                reply_markup=None)

            elif call.data == 'petros':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: k.petrosyan@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Петросян Кристина Арменовна",
                reply_markup=None)

            elif call.data == 'sergeeva':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: a.sergeeva@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Сергеева Анна Александровна",
                reply_markup=None)

            elif call.data == 'sokol':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: t.sokolskaya@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Сокольская Татьяна Геннадьевна",
                reply_markup=None)

            elif call.data == 'chernoborod':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: d.chernobrodova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Чернобродова Дарья Сергеевна",
                reply_markup=None)

            elif call.data == 'shir':
                bot.send_message(call.message.chat.id, '1.Учитель Английского\nПочта: t.shiryaeva@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ширяева Татьяна Сергеевна",
                reply_markup=None)

            elif call.data == 'ger':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Е.Н. Громыхина", callback_data='gromyh')
                item2 = types.InlineKeyboardButton("О.Е. Мурзина", callback_data='murz')
                item3 = types.InlineKeyboardButton("С.Е. Якимов", callback_data='yakim')
                item4 = types.InlineKeyboardButton("А.Ю. Яцина", callback_data='yatsyna')

                markup.add(item1, item2, item3, item4)

                bot.send_message(call.message.chat.id, 'Какой учитель?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какой предмет?",
                reply_markup=None)

            elif call.data == 'gromyh':
                bot.send_message(call.message.chat.id, '1.Учитель Немецкого\nПочта: e.gromykhina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Громыхина Елена Николаевна",
                reply_markup=None)

            elif call.data == 'murz':
                bot.send_message(call.message.chat.id, '1.Учитель Немецкого\nПочта: o.murzina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Мурзина Ольга Евгеньевна",
                reply_markup=None)

            elif call.data == 'yakim':
                bot.send_message(call.message.chat.id, '1.Учитель Немецкого\nПочта: s.jakimov@1520edu.ru',
                parse_mode='html')
                
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Якимов Сергей Евгеньевич",
                reply_markup=None)

            elif call.data == 'yatsyna':
                bot.send_message(call.message.chat.id, '1.Учитель Немецкого\nПочта: a.yatsina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Яцина Анна Юрьевна",
                reply_markup=None)

            elif call.data == 'fren':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Н.С. Артемова", callback_data='artemova')
                item2 = types.InlineKeyboardButton("А.В. Воронина", callback_data='voronina')
                item3 = types.InlineKeyboardButton("М.Ю. Гранова", callback_data='granova')
                item4 = types.InlineKeyboardButton("Ю.А. Назарова", callback_data='nazarova')
                item5 = types.InlineKeyboardButton("Т.М. Неклюдова", callback_data='nekludova')

                markup.add(item1, item2, item3, item4, item5)

                bot.send_message(call.message.chat.id, 'Какой учитель?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какой предмет?",
                reply_markup=None)

            elif call.data == 'artemova':
                bot.send_message(call.message.chat.id, '1.Учитель Французского\nПочта: n.artemova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Артемова Наталья Сергеевна",
                reply_markup=None)

            elif call.data == 'voronina':
                bot.send_message(call.message.chat.id, '1.Учитель Французского\nПочта: a.voronina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Воронина Анна Владиславовна",
                reply_markup=None)

            elif call.data == 'granova':
                bot.send_message(call.message.chat.id, '1.Учитель Французского\nПочта: m.granova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Гранова Марина Юрьевна",
                reply_markup=None)

            elif call.data == 'nazarova':
                bot.send_message(call.message.chat.id, '1.Учитель Французского\nПочта: yu.nazarova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Назарова Юлия Александровна",
                reply_markup=None)

            elif call.data == 'nekludova':
                bot.send_message(call.message.chat.id, '1.Учитель Французского\nПочта: t.nekludova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Неклюдова Татьяна Макаровна",
                reply_markup=None)

            elif call.data == 'bio':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Е.Н. Амосова", callback_data='amosova')
                item2 = types.InlineKeyboardButton("К.С. Москвитина", callback_data='moskvitina')
                item3 = types.InlineKeyboardButton("Е.А. Новикова", callback_data='novikova')
                item4 = types.InlineKeyboardButton("Д.А. Соловков", callback_data='solovkov')

                markup.add(item1, item2, item3, item4)

                bot.send_message(call.message.chat.id, 'Какой учитель?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какой предмет?",
                reply_markup=None)

            elif call.data == 'amosova':
                bot.send_message(call.message.chat.id, '1.Учитель Биологии\nПочта: e.amosova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Амосова Евгения Николаевна",
                reply_markup=None)

            elif call.data == 'moskvitina':
                bot.send_message(call.message.chat.id, '1.Учитель Биологии\nПочта: k.moskvitina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Москвитина Ксения Сергеевна",
                reply_markup=None)

            elif call.data == 'novikova':
                bot.send_message(call.message.chat.id, '1.Учитель Биологии\nПочта: e.novikova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Новикова Елена Александровна",
                reply_markup=None)

            elif call.data == 'solovkov':
                bot.send_message(call.message.chat.id, '1.Учитель Биологии\nПочта: d.solovkov@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Соловков Дмитрий Андреевич",
                reply_markup=None)

            elif call.data == 'phys':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("А.А. Барат", callback_data='barat')
                item2 = types.InlineKeyboardButton("О.Г. Гладченко", callback_data='gladchenko')

                markup.add(item1, item2)

                bot.send_message(call.message.chat.id, 'Какой учитель?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какой предмет?",
                reply_markup=None)

            elif call.data == 'barat':
                bot.send_message(call.message.chat.id, '1.Учитель Физики\nПочта: a.barat@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Барат Артем Александрович",
                reply_markup=None)

            elif call.data == 'gladchenko':
                bot.send_message(call.message.chat.id, '1.Учитель Физики\nПочта: o.gladchenko@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Гладченко Ольга Геннадиевна",
                reply_markup=None)

            elif call.data == 'hist':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Н.С. Барскова", callback_data='barskova')
                item2 = types.InlineKeyboardButton("С.В. Дмитриева", callback_data='dmitrieva')
                item3 = types.InlineKeyboardButton("А.П. Липовская", callback_data='lipovskaya')
                item4 = types.InlineKeyboardButton("С.В. Погорелова", callback_data='pogorelova')
                item5 = types.InlineKeyboardButton("С.В. Фильченкова", callback_data='filchenkova')
                item6 = types.InlineKeyboardButton("К.И. Фрейзе", callback_data='freize')
                item7 = types.InlineKeyboardButton("Т.В. Черкашина", callback_data='cherkashina')

                markup.add(item1, item2, item3, item4, item5, item6, item7)

                bot.send_message(call.message.chat.id, 'Какой учитель?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какой предмет?",
                reply_markup=None)

            elif call.data == 'barskova':
                bot.send_message(call.message.chat.id, '1.Учитель Истории\nПочта: n.barskova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Барскова Наталья Станиславовна",
                reply_markup=None)

            elif call.data == 'dmitrieva':
                bot.send_message(call.message.chat.id, '1.Учитель Истории и Обществознания\nПочта: s.dmitrieva@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Дмитриева Светлана Викторовна",
                reply_markup=None)

            elif call.data == 'lipovskaya':
                bot.send_message(call.message.chat.id, '1.Учитель Истории и Обществознания\nПочта: a.lipovskaya@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Липовская Анастасия Петровна",
                reply_markup=None)

            elif call.data == 'pogorelova':
                bot.send_message(call.message.chat.id, '1.Учитель Истории и Обществознания\nПочта: s.pogorelova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Погорелова Светлана Викторовна",
                reply_markup=None)

            elif call.data == 'filchenkova':
                bot.send_message(call.message.chat.id, '1.Учитель Истории\nПочта: s.filchenkova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Фильченкова Светлана Викторовна",
                reply_markup=None)

            elif call.data == 'freize':
                bot.send_message(call.message.chat.id, '1.Учитель Истории\nПочта: k.freize@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Фрейзе Константин Игоревич",
                reply_markup=None)

            elif call.data == 'cherkashina':
                bot.send_message(call.message.chat.id, '1.Учитель Истории и Обществознания\nПочта: t.cherkashina@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Черкашина Татьяна Владимировна",
                reply_markup=None)

            elif call.data == 'soc':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("С.В. Дмитриева", callback_data='dmitrieva')
                item2 = types.InlineKeyboardButton("А.П. Липовская", callback_data='lipovskaya')
                item3 = types.InlineKeyboardButton("С.В. Погорелова", callback_data='pogorelova')
                item4 = types.InlineKeyboardButton("Т.В. Черкашина", callback_data='cherkashina')

                markup.add(item1, item2, item3, item4)

                bot.send_message(call.message.chat.id, 'Какой учитель?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какой предмет?",
                reply_markup=None)

            elif call.data == 'physk':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("И.Ю. Кирдяшова", callback_data='kirdyashova')
                item2 = types.InlineKeyboardButton("Ю.Н. Михальчук", callback_data='michalchuk')
                item3 = types.InlineKeyboardButton("А.М. Мягков", callback_data='myagkov')
                item4 = types.InlineKeyboardButton("С.В. Нестеров", callback_data='nesterov')
                item5 = types.InlineKeyboardButton("В.В. Толстов", callback_data='tolstov')

                markup.add(item1, item2, item3, item4, item5)

                bot.send_message(call.message.chat.id, 'Какой учитель?', reply_markup=markup)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какой предмет?",
                reply_markup=None)

            elif call.data == 'kirdyashova':
                bot.send_message(call.message.chat.id, '1.Учитель Физкультуры\nПочта: i.kirdyashova@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Кирдяшова Ирина Юрьевна",
                reply_markup=None)

            elif call.data == 'michalchuk':
                bot.send_message(call.message.chat.id, '1.Учитель Физкультуры\nПочта: j.mikhalchuk@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Михальчук Юлия Николаевна",
                reply_markup=None)

            elif call.data == 'myagkov':
                bot.send_message(call.message.chat.id, '1.Учитель Физкультуры\nПочта: a.myagkov@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Мягков Артем Михайлович",
                reply_markup=None)

            elif call.data == 'nesterov':
                bot.send_message(call.message.chat.id, '1.Учитель Физкультуры\nПочта: s.nesterov@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Нестеров Станислав Викторович",
                reply_markup=None)

            elif call.data == 'tolstov':
                bot.send_message(call.message.chat.id, '1.Учитель Физкультуры\nПочта: v.tolstov@1520edu.ru',
                parse_mode='html')

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Толстов Виктор Викторович",
                reply_markup=None)

            else:
                bot.send_message(call.message.chat.id, '😸 Пожалуйста, нажимайте на кнопки')

    except Exception as e:
        print(repr(e))

        logger.warning("WARNING with callback_inline")
        logger.error("ERROR with callback_inline")
        logger.critical("CRITICAL with callback_inline")

# RUN
bot.polling(none_stop=True)
