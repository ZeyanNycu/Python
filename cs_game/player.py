import pygame
import random
class SHOOTER(pygame.sprite.Sprite):
    def __init__(self,img,sound):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img,(150,120)) # 圖片大小
        self.image.set_colorkey((255,255,255))
        self.radius = 80
        self.rect = self.image.get_rect()
        self.health = 100
        self.lives = 2
        self.sound = sound
        #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
        self.rect.centerx = 400
        self.rect.bottom = 780
        self.ishide = False
        self.hide_time = 0
        self.gun_lev = 1
        self.gun_time = 0
    def update(self):
        if self.gun_lev and pygame.time.get_ticks()-self.gun_time>1000:
            self.gun_lev = 1
            self.gun_time = 0
        if self.ishide and pygame.time.get_ticks()-self.hide_time>1000:
            self.ishide = False
            self.hide_time = 0
            self.rect.centerx = 400
            self.rect.bottom = 780
        else:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_LEFT]:
                self.rect.x -= 8
            if key_pressed[pygame.K_RIGHT]:
                self.rect.x += 8

            if self.rect.right>800:
                self.rect.right = 800
            if self.rect.left<0:
                self.rect.left = 0
    def shoot(self,all_sprites,bullets,img):
        if not(self.ishide):
            if self.gun_lev == 2:
                bullet = BULLET(self.rect.left,self.rect.y,img)
                bullets.add(bullet)
                all_sprites.add(bullet)
                bullet = BULLET(self.rect.right,self.rect.y,img)
                bullets.add(bullet)
                all_sprites.add(bullet)
            else:
                bullet = BULLET(self.rect.centerx,self.rect.y,img)
                bullets.add(bullet)
                all_sprites.add(bullet)
            #self.sound.play()
        return all_sprites,bullets
    def hide(self):
        self.ishide = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (400,1100)
    def gunup(self):
        self.gun_lev = 2
        self.gun_time = pygame.time.get_ticks()
class ROCK(pygame.sprite.Sprite):
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.width = random.randrange(80,120)
        self.img_ori = pygame.transform.scale(img[random.randrange(0,4)],(self.width,self.width+5))
        self.img_ori.set_colorkey((255,255,255))
        self.image = pygame.transform.scale(self.img_ori,(self.width,self.width+5)) # 圖片大小
        self.image.set_colorkey((255,255,255))
        self.radius = self.width*0.85/2
        self.rect = self.image.get_rect()
        #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
        self.rect.x = random.randrange(0,770)
        self.rect.y = random.randrange(-10,0)
        self.speedx = random.randrange(-5,5)
        self.speedy = random.randrange(5,10)
        self.total_deg = 0
        self.deg = random.randrange(-3,3)
    def rotate(self):
        self.total_deg += self.deg
        self.total_deg %= 360
        self.image = pygame.transform.rotate(self.img_ori,self.total_deg)
        self.image.set_colorkey((255,255,255))
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top>600 or self.rect.left>800 or self.rect.right<0:
            self.rect.x = random.randrange(0,770)
            self.rect.y = random.randrange(-10,0)
            self.speedx = random.randrange(-5,5)
            self.speedy = random.randrange(5,10)

class BULLET(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img,(10,20)) # 圖片大小
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom<0:
            self.kill()

class TREASURE(pygame.sprite.Sprite):
    def __init__(self,img,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.randrange(0,2)
        self.img_ori = pygame.transform.scale(img[self.type],(30,35))
        self.image = pygame.transform.scale(self.img_ori,(50,50)) # 圖片大小
        self.image.set_colorkey((255,255,255))
        self.radius = 30*0.85/2
        self.rect = self.image.get_rect()
        #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
        self.rect.center = center
        self.speedx = random.randrange(-5,5)
        self.speedy = random.randrange(5,10)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top>600 or self.rect.left>500 or self.rect.right<0:
            self.kill     

