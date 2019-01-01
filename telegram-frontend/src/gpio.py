import constants as c
if(c.DEVELOPER_COMPUTER != '64bit'):
    import mraa
from time import sleep
from threading import Thread

gpiowrite_list = []
gpioread_list = []

def touch_button(index):
    if(c.DEVELOPER_COMPUTER != '64bit'):
        gpiowrite_list[index].write(1)
        sleep(c.DELAY)
        gpiowrite_listp[index].write(0)
    else:
        print(index)

def read_gpio(index):
    if(c.DEVELOPER_COMPUTER == '64bit'):
        return 1
    else:
        return gpioread_list[index].read()

def check_if_finished(update, num, desired_state, action_text, state_text):
    text = str(num)
    count = c.MAX_TIME
    update.message.reply_text("Se notificara el estado en breve")
    while(read_gpio(num) != desired_state):
        sleep(1) # sleep 1 second
        count -= 1
        if(count == 0):
            update.message.reply_text("Porton "+ text+ " no pudo ser "+ state_text + "!!!\n Revise el estado manualmente")
        elif(count == int(c.MAX_TIME / 2)):
            update.message.reply_text("Porton "+ text+ " no ha podido ser "+ state_text + " todavia!\nPor favor espere")
    update.message.reply_text("Porton "+ text+ " "+ state_text + "!")




def open_close_routine(update, num,desired_state, action_text, state_text):
    text = str(num)
    if (num> c.NUM_GATES or num == 0):
        update.message.reply_text("Opcion invalida")
        return c.MAIN
    if (read_gpio(num) != desired_state):
        update.message.reply_text(action_text+ " "+ text)
        touch_button(num)
        Thread(target = check_if_finished, args = (update, num,desired_state, action_text, state_text, )).start()
        
    else:
        update.message.reply_text("Porton "+ text+ " ya esta " + state_text + "!")
    return c.MAIN 

def read_routine(gpio):
    print("pin " + repr(gpio.getPin(True)) + " = " + repr(gpio.read()))

def set_isr(function):
    if(c.DEVELOPER_COMPUTER != '64bit'):
        for gpio in gpioread_list:
            gpio.isr(mraa.EDGE_BOTH, function, gpio)

if(c.DEVELOPER_COMPUTER != '64bit'):
    for GPIO in c.GPIOREAD_LIST:
        gpio = mraa.Gpio(GPIO)
        gpio.dir(mraa.DIR_IN)
        gpioread_list.append(gpio)

    # initialise gpio
    for GPIO in c.GPIOWRITE_LIST:
        gpio = mraa.Gpio(GPIO)
        gpiowrite_list.append(gpio)
        gpio.dir(mraa.DIR_OUT)
        gpio.write(0)
