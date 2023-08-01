## McQueen
**Design Process of Self-Driving Car for WRO Competition**

#1. Introduction:
   The purpose of this report is to outline the design process of a self-driving car for the World Robot Olympiad (WRO) competition. The car is equipped with one rear driving motor and one steering motor, both of which are DC motors controlled by an L298N motor driver. Additionally, the robot incorporates three Time-of-Flight (ToF) sensors located in the front, right, and left sides, connected to an Arduino via an I2C hub. The Arduino further communicates with a Raspberry Pi 4, which uses a camera for obstacle detection.

#2. Requirements Analysis:
   Before starting the design process, it is crucial to identify the requirements and constraints of the self-driving car for the WRO competition. This includes factors such as size limitations, power source, weight restrictions, and specific rules set by the competition.

#3. Mechanical Design:
   The mechanical design of the self-driving car involves creating a sturdy and lightweight chassis to accommodate the required components. The chassis should be designed to fit the dimensions specified by the competition rules. The rear driving motor and the steering motor should be securely mounted, ensuring proper alignment with the wheels. The chassis should also provide suitable space for the placement of the Arduino, Raspberry Pi, and other electronic components.

#4. Electrical Design:
   The electrical design focuses on creating a reliable and efficient power supply system. The DC motors (rear driving motor and steering motor) are controlled using an L298N motor driver, which provides the necessary voltage and current to drive the motors. The motor driver is connected to the Arduino, which receives signals and commands from the Raspberry Pi for motor control. The Arduino, in turn, communicates with the Raspberry Pi using suitable interface protocols.

#5. Sensor Integration:
   The self-driving car incorporates three ToF sensors, positioned in the front, right, and left directions. These sensors use infrared light to measure the distance between the car and nearby obstacles. The sensors are connected to an I2C hub, which allows multiple sensors to communicate with the Arduino using a single interface. The Arduino processes the sensor data and makes decisions based on the detected obstacle distances.

#6. Software Development:
   The software development involves programming the Arduino and Raspberry Pi to enable autonomous driving and obstacle detection. The Arduino code reads the data from the ToF sensors and sends it to the Raspberry Pi for processing. The Raspberry Pi uses computer vision algorithms to analyze the camera feed, detect obstacles, and send appropriate commands to the Arduino for motor control. The software should be designed to ensure quick and accurate decision-making to navigate the car effectively.

#7. Testing and Calibration:
   After completing the hardware and software integration, extensive testing and calibration are necessary to ensure the self-driving car performs optimally. The car should be tested in various scenarios simulating the competition environment, including different obstacle configurations, varying light conditions, and different surface conditions. Testing helps identify and address any issues, such as sensor inaccuracies or software bugs, improving the overall performance of the car.

#8. Optimization and Refinement:
   Through testing, the self-driving car's performance can be evaluated, and areas for improvement can be identified. Optimization and refinement may involve adjusting the control algorithms, fine-tuning sensor calibration, optimizing power consumption, or enhancing obstacle detection accuracy. This iterative process continues until the car meets the desired performance standards.

#9. Conclusion:
   The design process of the self-driving car for the WRO competition involves careful consideration of mechanical, electrical, and software aspects. By integrating the rear driving motor, steering motor, ToF sensors, Arduino, and Raspberry Pi, a robust and autonomous vehicle can be developed. Thorough testing, calibration, and optimization are key to achieving a high-performance self-driving car that can successfully navigate obstacles and meet the competition requirements.
