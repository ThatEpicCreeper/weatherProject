import socket
import pygame as pg
import sys

# Client setup
SERVER = '192.168.171.97'  # Server IP
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER, PORT))
print("Connected to the server!")

# Pygame setup
pg.init()
WIDTH, HEIGHT = 400, 300
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Number Guessing Game")
font = pg.font.SysFont("Consolas", 24)

# Game variables
input_box = pg.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
response = ''

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            client_socket.close()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicks on the input box
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive

        if event.type == pg.KEYDOWN:
            if active:
                if event.key == pg.K_RETURN:
                    # Send guess to the server
                    try:
                        guess = int(text)
                        client_socket.send(text.encode())
                        response = client_socket.recv(1024).decode()
                        if response == "Correct!":
                            response = "You guessed it! Press ESC to quit."
                        text = ''
                    except ValueError:
                        response = "Enter a valid number."
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    # Drawing
    screen.fill((30, 30, 30))
    txt_surface = font.render(text, True, color)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))
    pg.draw.rect(screen, color, input_box, 2)

    # Display response
    if response:
        response_surface = font.render(response, True, pg.Color("white"))
        screen.blit(response_surface, (WIDTH // 2 - response_surface.get_width() // 2, HEIGHT // 2 + 50))

    pg.display.flip()
