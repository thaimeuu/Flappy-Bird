import pygame

pygame.init()

# Time
CLOCK = pygame.time.Clock()
FPS = 60

# Surface
HORIZONTAL, VERTICAL = (288, 580)
screen = pygame.display.set_mode((HORIZONTAL, VERTICAL))
pygame.display.set_caption("flappy bird")

# Sprites
BACKGROUND = pygame.image.load("sprites/background-day.png")  # 288 x 512

BASE = pygame.image.load("sprites/base.png")  # 336 x 112
BASE_POSITION = 0
BASE_SPEED = 4

# Sound effects
flap_sound = pygame.mixer.Sound("sound/wing.wav")
hit_sound = pygame.mixer.Sound("sound/hit.wav")


class Bird:
    # Physics
    gravity = 0

    img = [
        pygame.image.load("sprites/yellowbird-downflap.png"),  # 34 x 24
        pygame.image.load("sprites/yellowbird-midflap.png"),
        pygame.image.load("sprites/yellowbird-upflap.png"),
    ]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.flyCount = 0
        self.waiting = True
        self.waiting_swingCount = 0
        self.flap = False
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw_motion(self, surface):
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, "red", self.hitbox, 1)

        if self.flyCount + 1 >= 30:
            self.flyCount = 0

        surface.blit(self.img[self.flyCount // 10], (self.x, self.y))
        self.flyCount += 1

        if not self.waiting:
            if bird.y + bird.height <= 512:
                bird.y += int(self.gravity)
                if self.gravity < 15.5:
                    self.gravity += 0.5
                else:
                    self.gravity = 15.5

            else:
                i = 0
                while i < 200:
                    pygame.time.delay(10)
                    i += 1
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            i = 201
                            pygame.quit()
                self.x = HORIZONTAL // 2 - 34 // 2
                self.y = VERTICAL // 2 - 24 // 2
                self.flyCount = 0
                self.waiting = True
                self.waiting_swingCount = 0
                self.flap = False


def drawing():
    global BASE_POSITION
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BASE, (BASE_POSITION, 512))
    BASE_POSITION -= BASE_SPEED
    if BASE_POSITION < -48:
        BASE_POSITION = 0
    bird.draw_motion(screen)
    pygame.display.update()


bird = Bird(HORIZONTAL // 2 - 34 // 2, VERTICAL // 2 - 24 // 2, 34, 24)

running = True

while running:
    CLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Bird swinging up and down waiting for player to left-click
    if bird.waiting:
        if bird.waiting_swingCount < 25:
            bird.y -= 0.3
            bird.waiting_swingCount += 1
        elif 25 <= bird.waiting_swingCount < 50:
            bird.y += 0.3
            bird.waiting_swingCount += 1
        else:
            bird.waiting_swingCount = 0

    # Flap motion
    if pygame.mouse.get_pressed()[0] and not bird.flap:
        bird.flap = True
        bird.waiting = False
        bird.gravity = -6
        flap_sound.play()
    elif not pygame.mouse.get_pressed()[0]:
        bird.flap = False

    # Losing/Collision
    if bird.y + bird.height > 512:
        hit_sound.play()

    drawing()

pygame.quit()
