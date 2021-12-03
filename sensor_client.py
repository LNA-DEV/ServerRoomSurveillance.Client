class SensorClient:
    Room = "Room"
    BrokerIp = "000.000.000.000"
    Interval = 5
    Temperature = 30.2
    Humidity = 88.34
    TemperatureLimit = 90.00
    HumidityLimit = 90.00

    def __init__(self):
        print("Not implemented")

    def ReadDataFromSensor(self):
        print("Not implemented")

    def StatusInfo(self):
        print("Not implemented")

    def Run(self):
        print("Not implemented")

    def MessageReceived(self):
        print("Not implemented")

    def SaveLimits(self):
        print("Not implemented")


# Test
client = SensorClient()
client2 = SensorClient()
client.Room = "Room2"
print(client.Room)
print(client2.Room)
