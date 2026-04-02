import pygame
import sys

# CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "MAZEY"
MAX_FPS = 60        #--> 60 fps
TILE_SIZE = 50 

# IDENTIFIERS
STATE_TITLE = 0
STATE_PLAYING = 1 
STATE_WIN = 2
STATE_GAMEOVER = 3

# COLORS
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
GREEN = ( 60, 200, 60)
YELLOW = (255, 220, 0)
RED = (220, 60, 60)
DARK_GREEN = (0, 140, 0)

PLAYER_SPEED = 220
ENEMY_SPEED = 160

class Player(pygame.sprite.Sprite):
    # Starting positions
    START_X = 80
    START_Y = 80
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 8, TILE_SIZE - 8))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.reset()
    
    def reset(self):
        """ 
        Returns player to starting position
        """
        self.rect.topleft = (self.START_X, self.START_Y)
    
    def update(self, delta, walls):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -=int(PLAYER_SPEED * delta)
        if keys[pygame.K_RIGHT]:
            self.rect.x += int(PLAYER_SPEED * delta)
        
        for wall in pygame.sprite.spritecollide(self, walls, False):
            if keys[pygame.K_RIGHT]:
                self.rect.right = wall.rect.left
            if keys[pygame.K_LEFT]:
                self.rect.left = wall.rect.right
        
        if keys[pygame.K_UP]:
            self.rect.y -=(PLAYER_SPEED * delta)
        if keys[pygame.K_DOWN]:
            self.rect.y += int(PLAYER_SPEED * delta)
        
        for wall in pygame.sprite.spritecollide(self, walls, False):
            if keys[pygame.K_DOWN]:
                self.rect.bottom = wall.rect.top 
            if keys[pygame.K_UP]:
                self.rect.top = wall.rect.bottom
        
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class Enemy(pygame.sprite.Sprite):
    START_X = 680
    START_Y = 300
    
    def __init__(self):
        super().__init__()
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.reset()
    
    def reset(self):
        """
        Returns enemy to starting positions
        """
        self.rect.topleft = (self.START_X, self.START_Y)
        self._vel_x = - ENEMY_SPEED
    
    def update(self, delta, walls):
        """ 
        Bouncing of walls and screen edges
        """
        self.rect.x += int(self._vel_x * delta)
        
        # Bouncing screen edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self._vel_x *= -1
