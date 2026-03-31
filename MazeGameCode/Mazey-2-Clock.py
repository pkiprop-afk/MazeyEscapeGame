import pygame 
import sys

# CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "MAZEY"
MAX_FPS = 60        #--> 60 fps

#COLORS
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
GREEN = ( 60, 200, 60)
YELLOW = (255, 220, 0)

pygame.init()       # --> Initializing pygame

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock() #--> pygame.time.Clock() - creates a clock object

font_large = pygame.font.SysFont("Arial", 22, bold=True)
font_small = pygame.font.SysFont("Arial", 18)

red_x = 0.0
green_x = 0.0

SQUARE_SIZE = 50
RED_SPEED_PIXELS = 3        #--> 3 pixels per frame
GREEN_SPEED_PPS = 200       #--> 200 pixels per second

running = True

while running:
    
    clock.tick(MAX_FPS)
    delta = clock.get_time() / 1000.0       # Convert milliseconds to seconds to get delta time.
    
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # moving both squares 
    red_x += RED_SPEED_PIXELS
    
    green_x +=GREEN_SPEED_PPS * delta