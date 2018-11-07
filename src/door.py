import RPi.GPIO as GPIO  
from time import sleep     # this lets us have a time delay (see line 15)  
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO25 as input (button)  
GPIO.setup(17, GPIO.OUT)   # set GPIO24 as an output (LED)  
GPIO.output(17, True)
  
try:  
    while True:            # this will carry on until you hit CTRL+C  
        print(GPIO.input(4))
        sleep(0.1)         # wait 0.1 seconds  
        GPIO.output(17, GPIO.input(4))
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself 
