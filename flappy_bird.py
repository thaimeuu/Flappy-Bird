import pygame
from random import randint

from bird import Bird
from pipe import Pipe


# Set up
pygame.init()

# Surface
HORIZONTAL, VERTICAL = 288, 580
screen = pygame.display.set_mode((HORIZONTAL, VERTICAL))
pygame.display.set_caption("flippy bard")

# Time/Clock
clock = pygame.time.Clock()
FPS = 60

# Font


# Sound effects


# Sprites
COUNTER = [  # 24 x 36
    pygame.image.load("sprites/0.png"),
    pygame.image.load("sprites/1.png"),
    pygame.image.load("sprites/2.png"),
    pygame.image.load("sprites/3.png"),
    pygame.image.load("sprites/4.png"),
    pygame.image.load("sprites/5.png"),
    pygame.image.load("sprites/6.png"),
    pygame.image.load("sprites/7.png"),
    pygame.image.load("sprites/8.png"),
    pygame.image.load("sprites/9.png"),
]
MESSAGE = pygame.image.load("sprites/message.png")
GAMEOVER = pygame.image.load("sprites/gameover.png")
BACKGROUND = pygame.image.load("sprites/background-day.png")
BASE = pygame.image.load("sprites/base.png")
BASE_POS = 0
SCROLL_SPEED = 4
bird = Bird(HORIZONTAL//2 - 80, VERTICAL//2 - 12, 34, 24)

bot_pipe = Pipe(500, 350, -1)
top_pipe = Pipe(500, 350, 1)

# Main loop
running = True
click = False  # user's click
is_inside = False
# point-related
one = 0
ten = 0

while running:
    clock.tick(FPS)
    
    # LOGIC
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and bird.flying == False and bird.alive == True:
            bird.flying = True
     
    # Generating pipes after pipes when bird's flying and alive
    if bird.flying and bird.alive:
        if bot_pipe.x + bot_pipe.width < 0:
            del bot_pipe
            del top_pipe
            pipe_height = randint(300, 400)
            bot_pipe = Pipe(HORIZONTAL, pipe_height, -1)
            top_pipe = Pipe(HORIZONTAL, pipe_height, 1)
     
    # Allow bird to flap when it's alive (game not over)
    if bird.alive:     
        if pygame.mouse.get_pressed()[0] and click == False:
            click = True
            bird.gravity = -5
        elif not pygame.mouse.get_pressed()[0]:
            click = False
            
        # Bird collides when hits pipes using hit boxes
        if (bot_pipe.hitbox[0] <= bird.hitbox[0] + bird.hitbox[2] <= bot_pipe.hitbox[0] + bot_pipe.hitbox[2] or
            bot_pipe.hitbox[0] <= bird.hitbox[0] <= bot_pipe.hitbox[0] + bot_pipe.hitbox[2]):
            
            if (bird.hitbox[1] <= bot_pipe.hitbox[1] - bot_pipe.pipe_gap or
                bird.hitbox[1] + bird.hitbox[3] >= bot_pipe.hitbox[1]):
                
                bird.gravity = 0
                bird.alive = False
                bird.flying = False 
    
        # Point update
        if bot_pipe.hitbox[0] + bot_pipe.hitbox[2] >= bird.hitbox[0] + bird.hitbox[2] >= bot_pipe.hitbox[0] and is_inside == False:
            is_inside = True
        
        if bird.hitbox[0] + bird.hitbox[2] > bot_pipe.hitbox[0] + bot_pipe.hitbox[2] and is_inside == True:
            point += 1
            is_inside = False
            if point > 9:
                ten += 1
                point = 0
    
    # DISPLAY 
    screen.blit(BACKGROUND, (0, 0))
    
    # Make sure update bird and pipes before displaying base so that bird isn't on top of base
    bird.update(screen) 
    if bird.flying and bird.alive: 
        bot_pipe.update(screen)
        top_pipe.update(screen)
    else:  # if bird's dead, pipes stay still
        bot_pipe.stay(screen)
        top_pipe.stay(screen)
          
    # Bird collides when hits pipes when game over
    if not bird.alive:
        bird.collide(screen)
        
        
    screen.blit(BASE, (BASE_POS, 512))  
    if bird.alive:
        BASE_POS -= SCROLL_SPEED  # Scroll base when bird is alive
        if BASE_POS < -48:
            BASE_POS = 0
    # Counter should be displayed at last
    if not ten:    
        screen.blit(COUNTER[point], (HORIZONTAL//2-COUNTER[point].get_size()[0]//2, 15))
    elif ten:
        screen.blit(COUNTER[ten], (HORIZONTAL//2-COUNTER[ten].get_size()[0], 15))
        screen.blit(COUNTER[point], (HORIZONTAL//2, 15))
    
    pygame.display.update()
    
pygame.quit()
