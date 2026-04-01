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
                self.rect.right = wall.rect.left        #--> Moving right
            if keys[pygame.K_LEFT]:
                self.rect.left = wall.rect.right        #--> Moving left
        
        # Moving vertically
        if keys[pygame.K_UP]:
            self.rect.y -= int(self.speed * delta)
        if keys[pygame.K_DOWN]:
            self.rect.y += int(self.speed * delta)
        
        # Checking vertical collisions after vertical movement
        hit_walls = pygame.sprite.spritecollide(self, walls, False)
        for wall in hit_walls:
            if keys[pygame.K_DOWN]:
                self.rect.bottom = wall.rect.top
            if keys[pygame.K_UP]:
                self.rect.top = wall.rect.bottom
        
        # keeping player inside boundary
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.default_color = GRAY
        self.image.fill(self.default_color)
        pygame.draw.rect(self.image, (80, 80, 80), self.image.get_rect(), 3)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def set_highlighted(self, highlighted):
        """ 
        Changes color to red when the player is touching the wall
        """
        if highlighted:
            color = RED
        else:
            self.default_color
    
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(DARK_GREEN)
        pygame.draw.rect(self.image, GREEN, self.image.get_rect(), 4)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22, bold=True)
font_small = pygame.font.SysFont("Arial", 18)

player = Player(x=80, y=80)
goal = Goal(x=680, y=480)

wall_positions = [
    (2,1), (3,1), (4,1), (5,1),
    (2,2),
    (2,3), (3,3), (4,3),
    (4,4), (4,5)
    (1,5), (2,5), (3,5),
    (6,1), (6,2), (6,3),
    (7,3), (8,3),
    (8,4), (8,5), (8,6),
    (5,6), (6,6), (7,6),
]

walls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

for (col, row) in wall_positions:
    wall = Wall(col * TILE_SIZE, row *  TILE_SIZE)
    walls.add(wall)
    all_sprites.add(wall)

all_sprites.add(goal, player)

running = True
goal_reached = False 

while running:
    clock.tick(MAX_FPS)
    delta = clock.get_time()/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    player.update(delta, walls)
    
    for wall in walls:          # --> Reset all wall highlights each frame
        wall.set_highlighted(False)
    
    touching_walls = pygame.sprite.spritecollide(player, walls, False)
    for wall in touching_walls:
        wall.set_highlighted(True)
    
    if player.rect.colliderect(goal.rect):      #--> Check if player reached the goal
        goal_reached = True
    
    
    
    