# 1 - Import library
import pygame
from pygame.locals import *

import math

import random

print(dir(pygame))

# 2 - Initialize the game
class GameObject():

    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.collide = [False]*4
    
    def check_collide(self, blocks):

        colli_box = [0]*4


        for block in blocks:
            #Check if the block is above/below/left/right.

            #Case 1: the block is below:
            tolerance = 5

            if block.pos[1] > self.pos[1] + self.size[1] -tolerance  and  block.pos[1] < self.pos[1] + self.size[1] + tolerance:
                if  self.pos[0] + self.size[0] -tolerance > block.pos[0] and self.pos[0] + tolerance < block.pos[0] + block.size[0]:
                    colli_box[2] += 1
            
            #Case 2: the block is above:
            if block.pos[1] + block.size[1] > self.pos[1] - tolerance and block.pos[1] + block.size[1] < self.pos[1]  + tolerance:
                if self.pos[0] + self.size[0] -tolerance > block.pos[0] and self.pos[0] +5 < block.pos[0] + block.size[0]:              
                    colli_box[0] += 1
            
            #The sub-condition is never met. Why?

            #Case 3: the block is on the right:
            if block.pos[0] > self.pos[0]   and  block.pos[0] < self.pos[0] + self.size[0]:       
                if block.pos[1] > self.pos[1] - block.size[1] and block.pos[1] < self.pos[1] + self.size[1]:
                    colli_box[3] += 1
            
            #Case 2: the block is on the left:
            if block.pos[0] < self.pos[0] and block.pos[0] > self.pos[0] -block.size[0]:
                #light_rect = (block[0], block[1], 0.2*block_size, 0.2*block_size)
                #pygame.draw.rect(screen, YELLOW, light_rect)
                if block.pos[1] > self.pos[1] - block.size[1] and block.pos[1] < self.pos[1] + self.size[1]:
                    colli_box[1] += 1
        
        self.collide = [colli_box[i] > 0 for i in range(4)]


    def got_hit_any(self, objs):
        tolerance = 5
        for obj in objs:
            if obj.pos[0] + obj.size[0] > self.pos[0] - tolerance and obj.pos[0] < self.pos[0] + self.size[0] + tolerance:
                if obj.pos[1] + obj.size[1] > self.pos[1] - tolerance and obj.pos[1] < self.pos[1] + self.size[1] + tolerance:
                    return True
        
        return False


class Player(GameObject):

    _gravity = 0.1
    jump_speed_factor = 7
    move_speed = 0.3


    @property
    def gravity(self):
        return type(self)._gravity

    @gravity.setter
    def gravity(self, new_grav):
        type(self)._gravity = new_grav


    def __init__(self, pos, size = [30,50]):
        super(Player, self).__init__(pos, size)
        self.vert = 0
        self.keys = [False, False, False, False]
        self.face_right = True

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


    #This function is for debugging purposes.

    def lights_up(self, block, block_size):
        light_rect = (block[0], block[1], 0.2*block_size, 0.2*block_size)
        pygame.draw.rect(screen, YELLOW, light_rect)
        
    
# Create monsters.
        
class Monster(Player):
    
    jump_speed_factor = 4

    def __init__(self, pos, size = [30,30], key = "right"):
        super(Monster, self).__init__(pos, size)
        if key == "right":
            self.keys = [False, False, False, True]
        else:
            self.keys = [False, True, False, False]

    def progressing(self):
        
        if not self.collide[2]:
            self.vert = max(self.vert - 0.01*self.gravity, -self.jump_speed_factor * self.gravity)
        else:
            self.vert = 0

        self.pos[1] -= self.vert

        
        if self.keys[1]:
            if not self.collide[1]:
                self.pos[0] -= self.move_speed
            else:
                self.keys[1], self.keys[3] = False, True
                self.pos[0] += self.move_speed
        elif self.keys[3]:
            if not self.collide[3]:
                self.pos[0] += self.move_speed
            else:
                self.keys[3], self.keys[1] = False, True
                self.pos[0] -= self.move_speed
    
    def __del__(self):
        #Want to maybe add a sound of explosion.
        pass

# Create projectiles.
class Projectiles(GameObject):

    move_speed = 0.5
    angle_fac = 0.5

    def __init__(self, pos, size=[10, 10], face_right=True):
        super(Projectiles, self).__init__(pos, size)
        self.vel = [self.move_speed, self.angle_fac*self.move_speed] if face_right else [-self.move_speed, self.angle_fac*self.move_speed]
        self.col_count = 0
    
    def progressing(self):
        if self.collide != [False]*4:
            self.col_count += 1


        if self.collide[0]:
            self.vel[1] *= -1 #= -abs(self.vel[1])
        elif self.collide[2]:
            self.vel[1] *= -1 #= abs(self.vel[1])
        elif self.collide[1]:
            self.vel[0] = abs(self.vel[0])
        elif self.collide[3]:
            self.vel[0] = -abs(self.vel[0])

        #Now, start to move. Note that the coordinate is reverted.

        self.pos[1] += self.vel[1]
        self.pos[0] += self.vel[0]

    
    def lights_up(self, block, block_size):
        light_rect = (block[0], block[1], 0.2*block_size, 0.2*block_size)
        pygame.draw.rect(screen, YELLOW, light_rect)



def initialization(width, height, size, monster_size, monster_num = 1):
    player = Player([width//2, height//2], size)
    monsters = []
    dead_monsters = []

    for _ in range(monster_num):
        monsters.append(Monster([3*width//4, height//2], monster_size))
    
    return player, monsters, dead_monsters
    

# 2.1 - Some parameters

player_size = [30,50]
monster_size = [30,30]
block_size = [20,20]
fireball_size = [10,10]
monster_num = 1


pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)

keys = [False, False, False, False]






#Side wall and lower wall

blocks = [GameObject([x_pos * block_size[0], height-block_size[1]], block_size) for x_pos in range(width//block_size[0])]
blocks.extend([GameObject([0, y_pos *block_size[1]], block_size)  for y_pos in range(height//block_size[1])])
blocks.extend([GameObject([width-block_size[0], y_pos *block_size[1]], block_size)  for y_pos in range(height//block_size[1])])


#Some walls in the middle

blocks.extend([GameObject([x_pos * block_size[0], height-5*block_size[1]], block_size) for x_pos in range(10,width//block_size[0] - 10)])

acc=[0,0]
arrows=[]


badtimer=100
badtimer1=0
badguys=[[640,100]]
healthvalue=194

pygame.mixer.init()


# 3 - Load images

wall = pygame.image.load("resources/images/wall.jpg")
wall = pygame.transform.scale(wall, block_size)

mario = pygame.image.load("resources/images/mario_stand.png").convert_alpha()
mario = pygame.transform.scale(mario, player_size)

mario_jump = pygame.image.load("resources/images/Mario_jump.jpg")
mario_jump = pygame.transform.scale(mario_jump, player_size)


goomba = pygame.image.load("resources/images/goomba.png")
goomba = pygame.transform.scale(goomba, monster_size)


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


# 4 Big loop so that after the gameover one can restart.
while True:
    player, monsters, dead_monsters = initialization(width, height, player_size, monster_size)
    fireballs = []
    exit_flag = False

    while not exit_flag:
        # 5 - clear the screen before drawing it again
        screen.fill(0)

        #player_rect = (player.pos[0], player.pos[1], player.size[0], player.size[1])
        #small_rect = (player.pos[0], player.pos[1], 0.1*player.size[0], 0.1*player.size[1])
        #pygame.draw.rect(screen, BLUE, player_rect)
        #pygame.draw.rect(screen, GREEN, small_rect)

        # 5.1 - Blit players, wall, and monster

        player.check_collide(blocks)
        player.progressing()

        if player.vert != 0 and player.face_right:
            screen.blit(mario_jump, player.pos)
        elif player.vert != 0:
            screen.blit(pygame.transform.flip(mario_jump, True, False), player.pos)
        elif player.face_right:
            screen.blit(mario, player.pos)
        else:
            screen.blit(pygame.transform.flip(mario, True, False), player.pos)


        for block in blocks:
            screen.blit(wall, block.pos)
            #rect = (block[0], block[1], block_size, block_size)
            #small_rect = (block[0], block[1], 0.1*block_size, 0.1*block_size)
            #pygame.draw.rect(screen, RED, rect)
            #pygame.draw.rect(screen, GREEN, small_rect)

        # 5.1.2 - Check if monsters disappeared.
        while len(monsters) < monster_num:
            monsters.append(Monster([3*width//4, height//2], monster_size))


        for monster in monsters:

            monster.check_collide(blocks)
            monster.progressing()

            screen.blit(goomba, monster.pos)

        remaining_ind = []

        for i,dead_monster in enumerate(dead_monsters):
            dead_monster.progressing()

            if dead_monster.pos[1] > 2 * height:
                del dead_monster
            else:
                remaining_ind.append(i)
                screen.blit(goomba, dead_monster.pos)


        dead_monsters = [dead_monsters[i] for i in remaining_ind]


        for fireball in fireballs:

            fireball.check_collide(blocks)
            fireball.progressing()

            rect = (fireball.pos[0], fireball.pos[1], fireball.size[0], fireball.size[1])
            pygame.draw.rect(screen, RED, rect)
        

        
        pygame.display.flip()

        # 8 - loop through the events
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)


            #For pressing down the key for WASD, we perform some actions.
            if event.type == pygame.KEYDOWN:
                if event.key==K_w:
                    player.keys[0]=True
                elif event.key==K_a:
                    player.keys[1]=True
                    player.face_right = False
                elif event.key==K_s:
                    player.keys[2]=True
                elif event.key==K_d:
                    player.keys[3]=True
                    player.face_right = True

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
                elif event.key == pygame.K_SPACE and len(fireballs) < 4:
                    shoot.play()
                    if player.face_right:
                        fireballs.append(Projectiles([player.pos[0]+player.size[0], player.pos[1] + 0.5*player.size[1]], fireball_size, face_right = True))
                    else:
                        fireballs.append(Projectiles([player.pos[0], player.pos[1] + 0.5*player.size[1]], fireball_size, face_right = False))

        # 5.2.1 - If the player touches the monster, then game over. 


        if player.got_hit_any(monsters):
            #Clear all collision, let him jump one last time.
            player.collide = [False]*4
            player.keys = [False]*4
            player.vert = player.jump_speed_factor * player.gravity
            exit_flag = True
            hit.play()
            break

        # 5.2.2 - If the monster touches the fireball, then the monster dies and the fireball disappears.
        alive_ind = []
        dead_ind = []

        for i, monster in enumerate(monsters):
            if monster.got_hit_any(fireballs):
                # Jump a bit then die.
                monster.vert = monster.jump_speed_factor * monster.gravity
                monster.collide = [False]*4
                monster.keys = [False]*4
                dead_ind.append(i)
            else:
                alive_ind.append(i)
        
        newly_dead = [monsters[i] for i in dead_ind]
        dead_monsters += newly_dead

        monsters = [monsters[j] for j in alive_ind]


        # 5.2.3 - If the collision is more than 3, then the fireballs disappears.
        fireballs = [fireball for fireball in fireballs if fireball.col_count <= 3 and fireball.pos[0] > 0 and fireball.pos[0] < width and fireball.pos[1] > 0 and fireball.pos[1] < height]


    while player.pos[1] < 2*height:
        screen.fill(0)
        #Let the player jump and fall through walls.

        player.progressing()
        screen.blit(mario_jump, player.pos)

        #The wall and monsters are static.
        for block in blocks:
            screen.blit(wall, block.pos)
        
        for monster in monsters:
            screen.blit(goomba, tuple(monster.pos))        

        
        pygame.display.flip()

    # Delete all monsters and players.

    del player
    for monster in monsters:
        del monster

    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("You Lost. Click anywhere to play again.", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)

    replay_flag = False

    while not replay_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type==pygame.MOUSEBUTTONDOWN:
                replay_flag = True
                break
        pygame.display.flip()














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

