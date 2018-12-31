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
import psycopg2
import gpio
import os
import logging
import time
import constants as c

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


markup_main = ReplyKeyboardMarkup([['Abrir Porton','Cerrar Porton'],
                  ['Timbre','Estado de los Portones'],
                  ['Subscripciones']], one_time_keyboard=True)
subscribe_main = ReplyKeyboardMarkup([['Ver subscripciones'],
                  ['Subscribirse','Desubscribirse'], ["Volver"]], one_time_keyboard=True)
markup_choose = ReplyKeyboardMarkup([list(map(str, range(1,c.NUM_GATES+1))),["Cancelar"]], one_time_keyboard=True)

def start(bot, update):
    if(c.DEBUG > 0):
        print(update.effective_user)
        print(update.message.chat_id)
    if(update.effective_user.username in  c.ALLOWED_USERS and not update.effective_user.is_bot):
        update.message.reply_text(
        "Bienvenido {}\nQue desea hacer ?".format(update.effective_user.first_name),
        reply_markup=markup_main)
        return c.MAIN
    else:
        update.message.reply_text("Usted no esta autorizado para utilizar este bot")
        return c.BLOCKED

def main_menu(bot, update, user_data):
    text = update.message.text
    if (text == "Abrir Porton"):
        update.message.reply_text("Cual porton desea abrir?", reply_markup=markup_choose)
        return c.OPEN
    elif (text == "Cerrar Porton"):
        update.message.reply_text("Cual porton desea cerrar?", reply_markup=markup_choose)
        return c.CLOSE
    elif (text == "Timbre"):
        touch_button(0)
        update.message.reply_text("Tocando el timbre..", reply_markup=markup_main)
        return c.MAIN
    elif (text == "Estado de los Portones"):
        message = ""
        for i in range(c.TOTAL_SENSORS):
            if(gpio.read_gpio(i) == c.CLOSED_GPIO):
                state = "cerrado"
            elif(gpio.read_gpio(i) == c.OPEN_GPIO):
                state = "abierto"
            else:
                state = "desconocido"
            if(i == 0):
                message += "Puerta principal en estado: " + state + "\n"
            else: 
                message += "Porton "+ str(i)+ " en estado: " + state + "\n"
        update.message.reply_text(message, reply_markup=markup_main)
        return c.MAIN
    elif (text == "Subscripciones"):
        update.message.reply_text('Subscribiendo...',
        reply_markup=subscribe_main)
        return c.SUBSCRIBE
    else:
        return c.MAIN
    

    return c.MAIN

def open_gate(bot, update, user_data):
    
    text = update.message.text
    if(text == "Cancelar"):
        update.message.reply_text("Que desea hacer? ", reply_markup=markup_main)
        return c.MAIN
    num = int(text)
    return gpio.open_close_routine(update, num, c.OPEN_GPIO,"Abriendo porton ","abierto")

def close_gate(bot, update, user_data):
    text = update.message.text
    if(text == "Cancelar"):
        update.message.reply_text("Que desea hacer? ",
        reply_markup=markup_main)
        return c.MAIN
    num = int(text)
    return gpio.open_close_routine(update, num, c.CLOSED_GPIO,"Cerrando porton ","cerrado")

def subscribe_menu(bot, update):
    update.message.reply_text('Subscribiendo...',
        reply_markup=markup_main)
    return c.MAIN
def blocked_menu(bot, update):
    update.message.reply_text('Usted no esta autorizado')
    return c.MAIN

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
    # Add conversation handler with the states c.MAIN, c.SUBSCRIBE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            c.MAIN: [RegexHandler('^(Abrir Porton|Cerrar Porton|Timbre|Estado de los Portones|Subscripciones)$',
                                    main_menu,
                                    pass_user_data=True),
                       ],
            c.OPEN: [RegexHandler('^(\d+|Cancelar)$',
                                    open_gate,
                                    pass_user_data=True),
                       ],
            c.CLOSE: [RegexHandler('^(\d+|Cancelar)$',
                                    close_gate,
                                    pass_user_data=True),
                       ],
            c.SUBSCRIBE: [RegexHandler('^(Ver subscripciones|Subscribirse|Desubscribirse|Volver)$',
                                           subscribe_menu,
                                           pass_user_data=True),
                            ],
            c.BLOCKED: [MessageHandler(Filters.text,
                                           blocked_menu,
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