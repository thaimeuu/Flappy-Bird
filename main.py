import pygame
from random import randint

from bird import Bird
from pipe import Pipe
from sound import die, hit, point, swoosh, wing


# Set up
pygame.init()

# Surface
HORIZONTAL, VERTICAL = 288, 580
screen = pygame.display.set_mode((HORIZONTAL, VERTICAL))
pygame.display.set_caption("flippy bard")

# Time/Clock
clock = pygame.time.Clock()
FPS = 60

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
RESTART = pygame.image.load("sprites/restart.png")  # 120 x 42
RESTART = pygame.transform.scale(RESTART, (80, 28))  # 80 x 28
RESTART_rect = RESTART.get_rect()
BACKGROUND = pygame.image.load("sprites/background-day.png")
BASE = pygame.image.load("sprites/base.png")
BASE_POS = 0
SCROLL_SPEED = 4
bird = Bird(HORIZONTAL//2 - 80, VERTICAL//2 - 12, 34, 24)

bot_pipe = Pipe(500, 350, -1)
top_pipe = Pipe(500, 350, 1)

# Restart function
def restart():
    global click, is_inside, one, ten, bot_pipe, top_pipe
    
    # reset global variables
    click = False  # user's click
    is_inside = False
    one = 0
    ten = 0
    
    # reset sprites
    bird.alive = True
    bird.flying = False
    bird.gravity = 0
    bird.x, bird.y = HORIZONTAL//2 - 80, VERTICAL//2 - 12
    
    del bot_pipe
    del top_pipe
    
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
        elif event.type == pygame.MOUSEBUTTONDOWN and bird.flying == False and bird.alive == True:
            bird.flying = True
        # Check if restart is pressed
        elif event.type == pygame.MOUSEBUTTONDOWN and RESTART_rect.collidepoint(event.pos) and not bird.flying and not bird.alive:
            swoosh.play()
            restart()
     
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
        # bird.gravity helps avoid wing sound when clicking restart
        if pygame.mouse.get_pressed()[0] and bird.gravity and click == False:
            wing.play()
            click = True
            bird.gravity = -5
        elif not pygame.mouse.get_pressed()[0]:
            click = False
            
        # Bird collides when hits base using hit boxes
        if bird.hitbox[1] + bird.hitbox[3] >= 512 and bird.flying and bird.alive: 
            hit.play()
            die.play()

            bird.gravity = 0
            bird.alive = False
            bird.flying = False
            
        # Bird collides when hits pipes using hit boxes
        if (bot_pipe.hitbox[0] <= bird.hitbox[0] + bird.hitbox[2] <= bot_pipe.hitbox[0] + bot_pipe.hitbox[2] or
            bot_pipe.hitbox[0] <= bird.hitbox[0] <= bot_pipe.hitbox[0] + bot_pipe.hitbox[2]):
            
            if (bird.hitbox[1] <= bot_pipe.hitbox[1] - bot_pipe.pipe_gap or
                bird.hitbox[1] + bird.hitbox[3] >= bot_pipe.hitbox[1]):
                
                hit.play()
                die.play()

                bird.gravity = 0
                bird.alive = False
                bird.flying = False 
    
        # Point update
        if bot_pipe.hitbox[0] + bot_pipe.hitbox[2] >= bird.hitbox[0] + bird.hitbox[2] >= bot_pipe.hitbox[0] and is_inside == False:
            is_inside = True
        
        if bird.hitbox[0] + bird.hitbox[2] > bot_pipe.hitbox[0] + bot_pipe.hitbox[2] and is_inside == True:
            point.play()
            one += 1
            is_inside = False
            if one > 9:
                ten += 1
                one = 0
            if ten > 9:
                ten = 0
    
    # DISPLAY 
    screen.blit(BACKGROUND, (0, 0))
    
    # Message
    if not bird.flying and bird.alive:
        screen.blit(MESSAGE, (HORIZONTAL//2 - MESSAGE.get_size()[0]//2, 110))
    
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
        screen.blit(COUNTER[one], (HORIZONTAL//2-COUNTER[one].get_size()[0]//2, 15))
    elif ten:
        screen.blit(COUNTER[ten], (HORIZONTAL//2-COUNTER[ten].get_size()[0], 15))
        screen.blit(COUNTER[one], (HORIZONTAL//2, 15))
    
    # Game over
    if not bird.alive and not bird.flying:
        screen.blit(GAMEOVER, (HORIZONTAL//2 - GAMEOVER.get_size()[0]//2, VERTICAL//2 - GAMEOVER.get_size()[1]//2 - 60))
        screen.blit(RESTART, (HORIZONTAL//2 - RESTART.get_size()[0]//2, VERTICAL//2 - RESTART.get_size()[1]//2))
        RESTART_rect.center = (HORIZONTAL//2, VERTICAL//2)
        
        
    pygame.display.update()
        
    
pygame.quit()
