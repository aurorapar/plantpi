import RPi.GPIO as GPIO
from time import sleep

LOWER_BOUND = 0
UPPER_BOUND = 180

class Relay:

    #self._var   Protected variable
    #self.__var  Private variable
    def __init__(self, pin):
        
        self._activated = False
        self._pin = pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.OUT)
        self.off()
        
    @property
    def activated(self):
        return self._activated
        
    @property
    def pin(self):
        return self._pin
    
    def off(self):

        try:
            GPIO.output(self._pin, 1)
            self._activated = False
            
        except Exception as e:
            self._activated = None
            print "There was an error turning off the relay\n\t" + str(e)
            
    def on(self, duration=None):

        try:
            if not duration:
                GPIO.output(self._pin, 0)
                self._activated = True
            else:
                if duration > LOWER_BOUND and duration < UPPER_BOUND:
                    self.on()
                    sleep(duration)
                    self.off()
                else:
                    print("Time is out of range [%s,%s]. Found %s"%(LOWER_BOUND,UPPER_BOUND,duration))
            
        except Exception as e:
            self._activated = None
            print "There was an error turning on the relay\n\t" + str(e)