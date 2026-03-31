import pygame
import sys 

# CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "MAZEY"
TITLE_SIZE = 60

#COLORS
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    """_
    Represents the player character and it inherits from pygame.sprite.Sprite to work with Pygame's group system.
    """
    def __init__(self, x, y):
        super().__init__()      #--> Initialize the Sprite base class
        
        self.image = pygame.Surface(())     #--> defines what the sprite looks like
        self.image.fill()       # -->
        
        pygame.draw.rect(self.image, (), self.image.get_rect(), 3)      #--> Drawing a dark border on the wall to make the tiles visually distinct
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self._move_x  = 2       #--> Internal movement variable
        
    def update(self):
        """
        Player bounces from left to right automatically
        """
        
        
        
        
    


pygame.init() # --> Initializing Pygame

# CONSTANTS
GAME_TITLE = "Welcome to my World"