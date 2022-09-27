from pickle import HIGHEST_PROTOCOL
import pygame
import player
import attach
import os
import random

W = 800
H = 900
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()
pygame.display.set_caption("The first game")

def draw_init():
    waiting = True
    global screen
    screen = attach.draw_text(screen,'This game is Star game',25,400,200)
    screen = attach.draw_text(screen,'use <= => to move and use space to shoot bullets',25,400,450)
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
                return True
            if event.type == pygame.KEYUP:
                waiting = False
                return False
        pygame.display.update()

running = True
FPS = 60 #控制偵數
score = 0
#載入圖片
background_img = pygame.image.load(os.path.join("img","background.jpg")).convert()
background_img = pygame.transform.scale(background_img,(W,H))
bullets_img = pygame.image.load(os.path.join("img","bullets.jpg")).convert()
tool = []
gun_img = pygame.image.load(os.path.join("img","gun.png")).convert()
health_img = pygame.image.load(os.path.join("img","health.png")).convert()
tool.append(gun_img)
tool.append(health_img)
rock_imgs = []
for i in range(5):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i+1}.jpg")).convert())
shooter_img = pygame.image.load(os.path.join("img","shooter.png")).convert()
shooter_img_mini = pygame.transform.scale(shooter_img,(40,50))
shooter_img_mini.set_colorkey((255,255,255))
#載入音檔
expl_sound = [ pygame.mixer.Sound(os.path.join("sound","expl1.wav")),pygame.mixer.Sound(os.path.join("sound","expl2.wav")) ]
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
dead_sound = pygame.mixer.Sound(os.path.join("sound","dead.wav"))
pygame.mixer.music.load(os.path.join("sound","background.wav")) 
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)
show_init = True

## when the game is running
while running :
    clock.tick(FPS)
    if show_init:
        close = draw_init()
        if close:
            break
        score = 0
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        players = pygame.sprite.Group()
        treasures = pygame.sprite.Group()
        shooter = player.SHOOTER(shooter_img,shoot_sound)
        all_sprites.add(shooter)
        players.add(shooter)
        for i in range(20):
            rock = player.ROCK(rock_imgs)
            all_sprites.add(rock)
            rocks.add(rock)
        show_init = False
    ##取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                all_sprites,bullets = shooter.shoot(all_sprites,bullets,bullets_img)
                shoot_sound.play()
    ##更新遊戲
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
    for r in hits:
        random.choice(expl_sound).play()
        if random.random()>0.3:
            treasure = player.TREASURE(tool,r.rect.center)
            all_sprites.add(treasure)
            treasures.add(treasure)
        rock = player.ROCK(rock_imgs)
        score += int(rock.radius)
        all_sprites.add(rock)
        rocks.add(rock)
    hits = pygame.sprite.groupcollide(players,rocks,False,True,pygame.sprite.collide_circle)
    for r in hits:
        shooter.health -= r.radius
        if shooter.health<=0:
            shooter.lives -= 1
            shooter.health = 100
            shooter.hide() 
        rock = player.ROCK(rock_imgs)
        score += int(rock.radius)
        all_sprites.add(rock)
        rocks.add(rock)
    if shooter.lives<=0:
        show_init = True
        dead_sound.play()
    hits = pygame.sprite.groupcollide(treasures,players,True,False,pygame.sprite.collide_circle)
    for r in hits:
        if r.type == 1:
            shooter.health += 10
            if shooter.health>=100:
                shooter.health = 100
        elif r.type == 0:
            shooter.gunup() 
    ##畫面顯示
    screen.blit(background_img,(0,0))
    surface,rect  = attach.draw_score(str(score),36)
    screen.blit(surface,rect)
    screen = attach.draw_health(screen,shooter)
    screen = attach.draw_lives(screen,shooter_img_mini,shooter.lives)
    all_sprites.draw(screen)
    pygame.display.update()
pygame.quit()