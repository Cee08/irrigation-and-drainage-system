import time

# from main_fc.func import read_loop, blink_loop
import machine
import uasyncio as a
from dht import DHT11


class RainDropSensor:
    def __init__(self, max_unchanged_readings=5):
        self.adc = machine.ADC(0)
        self.conversion_factor = 100 / (65535)
        # self.max_unchanged_readings = max_unchanged_readings
        # self.prev_readings = []

    def read(self):
        rain_coverage = 100 - (self.adc.read_u16() * self.conversion_factor)
        return round(rain_coverage, 1)

    def isconnected(self):
        return False
        # readings = [self.read() for _ in range(self.max_unchanged_readings)]
        # if len(self.prev_readings) == 0 or readings != self.prev_readings:
        #     self.prev_readings = readings
        #     return True
        # else:
        #     return False

class HumidityTemperatureSensor:
    def __init__(self,pin=2) -> None:
        self.dht_sensor = DHT11(machine.Pin(pin))
        self.last_time_check=None
    def should_wait(self):
         if self.last_time_check is not None:
                t_diff=time.time()-self.last_time_check
                if t_diff<1.5:
                     time.sleep(1.5)
         self.last_time_check=time.time()
    def isconnected(self):
        try:
            self.read()
            return True
        except Exception as ex:
            return False
        
    def read(self):
        # Get the temperature and humidity data
        self.should_wait()
        self.dht_sensor.measure()
        temperature =self.dht_sensor.temperature()
        humidity =  self.dht_sensor.humidity()
        return temperature,humidity
    def read_temperature(self):
        self.should_wait()
        self.dht_sensor.measure()
        temperature =self.dht_sensor.temperature()
        return temperature
    def read_humidity(self):
        self.should_wait()
        self.dht_sensor.measure()
        humidity =  self.dht_sensor.humidity()
        return humidity
    

sensor=HumidityTemperatureSensor()
connected=sensor.isconnected()
print(f"Connected {connected}")