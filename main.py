import pygame

pygame.init()

# Time
CLOCK = pygame.time.Clock()
FPS = 60

# Surface
HORIZONTAL, VERTICAL = (288, 580)
screen = pygame.display.set_mode((HORIZONTAL, VERTICAL))
pygame.display.set_caption("flippy bard")

# Sprites
BACKGROUND = pygame.image.load("sprites/background-day.png")  # 288 x 512

BASE = pygame.image.load("sprites/base.png")  # 336 x 112
BASE_POSITION = 0
BASE_SPEED = 4

PIPE_GAP = 100

# Sound effects
flap_sound = pygame.mixer.Sound("sound/wing.wav")
hit_sound = pygame.mixer.Sound("sound/hit.wav")
point_sound = pygame.mixer.Sound("sound/point.wav")


class Bird:
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
        self.hitbox = (self.x, self.y, self.width, self.height + 7)
        self.gravity = 0
        self.gameover = False
        self.passPipe = False

    def draw_motion(self, surface):
        self.hitbox = (self.x, self.y, self.width, self.height + 7)
        # pygame.draw.rect(surface, "red", self.hitbox, 1)

        if not self.gameover:
            if self.flyCount + 1 >= 30:
                self.flyCount = 0

            surface.blit(
                pygame.transform.rotate(
                    self.img[self.flyCount // 10], self.gravity * -2.5
                ),
                (self.x, self.y),
            )
            self.flyCount += 1

            if not self.waiting:
                if self.hitbox[1] + self.hitbox[3] <= 512:
                    self.y += int(self.gravity)
                    if self.gravity < 11:
                        self.gravity += 0.25
                    else:
                        self.gravity = 11

    def hit(self):
        # Reset bird
        self.x = HORIZONTAL // 2 - 34 // 2 - 20
        self.y = VERTICAL // 2 - 24 // 2
        self.flyCount = 0
        self.waiting = True
        self.waiting_swingCount = 0
        self.flap = False
        self.gravity = 0

        # Pause game for notification
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()
                    
        self.gameover = False
        

class Pipe:
    img = pygame.image.load("sprites/pipe-green.png")  # 52 x 320
    
    def __init__(self, x, y, width, height, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction  # -1 down 1 up
        
    def draw_motion(self, surface):
        if self.direction == 1:
            surface.blit(self.img, (self.x, self.y))
            # self.x -= BASE_SPEED
        else:
            surface.blit(pygame.transform.flip(self.img, False, True), (self.x, self.y))
            # self.x -= BASE_SPEED
            
    def hit(self):
        pass


def drawing():
    global BASE_POSITION
    screen.blit(BACKGROUND, (0, 0))
    if not bird.waiting:
        for pipe in pipes:
            pipe.draw_motion(screen)
            pipe.x -= BASE_SPEED
    screen.blit(BASE, (BASE_POSITION, 512))
    BASE_POSITION -= BASE_SPEED
    if BASE_POSITION < -48:
        BASE_POSITION = 0
    bird.draw_motion(screen)
    pygame.display.update()


bird = Bird(HORIZONTAL // 2 - 34 // 2 - 20, VERTICAL // 2 - 24 // 2, 34, 24)
# pipe2 = Pipe(200, -120, 52, 320, -1)
# pipe1 = Pipe(200, -120 + 320 + PIPE_GAP, 52, 320, 1)

pipes = []


running = True

while running:
    CLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if len(pipes) == 0:
        pipes.append(Pipe(336, -120 + 320 + PIPE_GAP, 52, 320, 1))
        pipes.append(Pipe(336, -120, 52, 320, -1))
        bird.passPipe = False
        
    for pipe in pipes:
        if pipe.x + pipe.width <= 0:
            pipes.pop(pipes.index(pipe))
    

    if not bird.gameover:
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
            bird.gravity = -5
            flap_sound.play()
        elif not pygame.mouse.get_pressed()[0]:
            bird.flap = False

        # Point
        if pipes:
            if not bird.passPipe:
                if bird.x + bird.width > pipes[0].x + pipes[0].width:
                    point_sound.play()
                    bird.passPipe = True
                    
        # Losing/Collision
        if bird.hitbox[1] + bird.hitbox[3] >= 512:
            hit_sound.play()
            bird.gameover = True
            bird.hit()

    drawing()

pygame.quit()
