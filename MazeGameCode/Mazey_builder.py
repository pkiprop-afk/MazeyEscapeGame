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
            
            elif tile_char == ".":
                floor_rects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            
            elif tile_char == "P":
                floor_rects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                player = Player( x + 2, y + 2, settings["speed"])
            
            elif tile_char == "G":
                floor_rects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                goals.add(Goal(x, y))
    
    safe_floors = [r for r in floor_rects if r.x > TILE_SIZE * 4]
    random.shuffle(safe_floors)
    
    for i in range(min(settings["patrol"], len(safe_floors))):
        rect = safe_floors[i]
        patrol = PatrolEnemy(rect.x + 2, rect.y + 2, speed=90 + i * 10)
        