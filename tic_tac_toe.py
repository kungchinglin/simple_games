# 1 - Import library
import pygame
from pygame.locals import *

import math

import random


# 2 - Initialize the game
pygame.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height))

# 2.1 - label 1 if circle, -1 if cross
label = -1

# 3 - Draw lines.

WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0) 

up_1 = height // 3
up_2 = height * 2 // 3

left_1 = width // 3
left_2 = width * 2 // 3


# 3.1 - Parameters.

radius = 50
Board = [[0]*3 for _ in range(3)]
Running = 1
total_steps = 0

# 4 - Define utility functions.

def check_winner(Board):
    
    #There is a bingo if the sum of those three indices is 3 or -3.

    if abs(Board[0][0] + Board[1][0] + Board[2][0]) == 3:
        return Board[0][0]
    
    if abs(Board[0][0] + Board[0][1] + Board[0][2]) == 3:
        return Board[0][0]
    
    if abs(Board[0][0] + Board[1][1] + Board[2][2]) == 3:
        return Board[0][0]

    if abs(Board[1][0] + Board[1][1] + Board[1][2]) == 3:
        return Board[1][0]

    if abs(Board[2][0] + Board[2][1] + Board[2][2]) == 3:
        return Board[2][0]

    if abs(Board[2][0] + Board[1][1] + Board[0][2]) == 3:
        return Board[2][0]

    if abs(Board[0][1] + Board[1][1] + Board[2][1]) == 3:
        return Board[0][1]

    if abs(Board[0][2] + Board[1][2] + Board[2][2]) == 3:
        return Board[0][2]

    


    return 0




while Running:

    # 5 - clear the screen before drawing it again
    screen.fill(0)


    pygame.draw.line(screen, RED, [left_1, 0], [left_1, height])
    pygame.draw.line(screen, RED, [left_2, 0], [left_2, height])
    pygame.draw.line(screen, RED, [0, up_1], [width, up_1])
    pygame.draw.line(screen, RED, [0, up_2], [width, up_2])


    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            exit(0) 


        #When the mouse is clicked, add circle or cross.
        if event.type==pygame.MOUSEBUTTONDOWN:
            position=pygame.mouse.get_pos()

            pos_x  =  position[0]*3//width

            pos_y  =  position[1]*3//height

            if pos_x < 0 or pos_x > 2 or pos_y < 0 or pos_y > 2:
                print("Out of place!", pos_x, pos_y)
                break

            if Board[pos_x][pos_y] == 0:
                Board[pos_x][pos_y] = label


                total_steps += 1
                label *= -1

    for Pos_x in range(3):
        for Pos_y in range(3):
            
            center_x = (Pos_x+ 0.5) * width//3
            center_y = (Pos_y+ 0.5) * height//3

            if Board[Pos_x][Pos_y] == 1:
                pygame.draw.circle(screen, RED, (center_x , center_y) , radius, 10) 

            if Board[Pos_x][Pos_y] == -1:
                half_length = 40
                pygame.draw.line(screen, RED, [center_x - half_length , center_y - half_length], [center_x + half_length , center_y + half_length], width = 10)
                pygame.draw.line(screen, RED, [center_x + half_length , center_y - half_length], [center_x - half_length , center_y + half_length], width = 10)



    pygame.display.flip()




    # Check if the game is over.



    exitcode = check_winner(Board)

    if exitcode == 0 and total_steps == 9:
        exitcode = 2
        Running = 0

    elif exitcode != 0:

        Running = 0

pygame.font.init()
font = pygame.font.Font(None, 50)
if exitcode == 1:
    text = font.render("Circle wins.", True, (255,255,255))
elif exitcode == -1:
    text = font.render("Cross wins.", True, (255,255,255))
else:
    text = font.render("It's a draw.", True, (255,255,255))


textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery+24
        #screen.blit(gameover, (0,0))
screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()

 


