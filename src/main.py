import os

from flask import Flask, request
import telebot

from grammar_check import grammar_check
from punctuation_check import punctuation_check
from settings import get_user_settings, save_user_settings
from spell_check import spell_check
from syntax_check import check_syntax

app = Flask(__name__)
bot=telebot.TeleBot('5978160141:AAEv-aR_YApWY0cKKxepNBKyCLwkIfqyQuA')


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    settings = get_user_settings(user_id)
    reply_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.row('Grammar', 'Punctuation')
    reply_markup.row('Spelling', 'Syntax')
    reply_markup.row('Settings')
    bot.send_message(user_id, 'Welcome to Grammar Bot!', reply_markup=reply_markup)

    if not settings:
        settings = {'grammar': True, 'punctuation': True, 'spelling': True, 'syntax': True}
        save_user_settings(user_id, settings)


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    settings = get_user_settings(user_id)

    if message.text == 'Grammar':
        if settings['grammar']:
            bot.send_message(chat_id, 'Grammar check is already enabled!')
        else:
            save_user_settings(user_id, {'grammar': True})
            bot.send_message(chat_id, 'Grammar check has been enabled!')

    elif message.text == 'Punctuation':
        if settings['punctuation']:
            bot.send_message(chat_id, 'Punctuation check is already enabled!')
        else:
            save_user_settings(user_id, {'punctuation': True})
            bot.send_message(chat_id, 'Punctuation check has been enabled!')

    elif message.text == 'Spelling':
        if settings['spelling']:
            bot.send_message(chat_id, 'Spelling check is already enabled!')
        else:
            save_user_settings(user_id, {'spelling': True})
            bot.send_message(chat_id, 'Spelling check has been enabled!')

    elif message.text == 'Syntax':
        if settings['syntax']:
            bot.send_message(chat_id, 'Syntax check is already enabled!')
        else:
            save_user_settings(user_id, {'syntax': True})
            bot.send_message(chat_id, 'Syntax check has been enabled!')

    elif message.text == 'Settings':
        reply_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        reply_markup.row('Grammar', 'Punctuation')
        reply_markup.row('Spelling', 'Syntax')
        bot.send_message(user_id, 'Settings', reply_markup=reply_markup)

    else:
        text = message.text
        result = text
        if settings['grammar']:
            result = grammar_check(result)
        if settings['punctuation']:
            result = punctuation_check(result)
        if settings['spelling']:
            result = spell_check(result)
        if settings['syntax']:
            result = check_syntax(result)
        bot.send_message(chat_id, result)


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id, 'Type any text and the bot will check it for grammar, punctuation, spelling and syntax errors. You can also enable or disable specific checks with the settings command.')


if __name__ == '__main__':
    app.run()