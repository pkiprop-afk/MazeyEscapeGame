import pygame
import sys
import math
import random

# CONSTANTS
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
TITLE = "MAZEY - The Office Escape"
MAX_FPS = 60

# COLORS
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
GREEN = ( 60, 200, 60)
YELLOW = (255, 220, 0)
RED = (220, 60, 60)
DARK_GREEN = (0, 140, 0)
ORANGE = (255, 140, 0)

DARK_BACKGROUND = (15, 15, 25)
WALL_DARK = (40, 40, 55)
WALL_LIGHT = (70, 70, 90)
FLOOR_DARK= (25, 25, 35)
FLOOR_LIGHT = (35, 35, 50)
DARK_GREY = (50, 50, 65)
FREEZE_COL = (100, 200, 255)
GOAL_GLOW = (255, 255, 100)
PLAYER_COL = (80, 200, 120)
PLAYER_EYE = (220, 255, 220)
ENEMY_COL = (200, 60, 60)
ENEMY_EYE = (255, 200, 200)
GUARD_COL = (180, 80, 200)
GUARD_EYE = (240, 200, 255)

# IDENTIFIERS
STATE_TITLE = 0
STATE_PLAYING = 1 
STATE_WIN = 2
STATE_GAMEOVER = 3
STATE_LOADING = 4
STATE_DIFFICULT = 5

TILE_SIZE = 40

# Difficulty settings for game
DIFFICULTY = {
    "EASY": {"time":120, "patrol":2, "guards":1, "speed":200},
    "HARD": {"time": 75, "patrol":3, "guards":2, "speed":180},
    "VETERAN": {"time":45, "patrol":5, "guards":2, "speed":160},
}

# POWER UP TYPES
PU_SLOW_TIME = "SLOW TIME"
PU_SPEED_UP = "SPEED BOOST"
PU_WEAPON = "WEAPON"
PU_TELEPORT = "TELEPORT"
PU_FREEZE = "FREEZE GUN"
PU_AUTO_WIN = "AUTO WIN"
ALL_POWERUPS = [PU_SLOW_TIME, PU_SPEED_UP, PU_WEAPON, PU_TELEPORT, PU_FREEZE, PU_AUTO_WIN]

# POWER UP COLORS
PU_COLORS = {
    PU_SLOW_TIME: RED,
    PU_SPEED_UP: YELLOW,
    PU_WEAPON: GREEN,
    PU_TELEPORT: BLUE,
    PU_AUTO_WIN: WHITE,
}

# FLASHLIGHT Radius 
FLASH_RADIUS = 160
FLASH_RADIUS_MIN = 60


class Wall(pygame.sprite.Sprite):
    def __init__(self,x ,y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(WALL_DARK)
        pygame.draw.rect(self.image, WALL_LIGHT, (0, 0, TILE_SIZE, 2))
        pygame.draw.rect(self.image, WALL_LIGHT, (0, 0, 2, TILE_SIZE))
        pygame.draw.rect(self.image, (20, 20, 30), (0, TILE_SIZE - 2, TILE_SIZE, 2))
        pygame.draw.rect(self.image, (20, 20, 30), (TILE_SIZE-2, 0, 2, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self._anim_timer = 0
        self._draw(0)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Player(pygame.sprite.Sprite):
    # Starting positions
    START_X = 0
    START_Y = 0
    
    def __init__(self, x, y, speed ):
        super().__init__()
        self.base_speed = speed
        self.speed = speed
        self.image = pygame.Surface((TILE_SIZE - 6, TILE_SIZE - 6), pygame.SRCALPHA)
        self._draw_sprite()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        Player.START_X = x
        Player.START_Y = y
        
        #Flashlight
        self.flash_radius = FLASH_RADIUS
        self.flash_battery = 1.0
        
        # For power ups
        self.activate_powerup = None
        self.powerup_timer = 0.0
        self.weapon = None
        self.bullets = 0
        self.slow_time = False
        self.speed_boost = False
        
        # For facing the direction for shooting
        self.facing = pygame.math.Vector2(1,0)
        
        # Pixel art for player character
    def _draw_sprite(self):
        self.image.fill((0, 0, 0, 0))
        w = TILE_SIZE - 6
        pygame.draw.rect(self.image, PLAYER_COL, (w // 4, w // 3, w // 2, w // 2))
        pygame.draw.rect(self.image, PLAYER_COL, (w // 3, 2, w // 3, w // 4))
        pygame.draw.rect(self.image, PLAYER_EYE, (w // 3 + 2, 4, 3, 3))
        pygame.draw.rect(self.image, PLAYER_EYE, (w // 3 + w // 3 - 4, 4, 3, 3))
        pygame.draw.rect(self.image, PLAYER_COL, (w // 4, w // 3 + w // 2, w // 5, w // 5))
        pygame.draw.rect(self.image, PLAYER_COL, (w // 4 + w // 3, w // 3 + w // 2, w // 5, w // 5))
    
    def reset(self):
        self.rect.topleft = (self.START_X, self.START_Y)
        self.flash_battery = 1.0
        self.flash_radius = FLASH_RADIUS
        self.activate_powerup = None
        self.powerup_timer = 0.0
        self.weapon = None
        self.bullets = 0
        self.slow_time = False
        self.speed_boost = False
        self.speed = self.base_speed
        
    def update(self, delta, walls):
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
        
        # Power up timer
        if self.powerup_timer > 0:
            self.powerup_timer -= delta
            if self.powerup_timer <= 0:
                self._expire_powerup()
    
    # power up expire
    def _expire_powerup(self):
        if self.activate_powerup == PU_SLOW_TIME:
            self.slow_time = False
        if self.activate_powerup == PU_SPEED_UP:
            self.speed = self.base_speed
            self.speed_boost = False
        self.activate_powerup = None
    
    def apply_powerup(self, pu_type, enemies):
        # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
        if pu_type == PU_SLOW_TIME:
            self.slow_time = True
            self.activate_powerup = pu_type
            self.powerup_timer = 8.0
        
        elif pu_type == PU_SPEED_UP:
            self.speed = self.base_speed * 1.8
            self.speed_boost = True
            self.activate_powerup = pu_type
            self.powerup_timer = 6.0
        
        elif pu_type == PU_WEAPON:
            self.weapon = random.choice(PU_WEAPON)
            self.bullets = PU_WEAPON[self.weapon]
        
        elif pu_type == PU_TELEPORT:
            pass
        
        elif pu_type == PU_FREEZE:
            for enemy in enemies:
                enemy.freeze(5.0)
            self.activate_powerup = pu_type
            self.powerup_timer = 5.0
        
        elif pu_type == PU_AUTO_WIN:
            pass
    
class Bullet(pygame.sprite.Sprite):
    SPEED = 500
    
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (3, 3), 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = direction * self.SPEED
        self._fx = float(self.rect.x)
        self._fy = float(self.rect.y)
    
    def update(self, delta, walls):
        pass
    
    if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).colliderect(self.rect):
        self.kill()
        return
    
    if pygame.sprite.spritecollide(self, walls, False):
        self.kill()

class Powerup(pygame.sprite.Sprite):
    pass

class PatrolEnemy(pygame.sprite.Sprite):
    pass

class GuardEnemy (PatrolEnemy):
    pass

class Game:
    pass