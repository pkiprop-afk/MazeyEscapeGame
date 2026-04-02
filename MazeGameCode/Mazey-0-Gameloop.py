import pygame
import sys

# CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "MAZEY"

# COLORS
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
GREEN = (130, 130, 130)

# IMAGES
pygame.init()       # --> Initializing pygame
img = pygame.image.load("MazeGameCode/Images/background.jpg") 
background_image = pygame.transform.scale(img, (900, 600))


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

# font
font = pygame.font.SysFont("Arial", 22)

running = True

while running:
    for event in pygame.event.get():  #--> Event handling
        if event.type == pygame.QUIT:
            running = False

    #screen.fill(BLACK)
    
    square_rect = pygame.Rect(350, 250, 100, 100)
    pygame.draw.rect(screen, GRAY, square_rect)
    
    label = font.render("Game is loading...", True, WHITE)
    screen.blit(background_image, (0, 0))
    screen.blit(label, (20,20)) # blit - draw a surface on another surface
    
    pygame.display.flip()

pygame.quit()   #--> teardown
sys.exit