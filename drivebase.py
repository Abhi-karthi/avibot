import serial
import sys
import time
import RPi.GPIO as GPIO
import atexit
import signal
import threading
import socket
# import pygame

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '172.28.212.143'
port = 12349
s.bind((host, port))
s.listen(5)
print("Socket is listening")
conn, addr = s.accept()
print("Got a connection from ", addr, conn)

GPIO.setwarnings(False)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN)
GPIO.setup(23, GPIO.IN)                                
GPIO.setup(33, GPIO.IN)
GPIO.setup(18, GPIO.IN)          
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.OUT)   
GPIO.setup(5, GPIO.IN)  
GPIO.setup(7, GPIO.OUT)
GPIO.setup(21, GPIO.IN)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(10, GPIO.IN)

atexit.register(GPIO.cleanup)


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

class Ultrasonic:
    def __init__(self, echo: int, trig: int):
        self.echo = echo
        self.trig = trig

    def get_distance(self) -> float:
        GPIO.output(self.trig, 1)
        time.sleep(0.00001)
        GPIO.output(self.trig, 0)
        start_time = time.time()
        while GPIO.input(self.echo) != 1:
            pass

        distance = ((1/2)*(time.time()-start_time+0.00001)*345.86)
        if distance > .35:
            distance = .35
        return distance


class Infrared:
    def __init__(self, output: int):
        self.output = output
    
    def black(self) -> int:
        return GPIO.input(self.output)
        

class Motor:
    def __init__(self, forward_pin: int, backward_pin: int, pwm_pin=None):
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        if pwm_pin is not None:
            self.pwm_pin = GPIO.PWM(pwm_pin, 1000)
            self.pwm_pin.start(0)
        self.speed = 50
    
    def forward(self, speed=None) -> None:
        if speed is not None:
            self.speed = int(speed)
            if self.speed > 100:
                self.speed = 100
            elif self.speed < 0:
                self.speed = 0
        self.pwm_pin.ChangeDutyCycle(int(self.speed))
        GPIO.output(self.forward_pin, 1)
        GPIO.output(self.backward_pin, 0)
    
    def backward(self, speed=None) -> None:
        if speed is not None:
            self.speed = int(speed)
            if self.speed > 100:
                self.speed = 100
            elif self.speed < 0:
                self.speed = 0
        self.pwm_pin.ChangeDutyCycle(int(self.speed))
        GPIO.output(self.backward_pin, 1)
        GPIO.output(self.forward_pin, 0)
    
    def coast(self) -> None:
        GPIO.output(self.forward_pin, 0)
        GPIO.output(self.backward_pin, 0)
    
    def hold(self, power=50) -> None:
        self.pwm_pin.ChangeDutyCycle(int(power))  # Assuming 50% duty cycle for holding
        GPIO.output(self.forward_pin, 1)
        GPIO.output(self.backward_pin, 1)


class Servo:
    def __init__(self, output: int, starting_pos=None):
        self.output = output
        if starting_pos != None:
            self.rotate(starting_pos)

    def rotate(self, degree: int) -> None:
        GPIO.output(self.output, 1)
        time.sleep((degree / 90) * 0.001)
        GPIO.output(self.output, 0)


left_ultrasonic = Ultrasonic(11, 13)
right_ultrasonic = Ultrasonic(5, 7)
back_ultrasonic = Ultrasonic(21, 19)
left_infrared = Infrared(16)
left_middle_infrared = Infrared(23)
right_middle_infrared = Infrared(33)
right_infrared = Infrared(18)
left_motor = Motor(38, 40, 32)
right_motor = Motor(31, 29, 12)

input_list = ["0", "0", "0", "0", "25"]  # up, down, left, right, pwm
output_list = ["", "", "", "", ".14", ".14", ".14", "", ""]  # left ir, left mid ir, right mid ir, right ir, left us, right us, back us, left encoder, right encoder


def receive_data():
    global input_list
    while True:
        data_received = conn.recv(1024).decode()
        data_received = data_received.split(',')
        try:
            input_list = [data_received[0], data_received[1], data_received[2], data_received[3], data_received[4]]
        except IndexError:
            pass
        

def get_motor_encoder():
    global ser
    global output_list
    while True:
        try: 
            line = ser.readline().decode().strip()
            left_str, right_str = line.split(",")
            output_list[7] = str(float(left_str))
            output_list[8] = str(float(right_str))
        except (ValueError, UnicodeDecodeError):
            pass


def get_ultrasonic_values():
    global left_ultrasonic, right_ultrasonic, back_ultrasonic
    global output_list
    while True:
        output_list[4] = str(left_ultrasonic.get_distance())
        output_list[5] = str(right_ultrasonic.get_distance())
        output_list[6] = str(back_ultrasonic.get_distance())


def get_infrared_values():
    global left_infrared, left_middle_infrared, right_middle_infrared, right_infrared
    global output_list
    while True:
        output_list[0] = str(left_infrared.black())
        output_list[1] = str(left_middle_infrared.black())
        output_list[2] = str(right_middle_infrared.black())
        output_list[3] = str(right_infrared.black())


def send_data():
    global output_list
    while True:
        conn.sendall(f"{output_list[0]},{output_list[1]},{output_list[2]},{output_list[3]},{output_list[4]},{output_list[5]},{output_list[6]},{output_list[7]},{output_list[8]}".encode())
        
       
get_motor_encoder_thread = threading.Thread(target=get_motor_encoder)       
get_ultrasonic_values_thread = threading.Thread(target=get_ultrasonic_values)       
get_infrared_values_thread = threading.Thread(target=get_infrared_values)       
receive_data_thread = threading.Thread(target=receive_data)       
send_data_thread = threading.Thread(target=send_data)            
  
get_motor_encoder_thread.start()       
#get_ultrasonic_values_thread.start()       

get_infrared_values_thread.start()       
receive_data_thread.start()       
send_data_thread.start()       

while True:
    if input_list[0] == "1":       
        left_motor.forward(input_list[4])       
        right_motor.forward(input_list[4])     
    elif input_list[1] == "1":       
        left_motor.backward(input_list[4])       
        right_motor.backward(input_list[4])       
    elif input_list[2] == "1":       
        left_motor.backward(input_list[4])       
        right_motor.forward(input_list[4])
    elif input_list[3] == "1":       
        left_motor.forward(input_list[4])       
        right_motor.backward(input_list[4])
    else:
        left_motor.coast()
        right_motor.coast()

