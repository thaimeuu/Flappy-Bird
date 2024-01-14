import pygame


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
        self.index = 0  # for choosing img purpose
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.gravity = 0
        self.alive = True
        self.flying = False  # bird's state
        
    def update(self, surface):
        # Continuous flapping motion when alive
        if self.alive:
            if self.index + 1 >= 30:
                self.index = 0
                
            # Rotate bird
            rotated_img = pygame.transform.rotate(self.img[self.index // 10], self.gravity * -2)
                
            surface.blit(rotated_img, (self.x, self.y))
            self.index += 1
        
            # Update hitbox for visualization
            self.hitbox = (self.x, self.y, self.width, self.height)
            pygame.draw.rect(surface, 'red', self.hitbox, 1)
        
        # Bird's gravity when flying == True
        if self.flying:
            if self.hitbox[1] + self.hitbox[3] < 512:
                self.gravity += 0.25
                self.y += int(self.gravity)

            else: 
                self.alive = False
                die_img = pygame.transform.rotate(self.img[1], -90)
                surface.blit(die_img, (self.x, self.y))
                self.flying = False
                
        
        