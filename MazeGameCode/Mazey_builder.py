import random

import pygame

from Mazey_constants import ALL_POWERUPS, DIFFICULTY, TILE_SIZE
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
    