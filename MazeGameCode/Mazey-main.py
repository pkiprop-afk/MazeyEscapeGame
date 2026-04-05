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
        