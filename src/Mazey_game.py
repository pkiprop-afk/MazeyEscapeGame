import pygame
import sys

from Mazey_constants import (
    DARK_BACKGROUND,
    DARK_GREY,
    DIFFICULTY,
    GRAY,
    BLACK,
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
        self.screen.blit(h, h.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))
        s = self.font_medium.render(subtitle, True, WHITE)
        self.screen.blit(s, s.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))
    
    # MAIN Game loop
    def run(self):
        running = True
        
        while running:
            self.clock.tick(MAX_FPS)
            delta = self.clock.get_time() / 1000.0
            
            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self._handle_key(event.key)
            
            self._update(delta)
            self._draw()
            pygame.display.flip
            
        pygame.quit()
        sys.exit()
    
    def _handle_key(self, key):
        if self.state == STATE_LOADING:
            if key == pygame.K_RETURN and self._load_done:
                self.state = STATE_DIFFICULT
        
        elif self.state == STATE_DIFFICULT:
            if key in (pygame.K_UP, pygame.K_w):
                self._diff_selected = (self._diff_selected - 1) % 3
            
            if key in (pygame.K_DOWN, pygame.K_s):
                self._diff_selected = (self._diff_selected + 1) % 3
            
            if key == pygame.K_RETURN:
                self.difficult = self._diff_selected[self._diff_selected]
                self._build_level()
        
        elif self.state == STATE_PLAYING:
        # Space fires a bullet if the player has a weapon
            if key == pygame.K_SPACE and self.player.weapon and self.player.bullets > 0:
                b = Bullet(
                    self.player.rect.centerx,
                    self.player.rect.centery,
                    self.player.facing
                )
                self.bullets.add(b)
                self.player.bullets -= 1
                if self.player.bullets <= 0:
                    self.player.weapon = None
        
        elif self.state in (STATE_WIN, STATE_GAMEOVER):
            if key == pygame.K_RETURN:
                self._reset()
                self.state = STATE_DIFFICULT
    
    def _update(self, delta):
        if self.state == STATE_LOADING:
            self._update_loading(delta)
        elif self.state == STATE_PLAYING:
            self._update_playing(delta)
    
    # Loading screen
    def _update_loading(self, delta):
        self._load_timer += delta
        if self._load_timer >= 3.0:
            self._load_done = True
    
    def _update_playing(self, delta):
        """ 
        Updates the main game while the player is still playing
        """
        slow_game = 0.35 if self.player.slow_time else 1.0
        
        # countdown timer to indicate game over when the time hits zero
        self.time_left -= delta
        if self.time_left <=0:
            self.time_left = 0
            self.state = STATE_GAMEOVER
            return
        
        self.player.update(delta, self.walls)
        
        for enemy in self.all_enemies:
            enemy.update(delta, self.walls, self.player, slow_game)
        
        # updating bullet movement
        for bullet in list(self.bullets):
            bullet.update(delta, self.walls)
        
        # Goal door animation
        self.goals.update()
        
        # for collecting powerup while walking over it
        for pu in pygame.sprite.spritecollide(self.player, self.powerups, True):
            if pu.pu_type == PU_AUTO_WIN:
                self.state = STATE_WIN
                return
            self.player.apply_powerup(pu.pu_type, list(self.all_enemies))
        
        # Bullet hits enemy and both are removed
        for bullet in list(self.bullets):
            for enemy in pygame.sprite.spritecollide(bullet, self.all_enemies, False):
                enemy.kill
                bullet.kill
        
        # Win when player reaches the exit door
        if pygame.sprite.spritecollide(self.player, self.goals, False):
            self.state = STATE_WIN
        
        # Lose when the enemy catches the player
        if pygame.sprite.spritecollide(self.player, self.all_enemies, False):
            self.state = STATE_GAMEOVER
    
    def _draw(self):
        self.screen.fill(DARK_BACKGROUND)
        
        if self.state ==  STATE_LOADING:
            self._draw_loading()
        elif self.state == STATE_DIFFICULT:
            self._draw_difficulty()
        elif self.state == STATE_PLAYING:
            self._draw_playing()
        elif self.state == STATE_WIN:
            self._draw_playing()
            self._draw_overlay(" YOU ESCAPED!", GREEN, "ENTER to play again")
        elif self.state == STATE_GAMEOVER:
            self._draw_playing()
            self._draw_overlay("CAUGHT! YOU LOST", RED, "ENTER to try again")
    
    # Loading screen
    def _draw_loading(self):
        self.screen.fill(DARK_BACKGROUND)
        
        # TITLE
        t = self.font_title.render("MAZEY", True, YELLOW)
        self.screen.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120)))
        s = self.font_small.render("The Office Escape", True, GRAY)
        self.screen.blit(s, s.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70)))
        
        # WORD BOX
        box = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 30, 240, 60)
        pygame.draw.rect(self.screen, DARK_GREY, box, border_radius=8)
        pygame.draw.rect(self.screen, PLAYER_COL, box, 2, border_radius=8)
        label = self.font_medium.render("LET'S PLAY!", True, PLAYER_COL)
        self.screen.blit(label, label.get_rect(center=box.center))
        
        # LOADING BAR
        bar_w = int((min(self._load_timer, 3.0) / 3.0) * 300)
        pygame.draw.rect(self.screen, DARK_BACKGROUND,(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 60, 300, 12), border_radius=6)
        pygame.draw.rect(self.screen, PLAYER_COL, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 60, bar_w, 12), border_radius=6)
        
        if self._load_done:
            p = self.font_small.render(" Press ENTER to continue", True, WHITE)
            self.screen.blit(p, p.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))
        
    # Difficulty selection screen
    def _draw_difficulty(self):
        self.screen.fill(DARK_BACKGROUND)
        t = self.font_title.render("SELECT DIFFICULTY", True, YELLOW)
        self.screen.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, 100)))
        
        desc = {
            "EASY":     ("120s | 2 Patrol | 1 Guard", GREEN),
            "HARD":     (" 75s | 3 Patrol | 2 Guards", ORANGE),
            "VETERAN":  (" 45s | 5 Patrol | 2 Guards", RED),
        }
        
        for i, opt in enumerate(self._diff_options):
            y = 220 + i * 110
            if  i == self._diff_selected:
                color = YELLOW
            else:
                GRAY
            box = pygame.Rect(SCREEN_WIDTH // 2 - 200, y - 10, 400, 80)
            if i == self._diff_selected:
                pygame.draw.rect(self.screen, DARK_GREY, box, border_radius=6)
                pygame.draw.rect(self.screen, YELLOW, box, 2, border_radius=6)
            label = self.font_medium.render(opt, True, color)
            self.screen.blit(label, label.get_rect(center=(SCREEN_WIDTH // 2, y +12)))
            d_text, d_color = desc[opt]
            d_label = self.font_small.render(d_text, True, d_color)
            self.screen.blit(d_label, d_label.get_rect(center=(SCREEN_WIDTH // 2, y + 44)))
        
        hint = self.font_small.render("UP/DOWN to select | ENTER to start", True, GRAY)
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)))
    
    # Main Gameplay
    def _draw_playing(self):
        # floor tiles
        for r in self.floor_rects:
            draw_floor(self.screen, r.x, r.y)
        
        # walls
        self.walls.draw(self.screen)
        
        # All the game sprites
        self.sll_sprites.draw(self.screen)
        
        # Flashlight overlaying darkness
        draw_flashlight(self.screen, self.player.rect.center, self.player.flash_radius, self.player.flash_battery)
        
        # Heads UP Display (HUD)
        self._draw_hud()
    
    def _draw_hud(self):
        hud = pygame.Surface((SCREEN_WIDTH, 36), pygame.SRCALPHA)
        hud.fill((BLACK, 180))
        self.screen.blit(hud, (0,0))
        
        # Timer
        mins = int(self.time_left) // 60
        secs = int(self.time_left) % 60
        if self.time_left < 15:
            RED
        elif self.time_left < 30:
            ORANGE
        else:
            WHITE
            
        