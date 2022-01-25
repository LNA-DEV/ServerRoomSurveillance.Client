from fileinput import close
from os import stat
from pydoc import cli
from traceback import print_tb
import paho.mqtt.client as mqtt
import time

class SensorClient:
    # Constructor
    def __init__(self):      
        self.Temperature = "30.2"
        self.Humidity = "88.34"

        try:
            f = open("config.txt", "r")
            self.Room = f.readline().strip()
            self.BrokerIp = f.readline().strip()
            self.Interval = f.readline().strip()
            f.close
        except:
            print("Config files missing, client will shut down")

        try:
            f = open("limits.txt", "r")
            self.TemperatureLimit = f.readline().strip()
            self.HumidityLimit = f.readline().strip()
            f.close
        except:
            print("limits.txt missing")
            self.TemperatureLimit = "40"
            self.HumidityLimit = "85"

        print("Init successfull")
        print("TemperatureLimit: " + self.TemperatureLimit)
        print("HumidityLimit: " + self.HumidityLimit)
        print("Room: " + self.Room)
        print("BrokerIp: " + self.BrokerIp)
        print("Interval: " + self.Interval)

        self.Connect()
        self.Run()


    def ReadDataFromSensor(self):
        print("Not implemented")


    def StatusInfo(self):
        status = self.Room + ":" + self.Temperature + ":" + self.Humidity + ":" + self.TemperatureLimit + ":" + self.HumidityLimit
        return status


    def Run(self):
        while(True):
            statusInfo = self.StatusInfo()
            self.mqttClient.publish("sensorclient/data", statusInfo)
            print("Published: " + statusInfo)
            time.sleep(int(self.Interval))


    def MessageReceived(self):
        print("Not implemented")


    def SaveLimits(self):
        f = open("limits.txt", "w")
        f.writelines(self.TemperatureLimit + "\n" + self.HumidityLimit)


    def Connect(self):
        self.mqttClient = mqtt.Client("SensorClientRoom" + self.Room)
        self.mqttClient.connect(self.BrokerIp)


client = SensorClient()
