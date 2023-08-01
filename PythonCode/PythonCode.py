import cv2
import numpy as np
import serial
import time

# Define range of green color and red color in HSV
green_lower = np.array([40, 50, 50])
green_upper = np.array([80, 255, 255])
red_lower = np.array([0, 50, 50])
red_upper = np.array([10, 255, 255])

# Open the default camera
cap = cv2.VideoCapture(0)

# Get the width and height of the video frame
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the x-coordinate of the vertical lines
line_x = int(frame_width / 3)
line_x2 = int(frame_width * 2 / 3)

# Define the kernel for morphological operations
kernel = np.ones((5, 5), np.uint8)

# Initialize the serial connection to the Arduino
#ser = serial.Serial('COM3', 9600)
#time.sleep(2)  # wait for the serial connection to be established

# Loop to capture frames from the camera
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Apply a Gaussian blur to the frame
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    # Convert the blurred frame to HSV color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only green colors
    mask_green = cv2.inRange(hsv, green_lower, green_upper)

    # Apply a morphological filter to remove noise
    mask_green = cv2.erode(mask_green, kernel)
    mask_green = cv2.dilate(mask_green, kernel)

    # Threshold the HSV image to get only red colors
    mask_red = cv2.inRange(hsv, red_lower, red_upper)

    # Apply a morphological filter to remove noise
    mask_red = cv2.erode(mask_red, kernel)
    mask_red = cv2.dilate(mask_red, kernel)

    # Find contours of green and red objects
    contours_green, hierarchy_green = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
    contours_red, hierarchy_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    # Loop through all detected contours
    for contour in contours_green + contours_red:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)

        # Only consider contours with area greater than 500 pixels
        if area > 500:
            # Draw a bounding box around the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            
            checker = np.isin(contour, contours_green).all(dtype=object)
            
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0) if checker else (0, 0, 255), 2)
            
           

            # Add a label to the top of the bounding box indicating whether it is a green or red object
            cv2.putText(frame, 'Green' if checker else 'Red', (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0) if checker else (0, 0, 255), 2)


            # Check if the object is to the left or right or inside the two lines
            if x + w < line_x:
                cv2.putText(frame, 'Left', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0) if checker else (0, 0, 255), 2)
                
                
                # Send command to the Arduino to turn left
                #ser.write(b'l\n')
            elif x > line_x2:
                cv2.putText(frame, 'Right', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0) if checker else (0, 0, 255), 2)
                # Send command to the Arduino to turn right
                #ser.write(b'r\n')
            else:
                cv2.putText(frame, 'Inside', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0) if checker else (0, 0, 255), 2)
                # Send command to the Arduino to moveforward
                #ser.write(b'f\n')


    # Draw the two vertical lines on the frame
    cv2.line(frame, (line_x, 0), (line_x, frame_height), (255, 0, 0), 2)
    cv2.line(frame, (line_x2, 0), (line_x2, frame_height), (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Green and Red Objects', frame)

    # Wait for a key press
    if cv2.waitKey(1) == ord('q'):
        break


# Release the camera, close all windows, and close the serial connection to the Arduino
cap.release()
cv2.destroyAllWindows()
#ser.close()