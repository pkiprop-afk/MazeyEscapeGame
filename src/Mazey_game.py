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
        self.screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
    
    # Fonts
        self.font_title = pygame.font.SysFont("Courier", 64, bold=True)
        self.font_medium = pygame.font.SysFont("Courier", 22, bold=True)
        self.font_small = pygame.font.SysFont("Courier", 16)
    
    # Starts the game from the loading
        self.state = STATE_LOADING
        
    # Loading screen variables
        self._load_timer = 0.0
        self._load_done = False
        
    # Difficulty selection
        self._diff_options = [
            "EASY",
            "HARD",
            "VETERAN",
        ]
        self._diff_selected = 0
        self.difficult = "EASY"

        self.walls = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.all_enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.bullets  = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.floor_rects  =[]
        self.player = None
        self.time_left = 0.0
    
    # This functions builds the level using the map builder
    def _build_level(self):
        build_map(self.difficulty) = (self.walls, self.goals, self.all_enemies, self.powerups, self.player, self.floor_rects)
        
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.goals, self.powerups, self.all_enemies, self.player)
        self.time_left = float(DIFFICULTY[self.difficult]["time"])
        self.state = STATE_PLAYING
    
    # Resets the player and all the enemies to their starting positions
    def _reset(self):
        self.player.reset()
        for e in self.all_enemies:
            e.reset()
    
    # This function draws a semi-transparent overlay for win or game-over screens
    def _draw_overlay(self, heading, color, subtitle):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(GRAY)
        self.screen.blit(overlay, (0, 0))
        h = self.font_title.render(heading, True, color)
        self.screen.blit(h, h.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))