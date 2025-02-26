########################################################################################################################
#                                           ------ Don't Touch the Balls ------                                        #
#                                                                                                                      #
#                                        Author:   Rev:1                                                               #
#                                                                                                                      #
#   Description: This program is based off the arcade game, "World's Hardest Game." To win, you have to get to the     #
# other green zone without hitting any of them moving enemies. Use arrow keys to move. When you hit an enemy, your     #
# death counter goes up by  one and your character is returned to it's original position. When you reach the other     #
# green zone, your finish counter goes up by one and you are returned to the original position to play again.          #                                              
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
########################################################################################################################

import pygame

pygame.init()

XBG = 550
YBG = 350
XPSIZE=40
YPSIZE=40
VEL=5
BG_IMAGE = 'img\\sand.jpg'
PLAYER_IMAGE = 'img\\snom.png'
ENEMY_IMAGE = 'img\\kuro.png'
GREEN_IMAGE = 'img\\green.jpg'
PROJ_IMAGE = 'img\\kitty.png'
BG = pygame.image.load(BG_IMAGE)
BG = pygame.transform.scale(BG, (XBG, YBG))
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Don't Touch The Balls.")

isRunning = True

class Projectile():
    def __init__(self, posx, posy, image):
        self.posx = posx
        self.posy = posy
        self.image = image
        self.image = pygame.image.load(PROJ_IMAGE)
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, (self.posx, self.posy))

    def move(self, vel):
        self.posx += vel

    def off_screen(self, posx): ##tech w tim
        return not(self.posx <= 800 and self.posx >= 0) ##tech w tim

    def collision(self, obj): ##tech w tim
        return collide(self, obj) ##tech w tim

class Character():
    def __init__(self, posx, posy, hitboxx, hitboxy, deaths= 0, finisher=0, right=True):
        self.posx = posx
        self.posy = posy
        self.hitboxx = hitboxx
        self.hitboxy = hitboxy
        self.deaths = deaths
        self.finisher = finisher
        self.proj = []

    def draw(self, screen):
        screen.blit(self.image, (self.posx, self.posy))  
        for proj in self.proj:
            proj.draw(screen) 
    

class Player(Character):
    def __init__(self, posx, posy, hitboxx, hitboxy, deaths=0, finisher=0):
        super().__init__(posx, posy, hitboxx, hitboxy)
        self.image = PLAYER_IMAGE
        self.image = pygame.image.load(PLAYER_IMAGE)
        self.image = pygame.transform.scale(self.image, (XPSIZE, YPSIZE))
        self.mask = pygame.mask.from_surface(self.image)
        self.proj_image = PROJ_IMAGE
        self.proj_image = pygame.image.load(PROJ_IMAGE)
        self.proj_image = pygame.transform.scale(self.image, (10, 10))
        self.deaths = deaths
        self.finisher = finisher
    
    
    def proj_movement(self, obj):
        for proj in self.proj:
            proj.move(VEL)
            if proj.off_screen(800):
                self.proj.remove(proj)
            elif proj.collision(obj):
                self.proj.remove(proj)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            if self.posx > 150 + self.hitboxx: ##benxlabs
                self.posx -= VEL ##benxlabs

        if keys[pygame.K_RIGHT]:
            if self.posx < 600: ##benxlabs
                self.posx += VEL ##benxlabs

        if keys[pygame.K_DOWN]: 
            if self.posy < 420: ##benxlabs
                self.posy += VEL ##benxlabs

        if keys[pygame.K_UP]: 
            if self.posy > 200 + self.hitboxy: ##benxlabs
                self.posy -= VEL ##benxlabs
        
        if keys[pygame.K_SPACE]:
            player.fire()

    def fire(self):
        proj = Projectile(self.posx, self.posy, self.proj_image)
        self.proj.append(proj)


    def draw(self, screen):
        super().draw(screen)
        

    def reset(self):
        self.posx = 169
        self.posy = 420


class Enemy(Character):
    def __init__(self, posx, posy, hitboxx, hitboxy, right=True):
        super().__init__(posx, posy, hitboxx, hitboxy)
        self.image = ENEMY_IMAGE
        self.image = pygame.image.load(ENEMY_IMAGE)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.right = right ##benxlabs
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        super().draw(screen)

    def move(self, bound_x1, bound_x2):  ##benxlabs
        if self.posx < bound_x1 or self.posx > bound_x2: ##benxlabs
            self.right = not self.right ##benxlabs
        if self.right: ##benxlabs
            self.posx += VEL ##benxlabs
        else: ##benxlabs
            self.posx -= VEL ##benxlabs


class Green:
    def __init__(self, posx, posy, hitboxx, hitboxy, image):
        self.posx = posx
        self.posy = posy
        self.hitboxx = hitboxx
        self.hitboxy = hitboxy
        self.image = pygame.image.load(GREEN_IMAGE)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, (self.posx, self.posy))


def collide(obj1, obj2):  # tech with tim
    offset_x = obj2.posx - obj1.posx  # tech with tim
    offset_y = obj2.posy - obj1.posy  # tech with tim
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  # tech with tim


player = Player(169, 420, 10, 10)

enemy = Enemy(250, 200, 5, 5, 15)
enemy2 = Enemy(250, 250, 5, 5, 15)
enemy3 = Enemy(500, 300, 5, 5, 15)
enemy4 = Enemy(500, 350, 5, 5, 15)
enemy5 = Enemy(250, 400, 5, 5, 15)
enemy6 = Enemy(250, 450, 5, 5, 15)
enemylist=[enemy,enemy2,enemy3,enemy4,enemy5,enemy6]

bgStart = Green(133, 389, 100, 100, 10)
bgFinish = Green(540, 160, 100, 100, 10)


font = pygame.font.Font('freesansbold.ttf', 25) 


def update():
    keys = pygame.key.get_pressed() 
    player.move(keys)
    for enemy in enemylist:
        enemy.move(250,500)
    for enemy in enemylist:
        if collide(player, enemy):
            player.deaths += 1
            player.reset()
        if collide(player, enemy):
            enemylist.remove(enemy)
    if collide(player, bgFinish):
        player.finisher += 1
        enemy.draw(screen)
        player.reset()
    player.proj_movement(enemy)


def draw():
    screen.fill((0, 96, 255))
    screen.blit(BG, (100, 150))
    bgStart.draw(screen)
    bgFinish.draw(screen)
    player.draw(screen)
    for enemy in enemylist:
        enemy.draw(screen)
    deathCounter = font.render( ##benxlabs
        "Deaths: " + str(player.deaths), True, (255, 255, 255)) ##benxlabs
    screen.blit(deathCounter, (250, 50)) ##benxlabs
    finisherCounter = font.render(
        "Finishes: " + str(player.finisher), True, (255, 255, 255))
    screen.blit(finisherCounter, (450, 50))

    pygame.display.update()


while isRunning:
    pygame.time.delay(50) ##benxlabs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    update()

    draw()


pygame.quit()
