import cv2

import numpy as np

fram_1 = cv2.VideoCapture(0)

while True:
    ret, image = fram_1.read()
    cv2.imshow("F0",image)


    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #green color mask = (48 , 79, 0), (83 , 255, 255)
    green_lower = np.array([48 , 79, 0])
    green_upper = np.array([83 , 255, 255])
    #red color mask = (0 ,137,149), (11,255,255)
    red_lower = np.array([0 ,137,149])
    red_upper = np.array([11,255,255])
    

    
    mask_green = cv2.inRange(hsv,green_lower,green_upper)
    mask_red   = cv2.inRange(hsv,red_lower,red_upper)
    
    green_result = cv2.bitwise_and(image,image, mask= mask_green)
    red_result = cv2.bitwise_and(image,image, mask= mask_red)
    cv2.imshow("green",green_result)
    cv2.imshow("red",red_result)
    if cv2.waitKey(1) == ord('q'):
        break




# Code to send data from python to arduino and recive feedback
'''
# Importing Libraries
import serial
import time
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
def write_read(cmd):
    arduino.write(bytes(cmd, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
while True:
    cmd = input("Enter a command: ") # Taking input from user
    value = write_read(cmd)
    print(value) # printing the value
'''