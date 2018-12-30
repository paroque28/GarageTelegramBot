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
ALLOWED_USERS = ["cyanpablo", "perohe28", "vickyque14", "perq08"]
NUM_GATES = 2
MAX_TIME = 20
MAIN, OPEN, CLOSE, SUBSCRIBE, END, BLOCKED = range(6)
DELAY = 0.7
GP44 = 31
GP45 = 45
GP46 = 32
GP47 = 46
GP48 = 33
GP49 = 47
GPIOWRITE_LIST = [GP44, GP46, GP48]
GPIOREAD_LIST = [GP45, GP47, GP49]
# initialise gpio
gpiowrite_list = []
gpioread_list = []
for GPIO in GPIOWRITE_LIST:
    gpio = mraa.Gpio(GPIO)
    gpiowrite_list.append(gpio)
    gpio.dir(mraa.DIR_OUT)
    gpio.write(0)


def read_routine(gpio):
    print("pin " + repr(gpio.getPin(True)) + " = " + repr(gpio.read()))

def touch_button(gpio):
    gpio.write(1)
    time.sleep(DELAY)
    gpio.write(0)

for GPIO in GPIOREAD_LIST:
    gpio = mraa.Gpio(GPIO)
    gpio.dir(mraa.DIR_IN)
    gpioread_list.append(gpio)
    gpio.isr(mraa.EDGE_BOTH, read_routine, gpio)


markup_main = ReplyKeyboardMarkup([['Abrir Porton','Cerrar Porton'],
                  ['Timbre','Estado de los Portones'],
                  ['Subscribirse']], one_time_keyboard=True)
markup_choose = ReplyKeyboardMarkup([list(map(str, range(1,NUM_GATES+1))),["Cancelar"]], one_time_keyboard=True)

def start(bot, update):
    if(update.effective_user.username in  ALLOWED_USERS):
        update.message.reply_text(
        "Bienvenido a RQWireless {}\nQue desea hacer ?".format(update.effective_user.first_name),
        reply_markup=markup_main)
        return MAIN
    else:
        update.message.reply_text("Usted no esta autorizado para utilizar este bot")
        return BLOCKED

def main_menu(bot, update, user_data):
    text = update.message.text
    if (text == "Abrir Porton"):
        update.message.reply_text("Cual porton desea abrir?", reply_markup=markup_choose)
        return OPEN
    elif (text == "Cerrar Porton"):
        update.message.reply_text("Cual porton desea cerrar?", reply_markup=markup_choose)
        return CLOSE
    elif (text == "Timbre"):
        gpiowrite_list[0].write(1)
        time.sleep(DELAY)
        gpiowrite_list[0].write(0)
        update.message.reply_text("Tocando el timbre..", reply_markup=markup_main)
        return MAIN
    elif (text == "Estado de los Portones"):
        for i in range(len(gpioread_list)):
            if(gpioread_list[i].read() == 1):
                estado = "cerrado"
            elif(gpioread_list[i].read() == 0):
                estado = "abierto"
            else:
                estado = "desconocido"
            update.message.reply_text("Porton "+ str(i)+ " en estado: " + estado)
        update.message.reply_text("Fin", reply_markup=markup_main)
        return MAIN
    elif (text == "Subscribirse"):
        update.message.reply_text('Subscribiendo...',
        reply_markup=markup_main)
        return MAIN
    else:
        return MAIN
    

    return MAIN

def open_gate(bot, update, user_data):
    
    text = update.message.text
    if(text == "Cancelar"):
        update.message.reply_text("Que desea hacer? ",
        reply_markup=markup_main)
    else:
        num = int(text)
        if (gpioread_list[num].read() == 1):
            update.message.reply_text("Abriendo porton "+ text)
            touch_button(gpiowrite_list[num])
            count = MAX_TIME
            while(gpioread_list[num].read() == 1):
                time.sleep(1)
                count -= 1
                if(count == 0):
                    update.message.reply_text("Porton "+ text+ " no pudo ser abierto!!!",
                    reply_markup=markup_main)
                    return MAIN
            update.message.reply_text("Porton "+ text+ " abierto!",
            reply_markup=markup_main)
        else:
            update.message.reply_text("Porton "+ text+ " ya esta abierto!",
            reply_markup=markup_main)
    return MAIN

def close_gate(bot, update, user_data):
    text = update.message.text
    if(text == "Cancelar"):
        update.message.reply_text("Que desea hacer? ",
        reply_markup=markup_main)
    else:
        num = int(text)
        if (gpioread_list[num].read() == 0):
            update.message.reply_text("Cerrando porton "+ text)
            touch_button(gpiowrite_list[num])
            count = MAX_TIME
            while(gpioread_list[num].read() == 0):
                time.sleep(1)
                count -= 1
                if(count == 0):
                    update.message.reply_text("Porton "+ text+ " no pudo ser cerrado!!!",
                    reply_markup=markup_main)
                    return MAIN
            update.message.reply_text("Porton "+ text+ " cerrado!",
            reply_markup=markup_main)
        else:
            update.message.reply_text("Porton "+ text+ " ya esta cerrado!",
            reply_markup=markup_main)
    return MAIN

def subscribe_menu(bot, update):
    update.message.reply_text('Subscribiendo...',
        reply_markup=markup_main)
    return MAIN
def blocked_menu(bot, update):
    update.message.reply_text('Usted no esta autorizado')
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

    # Add conversation handler with the states MAIN, SUBSCRIBE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MAIN: [RegexHandler('^(Abrir Porton|Cerrar Porton|Timbre|Estado de los Portones|Subscribirse)$',
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
            SUBSCRIBE: [MessageHandler(Filters.text,
                                           subscribe_menu,
                                           pass_user_data=True),
                            ],
            BLOCKED: [MessageHandler(Filters.text,
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