import Adafruit_DHT

# humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

class DHT11:

    #self._var   Protected variable
    #self.__var  Private variable
    def __init__(self, pin):
        
        self._data = None
        self._pin = pin
        
    @property
    def data(self):
        return self._data
        
    @property
    def pin(self):
        return self._pin
    
    def sense(self):
        #sensor, pin
        try:
            readings = Adafruit_DHT.read_retry(11, self._pin)
            #humidity, temperature
            self._data = readings
            #(humidity, temperature)
            return self._data
        except Exception as e:
            self._data = None
            print "There was an error reading the sensor's data\n\t" + str(e)