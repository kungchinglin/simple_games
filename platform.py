# 1 - Import library
import pygame
from pygame.locals import *

import math

import random

print(dir(pygame))

# 2 - Initialize the game
class Player():

    _gravity = 0.1
    jump_speed_factor = 8
    move_speed = 0.3


    @property
    def gravity(self):
        return type(self)._gravity

    @gravity.setter
    def gravity(self, new_grav):
        type(self)._gravity = new_grav


    def __init__(self, pos, player_size = [30,50]):
        self.pos = pos
        self.vert = 0
        self.collide = [False, False, False, False]
        self.keys = [False, False, False, False]
        self.player_size = player_size

    def progressing(self):

        #Change vertical speed. Cap at maximum falling speed.

        #Case 1: The player is on the ground and is starting to jump.

        #Case 2: When the player is away from the ground.
        if self.collide[0]:
            self.vert *= -1
        elif not self.collide[2]:
            self.vert = max(self.vert - 0.01*self.gravity, -self.jump_speed_factor * self.gravity)
        else:
            if self.keys[0]:
                self.vert = self.jump_speed_factor * self.gravity
            else:
                self.vert = 0

        #Now, start to move. Note that the coordinate is reverted.

        self.pos[1] -= self.vert
        
        if self.keys[1] and not self.collide[1]:
            self.pos[0] -= self.move_speed
        if self.keys[3] and not self.collide[3]:
            self.pos[0] += self.move_speed

    
    def check_collide(self, blocks, block_size):

        colli_box = [0]*4


        for block in blocks:
            #Check if the block is above/below/left/right.

            #Case 1: the block is below:
            tolerance = 5

            if block[1] > self.pos[1] -tolerance  and  block[1] < self.pos[1] + self.player_size[1] + tolerance:
                if  self.pos[0] + self.player_size[0] -tolerance > block[0] and self.pos[0] +5 < block[0] + block_size:
                    colli_box[2] += 1
            
            #Case 2: the block is above:
            if block[1] > self.pos[1] - tolerance and block[1] < self.pos[1] + block_size + tolerance:
                if self.pos[0] + self.player_size[0] -tolerance > block[0] and self.pos[0] +5 < block[0] + block_size:              
                    colli_box[0] += 1
            
            #The sub-condition is never met. Why?

            #Case 3: the block is on the right:
            if block[0] > self.pos[0]   and  block[0] < self.pos[0] + self.player_size[0]:       
                if block[1] > self.pos[1] - block_size and block[1] < self.pos[1] + self.player_size[1]:
                    colli_box[3] += 1
            
            #Case 2: the block is on the left:
            if block[0] < self.pos[0] and block[0] > self.pos[0] -block_size:
                #light_rect = (block[0], block[1], 0.2*block_size, 0.2*block_size)
                #pygame.draw.rect(screen, YELLOW, light_rect)
                if block[1] > self.pos[1] - block_size and block[1] < self.pos[1] + self.player_size[1]:
                    colli_box[1] += 1
        
        self.collide = [colli_box[i] > 0 for i in range(4)]


    #This function is for debugging purposes.

    def lights_up(self, block, block_size):
        light_rect = (block[0], block[1], 0.2*block_size, 0.2*block_size)
        pygame.draw.rect(screen, YELLOW, light_rect)
        
    

        
        
    
    



player_size = [30,50]
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)

keys = [False, False, False, False]

player = Player([width//2, height//2], player_size)

block_size = 20


#Side wall and lower wall

blocks = [[x_pos * block_size, height-block_size] for x_pos in range(width//block_size)]
blocks.extend([[0, y_pos *block_size]  for y_pos in range(height//block_size)])
blocks.extend([[width-block_size, y_pos *block_size]  for y_pos in range(height//block_size)])


#Some walls in the middle

blocks.extend([[x_pos * block_size, height-5*block_size] for x_pos in range(10,width//block_size - 10)])

acc=[0,0]
arrows=[]


badtimer=100
badtimer1=0
badguys=[[640,100]]
healthvalue=194

pygame.mixer.init()


# 3 - Load images

wall = pygame.image.load("resources/images/wall.jpg")
wall = pygame.transform.scale(wall, (block_size, block_size))

mario = pygame.image.load("resources/images/mario_stand.png")
mario = pygame.transform.scale(mario, (player_size[0], player_size[1]))

mario_jump = pygame.image.load("resources/images/Mario_jump.jpg")
mario_jump = pygame.transform.scale(mario_jump, (player_size[0], player_size[1]))

player_rabbit = pygame.image.load("resources/images/dude.png")


grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")

arrow = pygame.image.load("resources/images/bullet.png")

badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg=badguyimg1

healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")

gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# 3.1 - Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


while True:
    # 5 - clear the screen before drawing it again
    screen.fill(0)

    #player_rect = (player.pos[0], player.pos[1], player.player_size[0], player.player_size[1])
    #small_rect = (player.pos[0], player.pos[1], 0.1*player.player_size[0], 0.1*player.player_size[1])
    #pygame.draw.rect(screen, BLUE, player_rect)
    #pygame.draw.rect(screen, GREEN, small_rect)

    if player.vert == 0:
        screen.blit(mario, (player.pos[0], player.pos[1]))
    else:
        screen.blit(mario_jump, (player.pos[0], player.pos[1]))



    for block in blocks:
        screen.blit(wall, (block[0], block[1]))
        #rect = (block[0], block[1], block_size, block_size)
        #small_rect = (block[0], block[1], 0.1*block_size, 0.1*block_size)
        #pygame.draw.rect(screen, RED, rect)
        #pygame.draw.rect(screen, GREEN, small_rect)


    player.check_collide(blocks, block_size)
    player.progressing()


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
                player.keys[0]=True
            elif event.key==K_a:
                player.keys[1]=True
            elif event.key==K_s:
                player.keys[2]=True
            elif event.key==K_d:
                player.keys[3]=True

        #For releasing the key, we reset our situation.
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_w:
                player.keys[0]=False
            elif event.key==pygame.K_a:
                player.keys[1]=False
            elif event.key==pygame.K_s:
                player.keys[2]=False
            elif event.key==pygame.K_d:
                player.keys[3]=False





# 4 - keep looping through
running = 1
exitcode = 0
while running:
    badtimer-=1


    badtimer-=1

    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))
    screen.blit(castle,(0,30))
    screen.blit(castle,(0,135))
    screen.blit(castle,(0,240))
    screen.blit(castle,(0,345 ))




    #screen.blit(player, playerpos)

    # 6.1 - Set player position and rotation
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1) 


    # 6.2 - Draw arrows
    for bullet in arrows:
        index=0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index+=1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))

    # 6.3 - Draw badgers
    if badtimer==0:
        badguys.append([640, random.randint(50,430)])
        badtimer=100-(badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
    index=0
    for badguy in badguys:
        if badguy[0]<-64:
            badguys.pop(index)
        badguy[0]-=5

        # 6.3.1 - Attack castle
        badrect=pygame.Rect(badguyimg.get_rect())
        badrect.top=badguy[1]
        badrect.left=badguy[0]
        if badrect.left<64:
            hit.play()
            healthvalue -= random.randint(5,20)
            badguys.pop(index)

        #6.3.2 - Check for collisions
        index1=0
        for bullet in arrows:
            bullrect=pygame.Rect(arrow.get_rect())
            bullrect.left=bullet[1]
            bullrect.top=bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0]+=1
                badguys.pop(index)
                arrows.pop(index1)
            index1+=1


        # 6.3.3 - Next bad guy
        index+=1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)

    # 6.4 - Draw clock
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(str(int((90000-pygame.time.get_ticks())/60000))+":"+str(int((90000-pygame.time.get_ticks())/1000%60)).zfill(2), True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright=[635,5]
    screen.blit(survivedtext, textRect)

    # 6.5 - Draw health bar
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8,8))



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
                keys[0]=True
            elif event.key==K_a:
                keys[1]=True
            elif event.key==K_s:
                keys[2]=True
            elif event.key==K_d:
                keys[3]=True

        #For releasing the key, we reset our situation.
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_w:
                keys[0]=False
            elif event.key==pygame.K_a:
                keys[1]=False
            elif event.key==pygame.K_s:
                keys[2]=False
            elif event.key==pygame.K_d:
                keys[3]=False


        #When the mouse is clicked, add arrow.
        if event.type==pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position=pygame.mouse.get_pos()
            acc[1]+=1
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])



    # 9 - Move player
    if keys[0]:
        playerpos[1]-=5
    elif keys[2]:
        playerpos[1]+=5
    if keys[1]:
        playerpos[0]-=5
    elif keys[3]:
        playerpos[0]+=5


    #10 - Win/Lose check
    if pygame.time.get_ticks()>=90000:
        running=0
        exitcode=1
    if healthvalue<=0:
        running=0
        exitcode=0
    if acc[1]!=0:
        accuracy=acc[0]*1.0/acc[1]*100
    else:
        accuracy=0

# 11 - Win/lose display        
if exitcode==0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()

