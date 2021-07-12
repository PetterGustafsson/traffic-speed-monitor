import paho.mqtt.client as mqtt #import the client1

# broker_address="192.168.1.184" 
print("1")
broker_address="mqtt.eclipse.org" #use external broker
print("1")
client = mqtt.Client("P1") #create new instance
print("1")
client.connect(broker_address) #connect to broker
print('OFF')
client.publish("traffic_monitor","OFF")#publish
