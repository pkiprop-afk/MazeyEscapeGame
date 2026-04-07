import pygame
import sys

from Mazey_constants import (
    DARK_BACKGROUND,
    DARK_GREY,
    DIFFICULTY,
    GRAY,
    GREEN,
    ORANGE, 
    MAX_FPS,
    PLAYER_COL,
    PLAYER_EYE,
    PU_AUTO_WIN,
    PU_COLORS,
    RED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STATE_DIFFICULT,
    STATE_GAMEOVER, 
    STATE_LOADING,
    STATE_PLAYING,
    STATE_TITLE,
    STATE_WIN,
    TITLE,
    WHITE,
    YELLOW,
)

from draw_func import draw_flashlight, draw_floor
from Mazey_builder import build_map
from Mazey_spritesandgroups import Bullet

class Game:
    def __init__(self):
        pygame.init()