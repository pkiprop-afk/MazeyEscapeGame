import random

import pygame

from Mazey_constants import ALL_POWERUPS, DIFFICULTY, TILE_SIZE
from Mazey_spritesandgroups import Goal, GuardEnemy, PatrolEnemy, Player, Powerup, Wall

def build_map(difficulty_key):
    settin