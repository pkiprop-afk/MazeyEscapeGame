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
        
        # Bouncing of walls
        for wall in pygame.sprite.spritecollide(self, walls, False):
            self._vel_x *= -1
            
            # prevent sticking
            if self._vel_x > 0:
                self.rect.left = wall.rect.right
            else:
                self.rect.right = wall.rect.left
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GRAY)
        pygame.draw.rect(self.image, (70, 70, 70), self.image.get_rect(), 3)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(DARK_GREEN)
        pygame.draw.rect(self.image, GREEN, self.image.get_rect(), 4)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Game:
    def __int__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        # fonts
        self.font_title = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 22)
        
        
        self.state = STATE_TITLE
        
        def _build_level(self):
            self.player = Player()
            self.enemy = Enemy()
            self.goal = Goal(x=680, y=500)
            
            wall_grid = [
                (3,1), (4,1), (5,1), (6,1),
                (3,2),
                (3,3), (4,3), (5,3),
                (5,4), (5,5),
                (2,5), (3,5),
                (8,2), (8,3), (8,4),
                (7,4), (6,4),
                (10, 1), (10, 2), (10, 3), (10, 4),
            ]
            
            self.walls = pygame.sprite.Group()
            self.enemies = pygame.sprite.Group()
            self.all_sprites = pygame.sprite.Group()
            
            for (col, row) in wall_grid:
                w = Wall(col * TILE_SIZE, row * TILE_SIZE)
                self.walls.add(w)
                self.all_sprites.add(w)
            
        self._build_level()
        
        self.enemies.add(self.enemy)
        self.all_sprites.add(self.goal, self.enemy, self.player)
            