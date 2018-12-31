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
                          ConversationHandler, PicklePersistence)
import gpio
import db
import os
import logging
import constants as c
from pathlib import Path
home = str(Path.home())
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
persistence = PicklePersistence(filename=home+'/telegram/save_state')

markup_main = ReplyKeyboardMarkup([['Abrir Porton','Cerrar Porton'],
                  ['Timbre','Estado de los Portones'],
                  ['Subscripciones']], one_time_keyboard=True)
subscribe_main = ReplyKeyboardMarkup([['Ver subscripciones'],
                  ['Subscribirse','Desubscribirse'], ["Volver"]], one_time_keyboard=True)
gate_choose = ReplyKeyboardMarkup([list(map(str, range(1,c.NUM_GATES+1))),["Cancelar"]], one_time_keyboard=True)
all_gate_choose = ReplyKeyboardMarkup([list(map(str, range(0,c.NUM_GATES+1))),["Cancelar"]], one_time_keyboard=True)

def start(bot, update):
    if(c.DEBUG > 0):
        print(update.effective_user)
        print(update.message.chat_id)
    if(not update.effective_user.is_bot and db.get_authorized(update.effective_user.id)):
        update.message.reply_text(
        "Bienvenido {}\nQue desea hacer ?".format(update.effective_user.first_name),
        reply_markup=markup_main)
        return c.MAIN
    else:
        db.add_user(update.effective_user.id, update.effective_user.username, update.effective_user.first_name)
        update.message.reply_text("Usted no esta autorizado para utilizar este bot")
        return ConversationHandler.END

def main_menu(bot, update, user_data):
    text = update.message.text
    if (text == "Abrir Porton"):
        update.message.reply_text("Cual porton desea abrir?", reply_markup=gate_choose)
        return c.OPEN
    elif (text == "Cerrar Porton"):
        update.message.reply_text("Cual porton desea cerrar?", reply_markup=gate_choose)
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
def cancelar(update):
    if(update.message.text == "Cancelar"):
        update.message.reply_text("Que desea hacer? ",
        reply_markup=markup_main)
        return True
    return False
def open_gate(bot, update, user_data):
    if(cancelar(update)):
        return c.MAIN
    next_state = gpio.open_close_routine(update, int(update.message.text), c.OPEN_GPIO,"Abriendo porton ","abierto")
    update.message.reply_text("Que desea hacer? ", reply_markup=markup_main)
    return next_state

def close_gate(bot, update, user_data):
    if(cancelar(update)):
        return c.MAIN
    next_state = gpio.open_close_routine(update, int(update.message.text), c.CLOSED_GPIO,"Cerrando porton ","cerrado")
    update.message.reply_text("Que desea hacer? ", reply_markup=markup_main)
    return next_state

def subscribe_menu(bot, update, user_data):
    text = update.message.text
    if (text == "Subscribirse"):
        update.message.reply_text("A cual porton desea subscribirse?", reply_markup=all_gate_choose)
        return c.SELECT_SUBSCRIBE
    elif (text == "Desubscribirse"):
        update.message.reply_text("A cual porton desea desubscribirse?", reply_markup=all_gate_choose)
        return c.SELECT_UNSUBSCRIBE
    elif (text == "Ver subscripciones"):

        update.message.reply_text("A cual porton desea desubscribirse?", reply_markup=all_gate_choose)
        return c.MAIN
    return c.MAIN
def select_subscribe(bot, update, user_data):
    text = update.message.text
    if(cancelar(update)):
        return c.MAIN
    return c.MAIN
def select_unsubscribe(bot, update, user_data):
    text = update.message.text
    if(cancelar(update)):
        return c.MAIN
    return c.MAIN
def blocked_menu(bot, update):
    update.message.reply_text('Usted no esta autorizado')
    return c.MAIN

def done(bot, update):
    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    #Read Token
    token = someVariable = os.environ['TELEGRAM_TOKEN']
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token, persistence=persistence)
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
            c.SELECT_SUBSCRIBE: [RegexHandler('^(\d+|Cancelar)$',
                                           select_subscribe,
                                           pass_user_data=True),
                            ],
            c.SELECT_UNSUBSCRIBE: [RegexHandler('^(\d+|Cancelar)$',
                                           select_unsubscribe,
                                           pass_user_data=True),
                            ],
            c.BLOCKED: [MessageHandler(Filters.text,
                                           blocked_menu,
                                           pass_user_data=True),
                            ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)],
        persistent=True, name='default'
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