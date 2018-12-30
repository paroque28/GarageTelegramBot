import mraa
import constants

gpiowrite_list = []
gpioread_list = []

def touch_button(index):
    gpiowrite_list[index].write(1)
    time.sleep(DELAY)
    gpiowrite_listp[index].write(0)

def read_gpio(index):
    return gpioread_list[index].read()

for GPIO in GPIOREAD_LIST:
    gpio = mraa.Gpio(GPIO)
    gpio.dir(mraa.DIR_IN)
    gpioread_list.append(gpio)
    gpio.isr(mraa.EDGE_BOTH, read_routine, gpio)

# initialise gpio
for GPIO in GPIOWRITE_LIST:
    gpio = mraa.Gpio(GPIO)
    gpiowrite_list.append(gpio)
    gpio.dir(mraa.DIR_OUT)
    gpio.write(0)