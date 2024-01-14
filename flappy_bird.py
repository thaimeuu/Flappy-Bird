import pygame
import random

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
COUNTER = [
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

# Main loop
running = True
while running:
    clock.tick(FPS)
    
    # LOGIC
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
           
    # DISPLAY 
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BASE, (BASE_POS, 512))
    
    # Scroll base
    BASE_POS -= SCROLL_SPEED
    if BASE_POS < -48:
        BASE_POS = 0
    
    pygame.display.update()
    
pygame.quit()
