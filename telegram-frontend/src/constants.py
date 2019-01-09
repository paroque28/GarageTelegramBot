import platform
from os import environ

def os_env_var(var_name, default):
    if var_name in environ:
        return environ.get(var_name)
    else:
        return default
# Used to fake gpio
DEVELOPER_COMPUTER = platform.architecture()[0]
# Developer tests token $env:TELEGRAM_TOKEN = "681248634:AAFxOsEz3yCTMlu9puVfhtOOEIugYElHL2A"
# Debug:  0 : disabled, 1: debug info messages, 2: frequent debug messages (bad for logs), 3: super annoying logs
DEBUG = int(os_env_var("TELEGRAM_DEBUG", 3))
# Foresee more doors
NUM_GATES = 2
TOTAL_SENSORS = 3
TOTAL_RELAYS = 3
# Max wating time for open/ close operations
MAX_TIME = int(os_env_var("TELEGRAM_MAX_TIME", 35))
# Max wating time minutes for close operations
MAX_TIME_WAIT = int(os_env_var("TELEGRAM_MAX_TIME_WAIT", 2))
# Max number of retries each DELAY_ALERT MINUTES
MAX_ALERT_MESSAGES = int(os_env_var("TELEGRAM_MAX_ALERT_MESSAGES", 2))
# Number of minutes between alerts
DELAY_ALERT = int(os_env_var("TELEGRAM_DELAY_ALERT", 5))
# States for Telegram logic
MAIN, OPEN, CLOSE, SUBSCRIBE, SELECT_SUBSCRIBE, SELECT_UNSUBSCRIBE, END, BLOCKED = range(8)
# Delay on amount time relay is on
DELAY = 0.7
# Intel Edison GPIO pins with Sparkfun breakout board
GP44 = 31
GP45 = 45
GP46 = 32
GP47 = 46
GP48 = 33
GP49 = 47
 #GPIO list for relays
GPIOWRITE_LIST = [GP44, GP46, GP48]
# GPIO list for sensors
GPIOREAD_LIST = [GP45, GP47, GP49]
# Sensor closed position
CLOSED_GPIO = 1
# Sensor open position
OPEN_GPIO = 0