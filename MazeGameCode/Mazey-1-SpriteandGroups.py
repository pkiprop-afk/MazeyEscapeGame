import pygame
import sys 

# CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "MAZEY"
TILE_SIZE = 60

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
        self.rect.x += self._move_x
        
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self._move_x *= -1

class Wall(pygame.sprite.Sprite):
    """ 
    Represents a single wall tile in the maze
    """
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.Surface(())     #--> defines what the sprite will look like
        self.image.fill()
        
        self.rect = self.image.get_rect()   
        self.rect.topleft = (x, y)
        

pygame.init() # --> Initializing Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
font = pygame.font.Sysfont("Arial", 20)

# Creating Sprite instances
player = Player(x=100, y=100)

wall1 = Wall(x=200, y=260)
wall2 = Wall(x=400, y=200)
wall3 = Wall(x=600, y=300)

# Creating Groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player, wall1, wall2, wall3)

# Game loop
running = True

while running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    all_sprites.update()
    
    screen.fill(BLACK)
    
    all_sprites.draw(screen)
    

# CONSTANTS
GAME_TITLE = "Welcome to my World"