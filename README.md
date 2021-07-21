# traffic-speed-monitor
Measure speed of passing cars

System that detects and monitors the speed of vehicles passing by on a one lane street. The cars are detected with OpenCV and a Haar Cascade classifier The motion is tracked and results are recorded.

This projects uses RasperryPi 3b with Camera module V.2
Results are published to an MQTT server, which can then be subscribed to from external machine.

To get speed of vehicle, the user need to calibrate by getting pixels/length of a sample of passing cars.


![image](https://user-images.githubusercontent.com/54184145/125330546-c550af00-e2fb-11eb-91fa-e622fdc86e1d.png)
