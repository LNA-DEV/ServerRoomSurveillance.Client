from fileinput import close
from os import stat
from pydoc import cli
from traceback import print_tb
import paho.mqtt.client as mqtt
import time
from datetime import datetime
from ServerRoomHTTPHandler import ServerRoomHTTPHandler
import RPi.GPIO as GPIO


class SensorClient:
    hostName = "localhost"
    serverPort = 1111
    deviceId = "28-3c01f0952d3c"

    def __init__(self):
        self.Temperature = "0.0"
        self.Humidity = "0.0"
        self.AlarmActive = False
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.IN)

        ServerRoomHTTPHandler.run(SensorClient.hostName, SensorClient.serverPort)

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

    def getTemperature(self):
        path = f"/sys/bus/w1/devices/" + self.deviceId + "/w1_slave"
        fin = open(path, "r")
        fin.readline()
        line = fin.readline().strip()
        pos = line.rfind("=") + 1
        try:
            temp = float(line[pos:]) / 1000
        except:
            temp = float("NaN")
        fin.close()
        return temp

    def ReadDataFromSensor(self):
        self.Temperature = self.getTemperature()
        if GPIO.input(16) == GPIO.LOW:
            self.Humidity = 100
        else:
            self.Humidity = 0

    def StatusInfo(self):
        status = (
            self.Room
            + ":"
            + str(self.Temperature)
            + ":"
            + str(self.Humidity)
            + ":"
            + self.TemperatureLimit
            + ":"
            + self.HumidityLimit
        )
        return status

    def Run(self):
        while True:

            statusInfo = self.StatusInfo()
            self.mqttClient.publish("sensorclient/data", statusInfo)
            currentDateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(currentDateTime + " Published: " + statusInfo)

            self.ReadDataFromSensor()

            if (
                float(self.Humidity) >= float(self.HumidityLimit)
                or float(self.Temperature) >= float(self.TemperatureLimit)
                or self.AlarmActive
            ):
                currentDateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.mqttClient.publish("sensorclient/alarm", self.Room)
                print(currentDateTime + " ALARM")
                self.AlarmActive = True

            ServerRoomHTTPHandler.room = self.Room
            ServerRoomHTTPHandler.temp = self.Temperature
            ServerRoomHTTPHandler.humid = self.Humidity
            ServerRoomHTTPHandler.tlimit = self.TemperatureLimit
            ServerRoomHTTPHandler.hlimit = self.HumidityLimit

            time.sleep(int(self.Interval))

    def MessageReceived(self):
        print("Not implemented")

    def SaveLimits(self):
        f = open("limits.txt", "w")
        f.writelines(self.TemperatureLimit + "\n" + self.HumidityLimit)

    def Connect(self):
        self.mqttClient = mqtt.Client("SensorClientRoom" + self.Room)
        self.mqttClient.connect(self.BrokerIp)
