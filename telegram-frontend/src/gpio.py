import constants as c
if(c.DEVELOPER_COMPUTER != '64bit'):
    import mraa

gpiowrite_list = []
gpioread_list = []

def touch_button(index):
    if(c.DEVELOPER_COMPUTER != '64bit'):
        gpiowrite_list[index].write(1)
        time.sleep(DELAY)
        gpiowrite_listp[index].write(0)

def read_gpio(index):
    if(c.DEVELOPER_COMPUTER == '64bit'):
        return 1
    else:
        return gpioread_list[index].read()

def open_close_routine(update, num,desired_state, action_text, state_text):
    if (num> c.NUM_GATES or num == 0):
        update.message.reply_text("Opcion invalida\nQue desea hacer? ", reply_markup=markup_main)
        return c.MAIN
    if (read_gpio(num) != desired_state):
        update.message.reply_text(action_text+ " "+ text)
        touch_button(num)
        count = c.MAX_TIME
        while(read_gpio(num) != desired_state):
            time.sleep(1) # sleep 1 second
            count -= 1
            if(count == 0):
                update.message.reply_text("Porton "+ text+ " no pudo ser "+ state_text + "!!!",
                reply_markup=markup_main)
                return c.MAIN
        update.message.reply_text("Porton "+ text+ " "+ state_text + "!",
        reply_markup=markup_main)
    else:
        update.message.reply_text("Porton "+ text+ " ya esta " + state_text + "!",
        reply_markup=markup_main)
    return c.MAIN 

if(c.DEVELOPER_COMPUTER != '64bit'):
    for c.GPIO in c.GPIOREAD_LIST:
        gpio = mraa.Gpio(GPIO)
        gpio.dir(mraa.DIR_IN)
        gpioread_list.append(gpio)
        gpio.isr(mraa.EDGE_BOTH, read_routine, gpio)

    # initialise gpio
    for c.GPIO in c.GPIOWRITE_LIST:
        gpio = mraa.Gpio(GPIO)
        gpiowrite_list.append(gpio)
        gpio.dir(mraa.DIR_OUT)
        gpio.write(0)