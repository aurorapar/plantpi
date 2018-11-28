import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import json

from dht11 import DHT11
from watersensor import WaterSensor

class FuzzyPlantSystem:

    def __init__(self):
        # Input/output sets
        self._a_temp = ctrl.Antecedent(np.arange(32, 213, 1), 'temperature')
        self._a_humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
        self._a_water = ctrl.Antecedent(np.arange(0, 20, 1), 'water')

        self._c_pump = ctrl.Consequent(np.arange(0, 101, 1), 'pump')
        self._c_fan = ctrl.Consequent(np.arange(0, 101, 1), 'fan')

        # Input membership functions
        self._a_temp['low'] = fuzz.trapmf(self._a_temp.universe, [0, 0, 50, 65])
        self._a_temp['normal'] = fuzz.trapmf(self._a_temp.universe, [50, 65, 75, 80])
        self._a_temp['high'] = fuzz.trapmf(self._a_temp.universe, [80, 90, 212, 212])

        self._a_humidity['low'] = fuzz.trapmf(self._a_humidity.universe, [0, 0, 20, 35])
        self._a_humidity['normal'] = fuzz.trapmf(self._a_humidity.universe, [20, 35, 50, 60])
        self._a_humidity['high'] = fuzz.trapmf(self._a_humidity.universe, [55, 70, 100, 100])

        self._a_water['low'] = fuzz.trapmf(self._a_water.universe, [0, 0, 3, 5])
        self._a_water['normal'] = fuzz.trapmf(self._a_water.universe, [3, 5, 10, 12])
        self._a_water['high'] = fuzz.trapmf(self._a_water.universe, [11, 15, 20, 20])

        # Output membership functions
        self._c_pump['low'] = fuzz.trapmf(self._c_pump.universe, [0, 0, 30, 70])
        self._c_pump['high'] = fuzz.trapmf(self._c_pump.universe, [30, 70, 100, 100])

        self._c_fan['low'] = fuzz.trapmf(self._c_fan.universe, [0, 0, 35, 65])
        self._c_fan['high'] = fuzz.trapmf(self._c_fan.universe, [35, 65, 100, 100])

        rule1 = ctrl.Rule(self._a_temp['high'] | self._a_humidity['low'], self._c_fan['high'])
        rule2 = ctrl.Rule(self._a_humidity['low'] | self._a_temp['low'], self._c_fan['low'])
        rule3 = ctrl.Rule(self._a_water['low'], self._c_pump['high'])
        rule4 = ctrl.Rule(self._a_water['high'], self._c_pump['low'])

        self._plant_system_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
        self._plant_system = ctrl.ControlSystemSimulation(self._plant_system_control)
        
    def get_data(self):
        humidity, temp = DHT11(17).sense()
        waterLevel = int(WaterSensor().sense())
        self.humidity = humidity
        self.temperature = temp
        self.water = waterLevel/4
        
        print(self._plant_system.antecedents)
    
    @property
    def temperature(self):
        return self._plant_system.input['temperature']

    @temperature.setter
    def temperature(self, value):
        self._plant_system.input['temperature'] = value


    @property
    def humidity(self):
        return self._plant_system.input['humidity']

    @humidity.setter
    def humidity(self, value):
        self._plant_system['humidity'] = value

    
    @property
    def water(self):
        return self._plant_system.input['water']

    @water.setter
    def water(self, value):
        self._plant_system['water'] = value

    def update(self):
        self._plant_system.compute()
    
    @property
    def pump_output(self):
        return self._plant_system.output['pump']

    @property
    def fan_output(self):
        return self._plant_system.output['fan']
    
    @property
    def output(self):
        return self._plant_system.output
    
    
crop = FuzzyPlantSystem()
crop.get_data()

print('Water: ' + crop.water)
print('Humidity: ' + crop.humidity)
print('Temp: ' + crop.temperature)

crop.update()
print(json.dumps(crop.output, indent=4))




