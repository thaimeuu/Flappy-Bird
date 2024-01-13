import pygame

pygame.init()

# Time
CLOCK = pygame.time.Clock()
FPS = 60

# Surface
HORIZONTAL, VERTICAL = (288, 580)
screen = pygame.display.set_mode((HORIZONTAL, VERTICAL))
pygame.display.set_caption("FLAPPY BIRD by thaimeuu")

# Sprites
BACKGROUND = pygame.image.load("sprites/background-day.png")  # 288 x 512

BASE = pygame.image.load("sprites/base.png")  # 336 x 112
BASE_POSITION = 0
BASE_SPEED = 4


def drawing():
    global BASE_POSITION
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BASE, (BASE_POSITION, 512))
    BASE_POSITION -= BASE_SPEED
    if BASE_POSITION < -48:
        BASE_POSITION = 0
    pygame.display.update()


def main():
    running = True

    while running:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        drawing()

    pygame.quit()


if __name__ == "__main__":
    main()
