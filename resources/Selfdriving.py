#!python3
# import the necessary packages
from distutils.cmd import Command
from resources.shape_classifier import Detector
import numpy as np
import imutils
import cv2
import serial
import time




def detect(cnts,color,image):
    # loop over the contours
    max = 0
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        try : 
            if cv2.contourArea(c)  < 2000 : continue
            if cv2.contourArea(c) > max : max =  cv2.contourArea(c)
            # shape = sd.detect(c)
            # if shape != "rectangle": continue
            # if shape not in ["square","rectangle"] : continue
            M = cv2.moments(c) 
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
            # print(shape,cX,cY)
            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            # draw contours around the detected shapes 
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            # draw circle at the center of the shape 
            cv2.circle(image,(cX, cY),1,( 255,0 , 0),10)
            # write the co-ordinates 
            cv2.putText(image, color , (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.7, ( 0 , 0 , 255), 2)
        except : pass
    return max







# create shape detector opject 
sd = Detector()
# Starting the webcam
vs = cv2.VideoCapture(1)
# creat arduino object
arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)




#(hMin = 0 , sMin = 0, vMin = 255), (hMax = 179 , sMax = 255, vMax = 255)
#(hMin = 0 , sMin = 0, vMin = 186), (hMax = 179 , sMax = 132, vMax = 255)

while True:
    ret, frame = vs.read()
    # Points counter 
    counter = 0    
    # falg 
    done = False
    # main loop 
    # load the image and resize it to a smaller factor so that
    image = imutils.resize(frame, width=720)
    # resize the images 
    resized = imutils.resize(image, width=480)
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    # for green color 
    # (hMin = 31 , sMin = 148, vMin = 21), (hMax = 67 , sMax = 255, vMax = 247)
    green_lower = np.array([31 , 148, 21], np.uint8)
    green_upper = np.array([67 , 255, 247], np.uint8)
    
    # for red color
    # (hMin = 0 , sMin = 196, vMin = 106), (hMax = 31 , sMax = 254, vMax = 255)
    red_lower = np.array([0 ,196,106], np.uint8)
    red_upper = np.array([31,254,255], np.uint8)

    # masks
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    red_mask = cv2.inRange(hsv, red_lower, red_upper)

    # reduce the resoluation 
    ratio = image.shape[0] / float(resized.shape[0])
    # convert the resized image to grayscale, blur it slightly,
    #gray = cv2.cvtColor(green_mask, cv2.COLOR_BGR2GRAY)
    # green_blurred images
    green_blurred = cv2.GaussianBlur(green_mask, (5, 5),200)
    red_blurred = cv2.GaussianBlur(red_mask, (5, 5),200)
    # and threshold it
    green_thresh = cv2.threshold(green_blurred, 20, 255, cv2.THRESH_BINARY)[1]
    red_thresh = cv2.threshold(red_blurred, 20, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image and initialize the
    
    
    # shape detector
    cnts_G = cv2.findContours(green_thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts_G = imutils.grab_contours(cnts_G)
    cnts_R = cv2.findContours(red_thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts_R = imutils.grab_contours(cnts_R)
    # wait key from keyboard
    green_area = detect(cnts_G,"Green",image)
    red_area = detect(cnts_R,"Red",image)
    # Sending the points to arduino 
    if arduino != None and not  done:
        # Sent the points to arduino
        if green_area > red_area : cmd = "Green"
        elif green_area < red_area  : cmd = "Red"
        else : cmd = 'None'
        arduino.write(cmd.encode())
        # Print 
        print("Command. {} sent".format(cmd))
    cv2.imshow("Output",image)
    cv2.imshow("th",green_thresh)
    
  
    
    #cv2.imshow("R",r)
    
    # if the `q` key is pressed, break from the lop
    if cv2.waitKey(1) == ord("q"):
    	break
   
# cleanup the camera and close any open windows
cv2.destroyAllWindows()

