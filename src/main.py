#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import os
import logging
import mraa
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
NUM_GATES = 2
MAIN, OPEN, CLOSE, SET, END = range(5)
GP44 = 31

# initialise gpio GP44
gpio_1 = mraa.Gpio(GP44)

# set gpio GP44 to output
gpio_1.dir(mraa.DIR_OUT)


markup_main = ReplyKeyboardMarkup([['Abrir Porton','Cerrar Porton'],
                  ['Timbre','Estado de los Portones'],
                  ['Ultimas 5 Acciones']], one_time_keyboard=True)
markup_choose = ReplyKeyboardMarkup([map(str, range(1,NUM_GATES+1)),["Cancelar"]], one_time_keyboard=True)

def start(bot, update):
    update.message.reply_text(
        "Bienvenido a RQWireless {}\nQue desea hacer ?".format(update.effective_user.first_name),
        reply_markup=markup_main)
    print(update.effective_user)

    return MAIN

def main_menu(bot, update, user_data):
    text = update.message.text
    if (text == "Abrir Porton"):
        update.message.reply_text("En hora buena! Cual desea abrir?", reply_markup=markup_choose)
        return OPEN
    elif (text == "Cerrar Porton"):
        update.message.reply_text("Cual desea cerrar?", reply_markup=markup_choose)
        return CLOSE
    elif (text == "Timbre"):
        update.message.reply_text("Tocando el timbre..", reply_markup=markup_main)
        return MAIN
    else:
        return MAIN
    

    return MAIN

def open_gate(bot, update, user_data):
    text = update.message.text
    update.message.reply_text("Abriendo porton "+ text,
        reply_markup=markup_main)
    gpio_1.write(1)
    time.sleep(0.5)
    gpio_1.write(0)
    return MAIN

def close_gate(bot, update, user_data):
    text = update.message.text
    update.message.reply_text("Cerrando porton "+ text,
        reply_markup=markup_main)
    return MAIN

def set_menu(bot, update):
    update.message.reply_text('Seteando...',
        reply_markup=markup_main)
    return MAIN

def done(bot, update, user_data):
    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    #Read Token
    token = someVariable = os.environ['TELEGRAM_TOKEN']
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states MAIN, SET
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MAIN: [RegexHandler('^(Abrir Porton|Cerrar Porton|Timbre|Estado de los Portones|Ultimas 5 Acciones)$',
                                    main_menu,
                                    pass_user_data=True),
                       ],
            OPEN: [RegexHandler('^(\d+|Cancelar)$',
                                    open_gate,
                                    pass_user_data=True),
                       ],
            CLOSE: [RegexHandler('^(\d+|Cancelar)$',
                                    close_gate,
                                    pass_user_data=True),
                       ],
            SET: [MessageHandler(Filters.text,
                                           set_menu,
                                           pass_user_data=True),
                            ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()