import pygame
import sys

# CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "MAZEY"
MAX_FPS = 60        #--> 60 fps
TILE_SIZE = 60 


#COLORS
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
GREEN = ( 60, 200, 60)
YELLOW = (255, 220, 0)
RED = (220, 60, 60)
DARK_GREEN = (0, 140, 0)

PLAYER_SPEED = 250  #-->pixels per second

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = PLAYER_SPEED 
    
    def update(self, delta, walls):
        """ 
        Moves players with arrow keys and wall collisions.
        Horizontal and Vertical movements
        """
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.rect.x -=int(self.speed * delta)
        if keys[pygame.K_RIGHT]:
            self.rect.x += int(self.speed * delta)
        
        hit_walls = pygame.sprite.spritecollide(self, walls, False)
        for wall in hit_walls:
            if keys[pygame.K_RIGHT]:
                self.rect.right = wall.rect.left
            
