import pygame
import random

from bird import Bird
from pipe import Pipe

pygame.init()

# Set up

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


# Main loop
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.update()
    
pygame.quit()
