class SensorClient:
    # Constructor
    def __init__(self):      
        self.Room = "Room"
        self.BrokerIp = "000.000.000.000"
        self.Interval = 5
        self.Temperature = 30.2
        self.Humidity = 88.34
        self.TemperatureLimit = 90.00
        self.HumidityLimit = 90.00
        try:
            f = open("config.txt", "r")
            print(f.read()) 
        except:
            print("Config files missing, client will shut down")


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
