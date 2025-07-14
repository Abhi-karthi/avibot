from values import Colors
import threading
import atexit
import pygame
import time
import socket

pygame.init()


def show_text(msg, x, y, color, size=32, font="Times new roman"):
    fontobj = pygame.font.SysFont(font, size)
    msgobj = fontobj.render(msg, False, color)
    screen.blit(msgobj, (x, y))


def handle_exit():
    print("This runs after keyboard interrupt")
    s.close()


atexit.register(handle_exit)
host = "10.0.0.60"
port = 12348
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("connected")
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
left_ir_color = Colors.red
left_middle_ir_input = 0
left_middle_ir_color = Colors.red
right_middle_ir_input = 0
right_middle_ir_color = Colors.red
right_ir_input = 0
right_ir_color = Colors.red
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


def receive_data():
    global left_ir_input, left_middle_ir_input, right_middle_ir_input, right_ir_input
    global left_ultrasonic_input, right_ultrasonic_input, back_ultra_sonic_input
    global left_motor_encoder_input, right_motor_encoder_input
    while True:
        data_received = s.recv(1024).decode()
        data_received = data_received.split(",")
        print(data_received)

        left_ir_input = data_received[0]
        left_middle_ir_input = data_received[1]
        right_middle_ir_input = data_received[2]
        right_ir_input = data_received[3]

        left_ultrasonic_input = data_received[4]
        right_ultrasonic_input = data_received[5]
        back_ultra_sonic_input = data_received[6]

        left_motor_encoder_input = data_received[7]
        right_motor_encoder_input = data_received[8]


def send_data():
    global up_status, down_status, left_status, right_status  # seperating
    global speed_percentage
    while True:
        s.sendall(f"{up_status},{down_status},{left_status},{right_status},{str(speed_percentage)}".encode())


receive_data_thread = threading.Thread(target=receive_data)
send_data_thread = threading.Thread(target=send_data)
receive_data_thread.start()
send_data_thread.start()
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

    clock.tick(fps)
    pygame.display.update()
