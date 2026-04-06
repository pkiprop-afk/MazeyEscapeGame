import random

import pygame

from .Mazey_constants import(
    FLOOR_DARK,
    FLOOR_LIGHT, 
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
    BLACK,
)

def draw_floor(surface, x, y):
    pygame.draw.rect(surface, FLOOR_DARK, (x, y, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(surface, FLOOR_LIGHT, (x, y + TILE_SIZE  // 2, TILE_SIZE, 1))
    pygame.draw.rect(surface, FLOOR_LIGHT, (x + TILE_SIZE // 2, y, 1, TILE_SIZE))

def draw_flashlight(screen, player_center, radius, battery):
    darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    darkness.fill(BLACK)
    
    cx, cy = player_center
    for r in range(radius, 0, -8):
        alpha = max(0, int(230 * (1 - r /radius)))
        pygame.draw.circle(darkness, (0, 0, 0, alpha), (cx, cy), r)
    
    if battery < 0.2 and random.random() < 0.05:
        darkness.fill