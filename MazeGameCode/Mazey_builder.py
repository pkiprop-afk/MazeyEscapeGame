import random

import pygame

from Mazey_constants import ALL_POWERUPS, DIFFICULTY, TILE_SIZE, MAP_DATA
from Mazey_spritesandgroups import Goal, GuardEnemy, PatrolEnemy, Player, Powerup, Wall

def build_map(difficulty_key):
    settings = DIFFICULTY[difficulty_key]
    
    walls = pygame.sprite.Group()
    goals = pygame.sprite.Group()
    all_enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    floor_rects = []
    player = None
    patrol_list = []
    guard_list = []
    
    for row_indx, row_txt in enumerate(MAP_DATA):
        for col_indx, tile_char in enumerate(row_txt):
            x = col_indx * TILE_SIZE
            y = row_indx * TILE_SIZE
            
            if tile_char == "W":
                walls.add(Wall(x,y))
                