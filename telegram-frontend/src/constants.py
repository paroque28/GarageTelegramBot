# Debug:  0 : disabled, 1: debug info messages, 2: frequent debug messages (bad for logs), 3: super annoying logs
DEBUG = 1
# Allowed users to operate doors to improve with database
ALLOWED_USERS = ["cyanpablo", "perohe28", "vickyque14", "perq08"]
# Foresee more doors
NUM_GATES = 2
TOTAL_SENSORS = 3
TOTAL_RELAYS = 3
# Max wating time for open/ close operations
MAX_TIME = 20
# States for Telegram logic
MAIN, OPEN, CLOSE, SUBSCRIBE, END, BLOCKED = range(6)
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