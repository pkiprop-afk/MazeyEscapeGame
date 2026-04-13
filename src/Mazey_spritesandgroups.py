import math
import os
import random
import pygame

from Mazey_constants import(
    RED,
    BLUE,
    BLACK,
    DARK_BACKGROUND,
    ENEMY_COL,
    ENEMY_EYE,
    FLASH_RADIUS,
    FLASH_RADIUS_MIN,
    FREEZE_COL,
    GOAL_GLOW,
    GUARD_COL,
    GUARD_EYE,
    PLAYER_COL,
    PLAYER_EYE,
    PU_AUTO_WIN,
    PU_COLORS,
    PU_FREEZE,
    PU_SLOW_TIME,
    PU_SPEED_UP,
    PU_TELEPORT,
    PU_WEAPON,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
    WALL_DARK,
    WALL_LIGHT,
    WEAPONS,
    WEAPON_BULLETS,
    WHITE,
    YELLOW,
)


class Wall(pygame.sprite.Sprite):
    """ 
    A solid wall tile used for collision and level boundaries.

    This sprite renders a single wall block at a fixed grid position and blocks
    movement for players, enemies, and other colliding entities.
    """
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
    """ 
    An animated goal tile that represents the maze exit.

    This sprite displays a glowing door-like graphic and updates its visual
    animation over time to draw the player's attention.
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self._animation_timer = 0
        self._draw(0)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def _draw(self, glow_set):
        self.image.fill(DARK_BACKGROUND)
        pygame.draw.rect(self.image, YELLOW, (4, 2, TILE_SIZE - 8, TILE_SIZE - 4 ))
        pygame.draw.rect(self.image, GOAL_GLOW, (6, 4, TILE_SIZE - 12, TILE_SIZE - 8), 2)
        pygame.draw.circle(self.image, WHITE, (TILE_SIZE - 10, TILE_SIZE // 2 + glow_set), 3 )
    
    def update(self):
        self._animation_timer += 1
        ofset = int(math.sin(self._animation_timer * 0.1 ) * 2)
        self._draw(ofset)
    
class Enemy(pygame.sprite.Sprite):
    """ 
    A simple horizontal enemy that bounces between walls and screen edges.

    This sprite moves along a line, reverses direction on collisions, and can be
    reset back to its original position.
    """
    START_X = 680
    START_Y = 300
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.reset()
    
    def reset(self):
        """
        Returns enemy to starting positions
        """
        self.rect.topleft = (self.START_X, self.START_Y)
        self._vel_x = - ENEMY_SPEED
    
    def update(self, delta, walls):
        """ 
        Bouncing of walls and screen edges
        """
        self.rect.x += int(self._vel_x * delta)
        
        # Bouncing screen edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self._vel_x *= -1
        
        # Bouncing of walls
        for wall in pygame.sprite.spritecollide(self, walls, False):
            self._vel_x *= -1
            
            # prevent sticking
            if self._vel_x > 0:
                self.rect.left = wall.rect.right
            else:
                self.rect.right = wall.rect.left

class Player(pygame.sprite.Sprite):
    """ 
    The controllable character that moves through the maze and interacts with enemies and powerups.

    This sprite handles player input, movement with collision, flashlight state, and
    the activation and expiration of powerup effects such as speed, slow time, and weapons.
    """
    # starting positions
    START_X = 0
    START_Y = 0
    
    def __init__(self, x, y, speed):
        super().__init__()
        self.base_speed = speed 
        self.speed = speed
        self.image = pygame.Surface((TILE_SIZE - 6, TILE_SIZE - 6), pygame.SRCALPHA)
        self._load_image()
        self.rect = self.image.get_rect(topleft=(x,y))
        Player.START_X = x
        Player.START_Y = y
        
        #Flashlight
        self.flash_radius = FLASH_RADIUS
        self.flash_battery = 1.0
        
        # For power ups
        self.active_powerup = None
        self.powerup_timer = 0.0
        self.weapon = None
        self.bullets = 0
        self.slow_time = False
        self.speed_boost = False
        
        # For facing the direction for shooting
        self.facing = pygame.math.Vector2(1,0)
    
    def _load_image(self):
        """ 
        Tries to load image from the same folder
        """
        try:
            _path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "player.png")
            raw = pygame.image.load("player.png").convert_alpha()
            self.image = pygame.transform.scale(raw, (TILE_SIZE - 6, TILE_SIZE - 6))
        
        except FileNotFoundError:
            self.image = pygame.Surface((TILE_SIZE - 6, TILE_SIZE - 6), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
            pygame.draw.rect(self.image, PLAYER_COL, (0, 0, TILE_SIZE - 6, TILE_SIZE-6))
        
    def reset(self):
        self.rect.topleft = (self.START_X, self.START_Y)
        self.flash_battery = 1.0
        self.flash_radius = FLASH_RADIUS
        self.active_powerup = None
        self.powerup_timer = 0.0
        self.weapon = None
        self.bullets = 0
        self.slow_time = False
        self.speed_boost = False
        self.speed = self.base_speed
    
    def update(self, delta, walls):
        keys = pygame.key.get_pressed()
        
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        
        # Bullet direction
        if dx != 0 or dy != 0:
            self.facing = pygame.math.Vector2(dx, dy).normalize()
        
        # Horizontal move and collisions
        self.rect.x += int(self.speed * dx * delta)
        for wall in pygame.sprite.spritecollide(self, walls, False):
            if dx > 0:
                self.rect.right = wall.rect.left
            if dx < 0:
                self.rect.left = wall.rect.right
        
        # vertical move and collision
        self.rect.y += int(self.speed * dy * delta)
        for wall in pygame.sprite.spritecollide(self, walls, False):
            if dy > 0:
                self.rect.bottom = wall.rect.top
            if dy < 0:
                self.rect.top = wall.rect.bottom
        
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Power up timer
        if self.powerup_timer > 0:
            self.powerup_timer -= delta
            if self.powerup_timer <= 0:
                self._expire_powerup()
    
    # power up expire
    def _expire_powerup(self):
        if self.active_powerup == PU_SLOW_TIME:
            self.slow_time = False
        if self.active_powerup == PU_SPEED_UP:
            self.speed = self.base_speed
            self.speed_boost = False
        self.active_powerup = None
    
    def apply_powerup(self, pu_type, enemies):
        if pu_type == PU_SLOW_TIME:
            self.slow_time = True
            self.active_powerup = pu_type
            self.powerup_timer = 8.0

        elif pu_type == PU_SPEED_UP:
            self.speed = self.base_speed * 1.8
            self.speed_boost = True
            self.active_powerup = pu_type
            self.powerup_timer = 6.0

        elif pu_type == PU_WEAPON:
            self.weapon = random.choice(WEAPONS)
            self.bullets = WEAPON_BULLETS[self.weapon]

        elif pu_type == PU_TELEPORT:
            patrol_only = [
                enemy
                for enemy in enemies
                if isinstance(enemy, PatrolEnemy) and not isinstance(enemy, GuardEnemy)
            ]
            if patrol_only:
                target = random.choice(patrol_only)
                old_position = self.rect.topleft
                self.rect.topleft = target.rect.topleft
                target.rect.topleft = old_position

        elif pu_type == PU_FREEZE:
            for enemy in enemies:
                enemy.freeze(5.0)
            self.active_powerup = pu_type
            self.powerup_timer = 5.0

        elif pu_type == PU_AUTO_WIN:
            pass

class Bullet(pygame.sprite.Sprite):
    """ 
    A fast-moving projectile fired by the player's weapon.

    This sprite travels in a straight line until it hits a wall or leaves the
    screen, at which point it is removed from the game.
    """
    SPEED = 500
    
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (3,3), 3)
        self.rect = self.image.get_rect(center=(x,y))
        self.vel = direction * self.SPEED
        self._fx = float(self.rect.x)
        self._fy = float(self.rect.y)
    
    def update(self, delta, walls):
        """ 
        delta will keep the bullet speed consistent
        """
        self._fx += self.vel.x * delta
        self._fy += self.vel.y * delta
        self.rect.x = int(self._fx)
        self.rect.y =  int(self._fy)
    
        # deletes the bullet if it leaves the screen
        if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).colliderect(self.rect):
            self.kill()
            return

        if pygame.sprite.spritecollide(self, walls, False):
            self.kill()

class Powerup(pygame.sprite.Sprite):
    """ 
    A collectible item that grants temporary abilities or effects to the player.

    This sprite represents different powerup types with distinct colors and labels,
    and applies their effects when picked up during gameplay.
    """
    def __init__(self, x, y, pu_type):
        super().__init__()
        self.pu_type = pu_type
        size = TILE_SIZE - 8
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self._draw(size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x + 4, y + 4)
    
    def _draw(self, size):
        color = PU_COLORS.get(self.pu_type, WHITE)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2 - 4)
        font = pygame.font.SysFont("Times", 12, bold=True)
        label = font.render(self.pu_type[0], True, BLACK)
        self.image.blit(label, label.get_rect(center=(size // 2, size // 2)))
    
    def update(self):
        pass

class PatrolEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=90):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 6, TILE_SIZE - 6), pygame.SRCALPHA)
        self._load_image(ENEMY_COL)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._start = (x, y)
        self.speed = speed
        self._vel_x = speed
        self._vel_y = 0
        self.frozen = False
        self.freeze_timer = 0.0
        self.alert = False
    
    def _load_image(self, fall_color):
        """ 
        Tries to load enemy.png from the same folder
        """
        try:
            _path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "enemy.png")
            raw = pygame.image.load(_path).convert_alpha()
            self.image = pygame.transform.scale(raw, (TILE_SIZE - 6, TILE_SIZE - 6))
        
        except FileNotFoundError:
            self.image = pygame.Surface((TILE_SIZE - 6, TILE_SIZE - 6), pygame.SRCALPHA)
            self.image.fill(BLACK)
            pygame.draw.rect(self.image, fall_color, (0, 0, TILE_SIZE - 6, TILE_SIZE - 6))
    
    def reset(self):
        """ 
        Returns enemy to starting positions
        """
        self.rect.topleft = self._start
        self._vel_x = self.speed
        self._vel_y = 0
        self.frozen = False
        self.alert = False
        self._load_image(ENEMY_COL)
    
    def freeze(self, duration=5.0):
        """ 
        stops the enemy and tints blue for a certain duration
        """
        self.frozen = True
        self.freeze_timer = duration
        tint = self.image.copy()
        tint.fill(BLUE)
        self.image = tint
    
    def update(self, delta, walls, player, slow = 1.0):
        """ 
        chase behavior for the patrol enemy
        """
        if self.frozen:
            self.freeze_timer -= delta
            if self.freeze_timer <= 0:
                self.frozen = False
                self._load_image(ENEMY_COL)
            return

        # effects of slow time power up
        eff = delta * slow

        px, py = player.rect.centerx, player.rect.centery
        ex, ey = self.rect.centerx, self.rect.centery

        # distance
        dist = math.hypot(px - ex, py - ey)

        # patrol enemy switches to chase mode within the detection range
        self.alert = dist < FLASH_RADIUS * 1.5

# sourcery skip: merge-nested-ifs
        if self.alert:
            if dist > 0:
                dx = (px - ex) / dist
                dy = (py - ey) / dist
                self.rect.x += int(self.speed * dx * eff)

                for wall in pygame.sprite.spritecollide(self, walls ,False):
                    if dx > 0:
                        self.rect.right = wall.rect.left
                    else:
                        self.rect.left = wall.rect.right

                self.rect.y += int(self.speed * dy * eff)

                for wall in pygame.sprite.spritecollide(self, walls ,False):
                    if dy > 0:
                        self.rect.bottom = wall.rect.top
                    else:
                        self.rect.top = wall.rect.bottom

class GuardEnemy(PatrolEnemy):
    def __init__(self, x, y, speed=70):
        super().__init__(x, y, speed)
        self._load_image(GUARD_COL)
        self._guard_pos = (x, y)
    
    def reset(self):
        self.rect.topleft = self._start
        self._vel_x = self.speed
        self._vel_y = 0
        self.frozen =  False
        self.alert = False
        self._load_image(GUARD_COL)
    
    def _load_image(self, fall_color):
        """ 
        Tries to load guard.png from the same folder
        """
        try:
            raw = pygame.image.load("guard.png").convert_alpha()
            self.image = pygame.transform.scale(raw, (TILE_SIZE - 6, TILE_SIZE - 6))
        
        except FileNotFoundError:
            self.image = pygame.Surface((TILE_SIZE - 6, TILE_SIZE -6), pygame.SRCALPHA)
            self.image.fill(BLACK)
            pygame.draw.rect(self.image, fall_color, (0, 0, TILE_SIZE - 6, TILE_SIZE - 6))
    
    def update(self, delta, walls, player, slow=1):
        if self.frozen:
            self.freeze_timer -= delta
            if self.freeze_timer <= 0:
                self.frozen = False
                self._load_image(GUARD_COL)
            return
        
        # effects of slow time power up
        eff = delta * slow

        px, py = player.rect.centerx, player.rect.centery
        ex, ey = self.rect.centerx, self.rect.centery

        # distance
        dist = math.hypot(px - ex, py - ey)

        # patrol enemy switches to chase mode within the detection range
        self.alert = dist < FLASH_RADIUS * 1.5


# sourcery skip: merge-nested-ifs
        if self.alert:
            if dist > 0:
                dx = (px - ex) / dist
                dy = (py - ey) / dist
                self.rect.x += int(self.speed * dx * eff)

                for wall in pygame.sprite.spritecollide(self, walls ,False):
                    if dx > 0:
                        self.rect.right = wall.rect.left
                    else:
                        self.rect.left = wall.rect.right

                self.rect.y += int(self.speed * dy * eff)

                for wall in pygame.sprite.spritecollide(self, walls ,False):
                    if dy > 0:
                        self.rect.bottom = wall.rect.top
                    else:
                        self.rect.top = wall.rect.bottom
        
        else:
            # make sure the guard returns to his post
            gx, gy = self._guard_pos
            dx = gx - self.rect.x
            dy = gy - self.rect.y
            
            dist_post = math.hypot(dx, dy)
            if dist_post > 4:
                self.rect.x += int((dx / dist_post) * self.speed * 0.5 * eff)
                self.rect.y += int((dy / dist_post) * self.speed * 0.5 * eff)
        
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))