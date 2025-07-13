from values import Colors
import pygame
import sockets

pygame.init()


def show_text(msg, x, y, color, size=32, font="Times new roman"):
    fontobj = pygame.font.SysFont(font, size)
    msgobj = fontobj.render(msg, False, color)
    screen.blit(msgobj, (x, y))


screen = pygame.display.set_mode((1400, 810))
pygame.display.set_caption("Avibot Front End Client")

slider_x = 103
danger_status_color = Colors.white
slider_drag = [False, 0]
speed_percentage = 25
speed_voltage = 3
robot = pygame.image.load("avibot_image.jpeg")
robot = pygame.transform.scale(robot, (284, 308))
left_ir_input = 0
left_ir_color = Colors.red
left_middle_ir_input = 0
left_middle_ir_color = Colors.red
right_middle_ir_input = 0
right_middle_ir_color = Colors.red
right_ir_input = 0
right_ir_color = Colors.red
left_ultrasonic_input = 0
right_ultrasonic_input = 0
back_ultra_sonic_input = 0
left_motor_encoder = 0
right_motor_encoder = 0

clock = pygame.time.Clock()
fps = 60
while True:
    screen.fill(Colors.black)
    slider_bg = pygame.draw.rect(screen, Colors.grey, (50, 700, 250, 25))
    slider = pygame.draw.rect(screen, danger_status_color, (slider_x, 687, 20, 50))
    seperator = pygame.draw.rect(screen, Colors.grey, (0, 645, 1400, 15))
    left_ir_circle = pygame.draw.circle(screen, left_ir_color, (598, 303), 3)
    left_middle_ir_circle = pygame.draw.circle(screen, left_middle_ir_color, (669, 277), 3)
    right_middle_ir_circle = pygame.draw.circle(screen, right_middle_ir_color, (741, 277), 3)
    right_ir_circle = pygame.draw.circle(screen, right_ir_color, (809, 304), 3)
    screen.blit(robot, (558, 251))

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
