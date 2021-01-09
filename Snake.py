# 1 - Import library
import pygame
from pygame.locals import *

import math

import random


# 2 - Initialize the game
pygame.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height))

square_size = 20

keys = [False, False, False, False]

BLUE = (0,0,255)
RED = (255,0,0)

snake_pos = []

treat_pos = []

timer = 0

start_move_time = 2000

# 1 is right, -1 is left, 2 is down, -2 is up.

direction = 1

prev_dir = 1


# 3 - Function to draw the snake and the treat, check collision, and generate treat

def draw_squares(snake_pos, is_snake, square_size = 20):
    for pos in snake_pos:
        rect = (pos[0]*square_size, pos[1]*square_size, square_size, square_size)
        if is_snake:
            pygame.draw.rect(screen, BLUE, rect)
        else:
            pygame.draw.rect(screen, RED, rect)
    



def check_collision(snake_pos, square_size = 20):

    # Check if the snake goes out of bound
    if snake_pos[-1][0] < 0 or snake_pos[-1][0] > width//square_size -1 or snake_pos[-1][1] < 0 or snake_pos[-1][1] > height//square_size -1:
        return True
    
    # Check if the snake collides with itself

    collision_set = [pos for pos in snake_pos if pos == snake_pos[-1]]

    if len(collision_set) > 1:
        return True
    
    return False

def gen_treat(snake_pos, treat_pos):
    while True:
        new_pos = (random.randint(0,width//square_size - 1), random.randint(0,height//square_size - 1))

        collision = 0

        for pos in snake_pos:
            if new_pos == pos:
                collision = 1
                break
        
        for pos in treat_pos:
            if new_pos == pos:
                collision = 1
                break
        
        if collision == 0:
            treat_pos.append(new_pos)
            return
        



# 4 - Start the game



gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)

# 4.0 - Before looping, generate the snake and the treat.
tail_pos = (random.randint(0,width//square_size-10), random.randint(0,height//square_size))

snake_pos.append(tail_pos)
snake_pos.append((tail_pos[0]+1, tail_pos[1]))
snake_pos.append((tail_pos[0]+2, tail_pos[1]))

gen_treat(snake_pos,treat_pos)

while True:

    move_time = max(start_move_time// len(snake_pos), 150)


    # 4.01 - clear the screen before drawing it again
    screen.fill(0)

    # 4.1 - Update timer.
    timer += 1

    # 4.2 - If the time is up, reset the time and let the snake move.

    if timer >= move_time:
        timer = 0
        last_pos = snake_pos[-1]
        # If the supposed direction is opposite to the previous direction, we ignore the command and let it go the same direction as before.
        if abs(direction) == abs(prev_dir):
            direction = prev_dir

        if direction != 1 and direction != -1 and direction != 2 and direction != -2:
            print("Unexpected direction!")
            direction = 1


        if direction == 1:
            snake_pos.append((last_pos[0]+1, last_pos[1]))
        elif direction == -1:
            snake_pos.append((last_pos[0]-1, last_pos[1]))
        elif direction == 2:
            snake_pos.append((last_pos[0], last_pos[1]+1))
        elif direction == -2:
            snake_pos.append((last_pos[0], last_pos[1]-1))
            
        prev_dir = direction


        # 4.3 - Check if the snake got the treat.

        got_treat = False

        for treat in treat_pos:
            if snake_pos[-1] == treat:
                got_treat = True
                break
        
        if got_treat:
            treat_pos.remove(snake_pos[-1])
            gen_treat(snake_pos, treat_pos)
        else:
            #If the snake didn't get the treat, it does not get longer.
            snake_pos.pop(0)

        # 4.4 - Check if the snake collided.

        if check_collision(snake_pos):
            break


    draw_squares(snake_pos, True, square_size)
    #shoot.play()
    draw_squares(treat_pos, False, square_size)


    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            exit(0) 


        #For pressing down the key for WASD, we perform some actions.
        if event.type == pygame.KEYDOWN:
            if event.key==K_w:
                direction = -2
            elif event.key==K_a:
                direction = -1
            elif event.key==K_s:
                direction = 2
            elif event.key==K_d:
                direction = 1



pygame.font.init()
font = pygame.font.Font(None, 24)
text = font.render("Snake length: "+str(len(snake_pos)), True, (0,255,255))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery+24
screen.blit(gameover, (0,0))
screen.blit(text, textRect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
