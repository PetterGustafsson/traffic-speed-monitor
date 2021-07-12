import cv2
import statistics
import paho.mqtt.client as mqtt #import the client1
import serial
import time

mqtt_url = "a2nu865xwia0u3-ats.iot.us-west-2.amazonaws.com"
root_ca ='/Users/pettergustafsson/Desktop/IoT/Project/iot-test/certificates/G2-RootCA1.pem'
public_crt = '/Users/pettergustafsson/Desktop/IoT/Project/iot-test/certificates/8cc5e6d9bc-certificate.pem.crt'
private_key = '/Users/pettergustafsson/Desktop/IoT/Project/iot-test/certificates/8cc5e6d9bc-private.pem.key'


#Establish GPS signal (4 digit precision, (3-10m))

def convert_to_decimal(coord):
    
    if coord[-1] == 'S' or coord[-1] == 'W':
        prefix = -1
    else:
        prefix = 1
    if len(str(int(float(coord[:6])))) ==5:
        degrees = coord[:3]
        dec =float(coord[3:-2]) /60
    else:
        degrees = coord[:2]
        dec = float(coord[2:-2]) /60 
    val = float(degrees) + dec
    return(val * prefix)
    

def publish(lat,lon,speed):
    broker_address="mqtt.eclipse.org" #use external broker
    client.tls_set(caPath, certfile = certPath,  keyfile = keyFile)


    client = mqtt.Client("P1") #create new instance
    client.connect(broker_address) #connect to broker
    client.publish("traffic_monitor",(lat,lon,speed))#publish

port = "/dev/ttyS0"    
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
while True:
    data = ser.readline()
    if data[0:6] == b'$GPGLL':
        data = data.decode("utf-8")
        lat = data[7:19]
        lon = data[20:33]
        lat = str(convert_to_decimal(lat))
        lon = str(convert_to_decimal(lon))
        break
        

    
#If you want to run this script, replace the two link with the paths to the files on your machine
cascade_src = '/home/pi/Desktop/sideview_cascade_classifier.xml'

video_src = '/home/pi/Desktop/IMG_2574.MOV' #Replace with live feed

cap = cv2.VideoCapture(video_src)
fgbg = cv2.createBackgroundSubtractorMOG2()
car_cascade = cv2.CascadeClassifier(cascade_src)
last_position = None
speed = None
speed_log = []
while True:
    position = None

    ret, img = cap.read()
    fgbg.apply(img)
    if (type(img) == type(None)):
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale3(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    
    flags = cv2.CASCADE_SCALE_IMAGE,
    outputRejectLevels = True,
    minSize=(400, 150),
    maxSize = (500,200))

    
    
    try:
        position = cars[0][0][0]
    except:
        position = None

    if position != None and last_position != None:
        speed = position - last_position
        # print(speed,position,last_position)
        if position > last_position:
            speed_log.append(speed)
        else:
            if len(speed_log) > 5:
                speed = statistics.mean(speed_log)
                publish(lat,lon,str(speed))
                
                print('Car speed:',speed,'pixels/frame time')

            speed_log = []
        last_position = position
        
    
    if position == None and last_position != None:

        last_position = None
        speed_log = []

    if position != None and last_position == None:
        last_position = position
    else:
        last_position = position


        



    for (x,y,w,h) in cars[0]:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        #cv2.putText(img, speed, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12),2)


    img = cv2.resize(img, (960, 540))

    cv2.imshow('Frame by Frame', img)
   
    
    if cv2.waitKey(33) == 27:
        break

cv2.destroyAllWindows()


