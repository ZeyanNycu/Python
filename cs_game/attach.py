import pygame
font_name = pygame.font.match_font('arial')
def draw_score(text,size):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,(255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = 400
    text_rect.top = 20
    return text_surface,text_rect
def draw_text(scr,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,(255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    scr.blit(text_surface,text_rect)
    return scr
def draw_health(surf,shooter):
    if shooter.health<0:
        shooter.health = 0
    BAR_width = 200
    BAR_height = 40
    fill_length = (shooter.health/100)*BAR_width
    outline = pygame.Rect(20,18,BAR_width,BAR_height)
    fill = pygame.Rect(20,18,fill_length,BAR_height)
    pygame.draw.rect(surf,(0,255,0),fill)
    pygame.draw.rect(surf,(255,255,255),outline,2)
    return surf
def draw_lives(surf,img,lives):
    for i in range(lives):
        rect = img.get_rect()
        rect.x = 700+32*i
        rect.y = 18
        surf.blit(img,rect)
    return surf
