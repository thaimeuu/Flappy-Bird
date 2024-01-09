import pygame
import pygame.image as img

pygame.init()

# Surface
horizontal, vertical = (288, 580)
screen = pygame.display.set_mode((horizontal, vertical))
pygame.display.set_caption("Flappy Bird")

# Frame rate
clock = pygame.time.Clock()
FPS = 60

# Sprites
background = [
    img.load("sprites/background-day.png"),  # 288 x 512
    img.load("sprites/background-night.png"),
]
base = img.load("sprites/base.png")  # 336 x 112
base_pos = 0
base_speed = 2


class Bird:
    appearance = [
        img.load("sprites/yellowbird-downflap.png"),
        img.load("sprites/yellowbird-midflap.png"),
        img.load("sprites/yellowbird-upflap.png"),
    ]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.flap = False
        self.velocity = 7
        self.down = False
        self.mid = True
        self.up = False
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw_motion(self, surface):
        if self.down:
            surface.blit(self.appearance[0], (self.x, self.y))
        elif self.mid:
            surface.blit(self.appearance[1], (self.x, self.y))
        elif self.up:
            surface.blit(self.appearance[2], (self.x, self.y))

        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, "red", self.hitbox, 1)
        
    def collide(self):
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()
            


def drawing():
    global base_pos
    screen.blit(background[0], (0, 0))
    screen.blit(base, (base_pos, 512))
    base_pos -= base_speed
    if base_pos <= -48:  # 336 - 288 = 48
        base_pos = 0
        
    bird.draw_motion(screen)
    pygame.display.update()


bird = Bird(horizontal // 2 - 17, vertical // 2 - 12, 34, 24)
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pressed()

    if not bird.flap and bird.y == vertical // 2 - 12:
        if mouse[0]:
            bird.flap = True
    else:
        if bird.velocity >= -7:
            bird.y -= round(bird.velocity * abs(bird.velocity) * 0.5)
            bird.velocity -= 1

            if bird.velocity > 0:
                bird.down = False
                bird.mid = False
                bird.up = True
            elif bird.velocity == 0:
                bird.down = False
                bird.mid = True
                bird.up = False
            else:
                bird.down = True
                bird.mid = False
                bird.up = False
        
        else:
            bird.flap = False
            bird.velocity = 7

    drawing()

pygame.quit()
