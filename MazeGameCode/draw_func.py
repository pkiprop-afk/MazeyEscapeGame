import random

import pygame

from .Mazey_constants import(
    FLOOR_DARK,
    FLOOR_LIGHT, 
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
)

def draw_floor(surface, x, y):
    pygame.draw.rect(surface, FLOOR_DARK, (x, y, TILE_SIZE, TILE_SIZE))
    