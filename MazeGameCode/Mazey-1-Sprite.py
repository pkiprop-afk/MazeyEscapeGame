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
    Represents the player character and it inherits from pygame.sprite.Sprite to work with Pygame's group system
    """
    


pygame.init() # --> Initializing Pygame

# CONSTANTS
GAME_TITLE = "Welcome to my World"