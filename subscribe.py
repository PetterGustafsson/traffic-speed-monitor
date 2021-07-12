import paho.mqtt.client as mqtt
import time
import json

def read_json(json_file):
    json_file = open("traffic_log.json", "r")
    json_object = json.load(json_file)
    json_file.close()

    return(json_object)

def write_json(json_file, json_object):
    json_file = open("traffic_log.json", "w")
    json.dump(json_object, json_file)
    json_file.close()
    return("Write done")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("traffic_monitor")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message =str(msg.payload)
    message = message.split( )

    lat = message[0][2:]
    lon = message[1]
    lat = round(float(lat),4)
    lon = round(float(lon),4)
    
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y %H:%M:%S", named_tuple)
    time_string = time_string.split( )
    date = time_string[0]
    tme = time_string[1]
    speed = message[2][:-1]
    device_location = "{},{}".format(lat,lon)
    print(1)
    json_object = read_json("traffic_log.json")
    print(3)
    if device_location in json_object:
        date_dict = json_object[device_location]
        if date in date_dict:
            json_object[device_location][date][tme] = speed
            print(write_json("traffic_log.json", json_object))
            print(2)
            
        else:
            speed_dict = {}
            speed_dict[tme] = speed
            date_dict[date] = speed_dict
            json_object[device_location] = date_dict
            print(write_json("traffic_log.json", json_object))
            print(2)
            
    else:
        speed_dict = {}
        speed_dict[tme] = speed
        date_dict = {}
        date_dict[date] = speed_dict
        json_object[device_location] = date_dict
        print(write_json("traffic_log.json", json_object))
        print(2)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipse.org", 1883, 60)

client.loop_forever()
