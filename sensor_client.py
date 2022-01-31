from fileinput import close
from os import stat
from pydoc import cli
import this
from traceback import print_tb
import paho.mqtt.client as mqtt
import time
from datetime import datetime

class SensorClient:

    def __init__(self):      
        self.Temperature = "30.2"
        self.Humidity = "88.34"
        self.AlarmActive = False

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
        self.Humidity = float(self.Humidity)
        self.Temperature = float(self.Temperature)
        self.Humidity += 1
        self.Temperature += 1


    def StatusInfo(self):
        status = self.Room + ":" + str(self.Temperature) + ":" + str(self.Humidity) + ":" + self.TemperatureLimit + ":" + self.HumidityLimit
        return status

        
    def Run(self):
        while(True):

            statusInfo = self.StatusInfo()
            self.mqttClient.publish("sensorclient/data", statusInfo)
            currentDateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(currentDateTime + " Published: " + statusInfo)

            self.ReadDataFromSensor()

            if self.Humidity >= float(self.HumidityLimit) or self.Temperature >= float(self.TemperatureLimit) or self.AlarmActive:
                currentDateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.mqttClient.publish("sensorclient/alarm", self.Room)
                print(currentDateTime + " ALARM")
                self.AlarmActive = True


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
