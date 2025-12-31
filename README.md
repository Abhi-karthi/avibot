This repository contains code that runs on a raspberry pi and any laptop to give a dashboard containing all the sensor outputs and a gui and controller that lets you move the robot.

If you have VNC installed, the inputs and outputs will be less laggy.

Steps if you have don't VNC installed:
1. Clone the branch: seperate-client-and-server on both the pi and your own computer that will be the client.
2. Push the arduino_nano_encoder_code.ino to the arduino nano. The arduino manages the motor encoder values and relays them to the pi.
3. Run drivebase.py on the pi. This creates a new server.
4. Run pip3 install pygame on your computer.
5. Now run main_frontend_client.py on your computer. If you get an error, it's likely because the connection broke or you ran the client before the server. To fix this, just change the port in both the client and server.

Steps if you do have VNC installed:
1. Open the pi's screen using VNC.
2. Clone the main branch
3. Run pip3 install pygame
4. Run main_frontend_client.py

The following are my configurations, if you are missing any/have extra, make sure to update that in drivebase.py or main_frontend_client.py. 
* 3 Ultrasonnic sensors (two in the front of the chassis, and one in the back)
* 4 IR sensors (all 4 in front of the chassis)
* 2 Encoded Motors (+ a deadwheel on the back)
* 1 Servo

Make sure your pins also match the one in the code. 
