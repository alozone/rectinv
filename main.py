import pygame
import sys
import math
import random as r

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans', 30)
(width, height) = (600,400)
scr = pygame.display.set_mode((width,height))
lives = 5
score = 0

def lives_text(lifescore, font):
    msg = "Lives: {0}".format(lifescore)
    livesmsg = font.render(msg, 1, (255,255,255))
    scr.blit(livesmsg,(500,10))


def score_text(value, font):
    msg = "Score: {0}".format(value, font)
    scoremsg = font.render(msg, 1, (255,255,255))
    scr.blit(scoremsg,(500,30))
pygame.mouse.set_visible(False)
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.lives = 5
        self.image = pygame.Surface((50,50))
        self.image.fill((1,111,3))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speedy = 0
    #Change the position of rectangle to the mouse position
    def update(self):
        self.speedy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.speedy = -8
        if key[pygame.K_s]:
            self.speedy = 8
        self.rect.y += self.speedy
        #hitting a wall stop
        if self.rect.top < 0:
            if key[pygame.K_w]:
                self.speedy = 8
            self.rect.y +=self.speedy
        if self.rect.bottom > height:
            if key[pygame.K_s]:
                self.speedy = -8
            self.rect.y += self.speedy
            
    #returns the pos_x and pos_y for Bullet class to tell where it have to create
    def shot(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        all_sprites.add(bullet)
        bullets.add(bullet)


        if self.rect.bottom >= height:
            self.speedy = 0
    def lives(self):
        if hits:
            self.lives-=1
            print(self.lives)
        if self.lives==0:
            running = False

            
    #returns the pos_x and pos_y for Bullet class to tell where it have to create
    def shot(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,10))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        #if hit wall kill
        if self.rect.y > 600:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40,40))
        self.image.fill((1,3,111))
        self.rect = self.image.get_rect()
        self.rect.x = r.randrange(590,600)
        self.rect.y = r.randrange(height-30)
        self.speedx = r.randrange(-8,-1)
    def update(self):
        global lives
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.rect.x = r.randrange(590,600)
            self.rect.y = r.randrange(height-30)
            self.speedx = r.randrange(-8,-1)
            lives -= 1 

def live():
    global lives
    if lives==0:
        sys.exit()


player = Player(50, 200)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)


Clock = pygame.time.Clock()
fps = 30
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shot()
    #update section (take this to minimum later, into one group)
    all_sprites.update() 

    hits = pygame.sprite.spritecollide(player, enemies, False)
    hits2 = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits2:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        score+=1
        

    #draw section

    all_sprites.draw(scr)
    lives_text(lives,myfont)
    score_text(score,myfont)
    live()
    pygame.display.update()
    Clock.tick(fps)
    scr.fill((111,1,3))
