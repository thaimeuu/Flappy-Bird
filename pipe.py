import pygame


class Pipe:
    bot_pipe = pygame.image.load("sprites/pipe-green.png")
    top_pipe = pygame.transform.flip(
        pygame.image.load("sprites/pipe-green.png"),
        False,
        True
    )
    pipe_gap = 110
    
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # 1: top, -1: bottom
        self.width, self.height = self.bot_pipe.get_size()
        self.hitbox = (self.x, self.y, self.width, self.height)
        
    def update(self, surface):
        # Draw bottom pipe and top pipe
        if self.direction == -1:
            surface.blit(self.bot_pipe, (self.x, self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)
            pygame.draw.rect(surface, 'red', self.hitbox, 1)
        else:
            surface.blit(self.top_pipe, (self.x, self.y - self.height - self.pipe_gap))
            self.hitbox = (self.x, self.y - self.height - self.pipe_gap, self.width, self.height)
            pygame.draw.rect(surface, 'red', self.hitbox, 1)
            
        # Scroll pipe with SCROLL_SPEED
        self.x -= 4
    
    def stay(self, surface):
        if self.direction == -1:
            surface.blit(self.bot_pipe, (self.x, self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)
            pygame.draw.rect(surface, 'red', self.hitbox, 1)
        else:
            surface.blit(self.top_pipe, (self.x, self.y - self.height - self.pipe_gap))
            self.hitbox = (self.x, self.y - self.height - self.pipe_gap, self.width, self.height)
            pygame.draw.rect(surface, 'red', self.hitbox, 1)
        
        