import cv2
import numpy as np
import serial
import time
import threading
from queue import Queue



class ObjectTracker:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.green_lower = np.array([40, 50, 50])
        self.green_upper = np.array([80, 255, 255])
        self.red_lower = np.array([0, 50, 50])
        self.red_upper = np.array([10, 255, 255])
        self.line_x = int(width / 3)
        self.line_x2 = int(width * 2 / 3)
        self.kernel = np.ones((5, 5), np.uint8)
        self.running = False
        self.frame_queue = Queue(maxsize=1)
        self.color = None
        self.x = None
        self.w = None
        self.last_x = None
        #self.ser = serial.Serial('COM9', 9600)


    def start(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Cannot open camera")
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        threading.Thread(target=self._capture_frames, daemon=True).start()
        threading.Thread(target=self._detect_objects, daemon=True).start()
        threading.Thread(target=self._send_commands, daemon=True).start()

    def stop(self):
        self.running = False
        cv2.destroyAllWindows()
        self.cap.release()
        self.ser.close()

    def _capture_frames(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            if self.frame_queue.full():
                self.frame_queue.get()
            self.frame_queue.put(frame)

    def _detect_objects(self):
        while self.running:
            try:
                frame = self.frame_queue.get(timeout=1)
            except:
                continue

            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            mask_green = cv2.inRange(hsv, self.green_lower, self.green_upper)
            mask_green = cv2.erode(mask_green, self.kernel)
            mask_green = cv2.dilate(mask_green, self.kernel)

            mask_red = cv2.inRange(hsv, self.red_lower, self.red_upper)
            mask_red = cv2.erode(mask_red, self.kernel)
            mask_red = cv2.dilate(mask_red, self.kernel)

            contours_green, hierarchy_green = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
            contours_red, hierarchy_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

            if len(contours_green) == 0 and len(contours_red) == 0:
                continue

            for contour in contours_green + contours_red:
                area = cv2.contourArea(contour)

                if area > 500:
                    x, y, self.w, h = cv2.boundingRect(contour)
                    self.color = 'Green' if contour in contours_green else 'Red'
                    self.x = x

                    # Draw the bounding box and label on the frame
                    cv2.rectangle(frame, (x, y), (x + self.w, y + h), (0, 255, 0) if self.color == 'Green' else (0, 0, 255), 2)
                    cv2.putText(frame, self.color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) if self.color == 'Green' else (0, 0, 255), 2)

                    break

            # Draw the two vertical lines on the frame
            cv2.line(frame, (self.line_x, -10), (self.line_x, self.height), (255, 0, 0), 2)
            cv2.line(frame, (self.line_x2, 0), (self.line_x2, self.height), (255, 0, 0), 2)

            cv2.imshow('Object Tracker', frame)
            
            # Wait for a key press
            if cv2.waitKey(1) == ord('q'):
                break


    def _send_commands(self):
        while self.running:
            if self.color is not None and self.x is not None and self.w is not None:
                if self.last_x is not None:
                    if self.x + self.w < self.line_x and self.last_x + self.w >= self.line_x:
                        pass
                        #self.ser.write(b'l\n')
                    elif self.x > self.line_x2 and self.last_x <= self.line_x2:
                        pass
                        #self.ser.write(b'r\n')
                    else:
                        pass
                        #self.ser.write(b'f\n')
                self.last_x = self.x
                self.color = None
                self.x = None
                self.w = None

            time.sleep(0.1)

    def get_frame(self):
        try:
            return self.frame_queue.get(timeout=1)
        except:
            return None

if __name__ == '__main__':
    # Create an ObjectTracker instance with a resolution of 320x240
    tracker = ObjectTracker(320, 240)

    # Start the object tracking and control system
    tracker.start()

    # Wait for the user to press any key to stop the system
    while cv2.waitKey(1) & 0xFF == 0xFF:
        pass

    # Stop the system
    tracker.stop()