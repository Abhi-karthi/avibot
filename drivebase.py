import serial
import sys
import time
import RPi.GPIO as GPIO
import atexit
import signal
import threading
import socket
import values
import pygame

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '10.0.0.60'
# port = 12352
# s.bind((host, port))
# s.listen(5)
# print("Socket is listening")
# conn, addr = s.accept()
# print("Got a connection from ", addr, conn)

GPIO.setwarnings(False)
pygame.init()

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


def show_text(msg, x, y, color, size=32, font="Times new roman"):
    fontobj = pygame.font.SysFont(font, size)
    msgobj = fontobj.render(msg, False, color)
    screen.blit(msgobj, (x, y))


def handle_exit():
    print("this runs oafter keyboard interrupt")
    s.close()


atexit.register(GPIO.cleanup)
atext.register(handle_exit)

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

screen = pygame.display.set_mode((1400, 810))
pygame.display.set_caption("Avibot Front End Client")
slider_x = 103
danger_status_color = Colors.white
slider_drag = [False, 0]
speed_percentage = 25
speed_voltage = 3
robot = pygame.image.load("avibot_image.jpeg")
robot = pygame.transform.scale(robot, (142, 154))
left_ir_input = 0
left_ir_color = Colors.white
left_middle_ir_input = 0
left_middle_ir_color = Colors.white
right_middle_ir_input = 0
right_middle_ir_color = Colors.white
right_ir_input = 0
right_ir_color = Colors.white
left_ultrasonic_input = 0
left_ultrasonic_value = 0
right_ultrasonic_input = 0
right_ultrasonic_value = 0
back_ultra_sonic_input = 0
back_ultra_sonic_value = 0
left_motor_encoder_input = 0
left_motor_encoder_values = [0, 0]
right_motor_encoder_input = 0
right_motor_encoder_values = [0, 0]
motor_update_timer = time.time()
real_speed_and_direction = ["Coast", 0]
up_arrow_color = Colors.white
down_arrow_color = Colors.white
right_arrow_color = Colors.white
left_arrow_color = Colors.white
up_status = "0"
right_status = "0"
left_status = "0"
down_status = "0"



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

# input_list = ["0", "0", "0", "0", "25"]  # up, down, left, right, pwm
# output_list = ["", "", "", "", ".14", ".14", ".14", "", ""]  # left ir, left mid ir, right mid ir, right ir, left us, right us, back us, left encoder, right encoder


# def receive_data():
#     global input_list
#     while True:
#         data_received = conn.recv(1024).decode()
#         data_received = data_received.split(',')
#         try:
#             input_list = [data_received[0], data_received[1], data_received[2], data_received[3], data_received[4]]
#         except IndexError:
#             pass
        

def get_motor_encoder():
    global ser
    global left_motor_encoder_input
    global right_motor_encoder_input
    while True:
        try: 
            line = ser.readline().decode().strip()
            left_str, right_str = line.split(",")
            left_motor_encoder_input = str(float(left_str))
            right_motor_encoder_input = str(float(right_str))
        except (ValueError, UnicodeDecodeError):
            pass


def get_ultrasonic_values():
    global left_ultrasonic, right_ultrasonic, back_ultrasonic
    global left_ultrasonic_input, right_ultrasonic_input, back_ultra_sonic_input
    while True:
        left_ultrasonic_input = str(left_ultrasonic.get_distance())
        right_ultrasonic_input = str(right_ultrasonic.get_distance())
        back_ultra_sonic_input = str(back_ultrasonic.get_distance())


def get_infrared_values():
    global left_infrared, left_middle_infrared, right_middle_infrared, right_infrared
    global left_ir_input, left_middle_ir_input, right_middle_ir_input, right_ir_input
    while True:
        left_ir_input = str(left_infrared.black())
        left_middle_ir_input = str(left_middle_infrared.black())
        right_middle_ir_input = str(right_middle_infrared.black())
        right_ir_input = str(right_infrared.black())


# def send_data():
#     global output_list
#     while True:
#         conn.sendall(f"{output_list[0]},{output_list[1]},{output_list[2]},{output_list[3]},{output_list[4]},{output_list[5]},{output_list[6]},{output_list[7]},{output_list[8]}".encode())
        
       
get_motor_encoder_thread = threading.Thread(target=get_motor_encoder)       
get_ultrasonic_values_thread = threading.Thread(target=get_ultrasonic_values)       
get_infrared_values_thread = threading.Thread(target=get_infrared_values)       
# receive_data_thread = threading.Thread(target=receive_data)       
# send_data_thread = threading.Thread(target=send_data)            
  
get_motor_encoder_thread.start()       
get_ultrasonic_values_thread.start()       
get_infrared_values_thread.start()       
# receive_data_thread.start()       
# send_data_thread.start()       


clock = pygame.time.Clock()
fps = 60
while True:
    screen.fill(Colors.black)

    slider_bg = pygame.draw.rect(screen, Colors.grey, (50, 700, 250, 25))
    slider = pygame.draw.rect(screen, danger_status_color, (slider_x, 687, 20, 50))
    seperator = pygame.draw.rect(screen, Colors.grey, (0, 645, 1400, 15))
    screen.blit(robot, (629, 251))
    left_ir_circle = pygame.draw.circle(screen, left_ir_color, (652, 274), 3)
    left_middle_ir_circle = pygame.draw.circle(screen, left_middle_ir_color, (684, 263), 3)
    right_middle_ir_circle = pygame.draw.circle(screen, right_middle_ir_color, (720, 263), 3)
    right_ir_circle = pygame.draw.circle(screen, right_ir_color, (745, 274), 3)

    if left_ir_input == 0:  # This means it senses black
        left_ir_color = Colors.red
    else:
        left_ir_color = Colors.white
    if left_middle_ir_input == 0:
        left_middle_ir_color = Colors.red
    else:
        left_middle_ir_color = Colors.white
    if right_middle_ir_input == 0:
        right_middle_ir_color = Colors.red
    else:
        right_middle_ir_color = Colors.white
    if right_ir_input == 0:
        right_ir_color = Colors.red
    else:
        right_ir_color = Colors.white
    left_ultrasonic_value = (left_ultrasonic_input * 100)*154/25  # converts to cm, then to pixels
    left_ultrasonic_line = pygame.draw.line(screen, Colors.white, (658, 257), ((left_ultrasonic_value/3.6)*-2+658, (left_ultrasonic_value/3.6)*-3+257))
    show_text(f"{left_ultrasonic_input*100}cm", 659, 242, Colors.white, 10)
    right_ultrasonic_value = (right_ultrasonic_input * 100)*154/25
    right_ultrasonic_line = pygame.draw.line(screen, Colors.white, (748, 259), ((right_ultrasonic_value/3.6)*2+748, (right_ultrasonic_value/3.6)*-3+259))
    show_text(f"{right_ultrasonic_input*100}cm", 729, 240, Colors.white, 10)
    back_ultra_sonic_value = (back_ultra_sonic_input * 100)*154/25
    back_ultra_sonic_line = pygame.draw.line(screen, Colors.white, (697, 403), (697, 403 + back_ultra_sonic_value))
    show_text(f"{back_ultra_sonic_input*100}cm", 700, (403 + 403 + back_ultra_sonic_value)/2, Colors.white, 10)

    left_motor_encoder_values[1] = left_motor_encoder_values[0]
    right_motor_encoder_values[1] = right_motor_encoder_values[0]
    left_motor_encoder_values[0] = left_motor_encoder_input
    right_motor_encoder_values[0] = right_motor_encoder_input

    if left_motor_encoder_values[0] - left_motor_encoder_values[1] > 0 and right_motor_encoder_values[0] - right_motor_encoder_values[1] > 0:
        real_speed_and_direction = ["Forward", (((left_motor_encoder_values[0] - left_motor_encoder_values[1]) + (right_motor_encoder_values[0] - right_motor_encoder_values[1]))/2*100)/(time.time()-motor_update_timer)]
    elif left_motor_encoder_values[0] - left_motor_encoder_values[1] > 0 >= right_motor_encoder_values[0] - right_motor_encoder_values[1]:
        real_speed_and_direction = ["Turning right", ((left_motor_encoder_values[0] - left_motor_encoder_values[1])*100)/(time.time()-motor_update_timer)]
    elif left_motor_encoder_values[0] - left_motor_encoder_values[1] > 0 >= right_motor_encoder_values[0] - right_motor_encoder_values[1]:
        real_speed_and_direction = ["Turning left", ((right_motor_encoder_values[0] - right_motor_encoder_values[1])*100)/(time.time()-motor_update_timer)]
    elif left_motor_encoder_values[0] - left_motor_encoder_values[1] < 0 and right_motor_encoder_values[0] - right_motor_encoder_values[1] < 0:
        real_speed_and_direction = ["Backward", (((left_motor_encoder_values[0] - left_motor_encoder_values[1]) + (right_motor_encoder_values[0] - right_motor_encoder_values[1]))/2*100)/(time.time()-motor_update_timer)]
    else:
        real_speed_and_direction = ["Coast", 0]
    motor_update_timer = time.time()
    show_text(f"{real_speed_and_direction[0]}   {real_speed_and_direction[1]} cm/s", 395, 717, Colors.white, 25)
    # show_text(f"{}")

    up_arrow = pygame.draw.rect(screen, up_arrow_color, (1026, 710, 50, 25))
    show_text("^", 1044, 712, Colors.black, 25)
    down_arrow = pygame.draw.rect(screen, down_arrow_color, (1026, 735, 50, 25))
    show_text("⬇", 1044, 741, Colors.black, 25)
    left_arrow = pygame.draw.rect(screen, left_arrow_color, (976, 735, 50, 25))
    show_text("<", 1000, 740, Colors.black, 25)
    right_arrow = pygame.draw.rect(screen, right_arrow_color, (1076, 735, 50, 25))
    show_text(">", 1096, 740, Colors.black, 25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if slider.collidepoint(event.pos):
                    slider_drag = [True, event.pos[0]]

        if event.type == pygame.MOUSEMOTION:
            slider_drag[1] = event.pos[0]
            print(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                slider_drag = [False, 0]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up_arrow_color = Colors.green
                down_arrow_color = Colors.white
                right_arrow_color = Colors.white
                left_arrow_color = Colors.white
                up_status = "1"
                down_status = "0"
                right_status = "0"
                left_status = "0"
            elif event.key == pygame.K_DOWN:
                up_arrow_color = Colors.white
                down_arrow_color = Colors.green
                right_arrow_color = Colors.white
                left_arrow_color = Colors.white
                up_status = "0"
                down_status = "1"
                right_status = "0"
                left_status = "0"
            elif event.key == pygame.K_RIGHT:
                up_arrow_color = Colors.white
                down_arrow_color = Colors.white
                right_arrow_color = Colors.green
                left_arrow_color = Colors.white
                up_status = "0"
                down_status = "0"
                right_status = "1"
                left_status = "0"
            elif event.key == pygame.K_LEFT:
                up_arrow_color = Colors.white
                down_arrow_color = Colors.white
                right_arrow_color = Colors.white
                left_arrow_color = Colors.green
                up_status = "0"
                down_status = "0"
                right_status = "0"
                left_status = "1"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up_arrow_color = Colors.white
                up_status = "0"
            elif event.key == pygame.K_DOWN:
                down_arrow_color = Colors.white
                down_status = "0"
            elif event.key == pygame.K_RIGHT:
                right_arrow_color = Colors.white
                right_status = "0"
            elif event.key == pygame.K_LEFT:
                left_arrow_color = Colors.white
                left_status = "0"

    if slider_drag[0] and 48 < slider_drag[1] < 304:
        slider_x = slider_drag[1] - 10
        print(slider_x, slider_drag)

    speed_percentage = int(((slider_x + 10) - 50)*10/25)
    speed_voltage = ((slider_x + 10) - 50)*12/250

    if speed_percentage > 100:
        speed_percentage = 100
    if speed_voltage > 12:
        speed_voltage = 12

    show_text(f"{speed_percentage}%", 100, 775, danger_status_color, 25)
    show_text(f"{speed_voltage}V", 200, 775, danger_status_color, 25)

    if slider_x + 10 > 175:
        danger_status_color = Colors.red
        show_text("Warning! Motors are only rated at 6V.", 60, 735, Colors.red, 15)
        show_text("Higher voltage may cause burnouts.", 60, 755, Colors.red, 15)
    else:
        danger_status_color = Colors.white

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

    clock.tick(fps)
    pygame.display.update()
