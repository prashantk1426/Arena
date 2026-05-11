# # game_collector.py
# import pygame
# import random
# import math
# import config as cfg
# from graphics import Particle

# class Obstacle:
#     def __init__(self, x, y, w, h, moving=False, speed=0):
#         self.rect = pygame.Rect(x, y, w, h)
#         self.moving = moving
#         self.speed = speed
#         self.dir = 1
    
#     def update(self, dt, bounds):
#         if self.moving:
#             self.rect.x += self.speed * self.dir * dt
#             if self.rect.left < bounds[0] or self.rect.right > bounds[1]:
#                 self.dir *= -1
    
#     def draw(self, surf):
#         pygame.draw.rect(surf, cfg.NEON_RED, self.rect, border_radius=8)
#         pygame.draw.rect(surf, cfg.WHITE, self.rect, 2, border_radius=8)

# class ArenaGame:
#     def __init__(self, audio, hud, particles):
#         self.audio = audio
#         self.hud = hud
#         self.particles = particles
#         self.reset()
    
#     def reset(self):
#         # SQUARE COLLECTOR (40x40 pixels) - NOT A BAR
#         self.player = pygame.Rect(550, 350, 40, 40)
#         self.player_color = cfg.NEON_BLUE
#         self.score = 0
#         self.time_left = 60.0
#         self.gems = []
#         self.obstacles = [
#             Obstacle(200, 300, 150, 20, moving=True, speed=150),
#             Obstacle(800, 450, 150, 20, moving=True, speed=-120),
#             Obstacle(400, 200, 20, 150, moving=False),
#             Obstacle(700, 550, 200, 20, moving=False)
#         ]
#         self.running = True
#         self.spawn_timer = 0
    
#     def spawn_gem(self):
#         x = random.randint(100, cfg.SCREEN_WIDTH - 100)
#         y = random.randint(50, cfg.SCREEN_HEIGHT - 100)
#         val = random.choice([10, 20, 50])
#         col = cfg.NEON_GREEN if val == 50 else cfg.NEON_YELLOW if val == 20 else cfg.NEON_BLUE
#         self.gems.append({'rect': pygame.Rect(x, y, 20, 20), 'val': val, 'col': col, 'pulse': 0})
    
#     def update(self, dt, keys, clicks=None):
#         if not self.running:
#             return self.score
        
#         self.time_left -= dt
#         if self.time_left <= 0:
#             self.time_left = 0
#             self.running = False
#             return self.score
        
#         # 4-DIRECTION MOVEMENT (WASD + ARROWS)
#         spd = 400
#         if keys[pygame.K_w] or keys[pygame.K_UP]:
#             self.player.y -= spd * dt
#         if keys[pygame.K_s] or keys[pygame.K_DOWN]:
#             self.player.y += spd * dt
#         if keys[pygame.K_a] or keys[pygame.K_LEFT]:
#             self.player.x -= spd * dt
#         if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
#             self.player.x += spd * dt
        
#         # Keep in bounds
#         self.player.x = max(50, min(cfg.SCREEN_WIDTH - 90, self.player.x))
#         self.player.y = max(50, min(cfg.SCREEN_HEIGHT - 90, self.player.y))
        
#         # Update obstacles
#         for obs in self.obstacles:
#             obs.update(dt, (50, cfg.SCREEN_WIDTH - 50))
        
#         # MUCH SLOWER SPAWN (3 seconds between orbs - NOT messy)
#         self.spawn_timer += dt
#         if self.spawn_timer > 3.0:
#             self.spawn_gem()
#             self.spawn_timer = 0
        
#         # Check gem collection
#         for g in self.gems[:]:
#             g['pulse'] += dt * 3
#             if self.player.colliderect(g['rect']):
#                 self.score += g['val']
#                 self.audio.play_sfx(800, 0.1, 0.3)
#                 for _ in range(10):
#                     self.particles.append(Particle(g['rect'].centerx, g['rect'].centery, g['col']))
#                 self.gems.remove(g)
        
#         # Check obstacle collision
#         for obs in self.obstacles:
#             if self.player.colliderect(obs.rect):
#                 self.score = max(0, self.score - 20)
#                 self.audio.play_sfx(200, 0.2, 0.4)
#                 self.player.x = 550
#                 self.player.y = 350
#                 break
        
#         return self.score
    
#     def draw(self, surf):
#         for obs in self.obstacles:
#             obs.draw(surf)
        
#         for g in self.gems:
#             s = 10 + math.sin(g['pulse']) * 3
#             pygame.draw.circle(surf, (*g['col'][:3], 150), g['rect'].center, int(s * 1.2))
#             pygame.draw.circle(surf, g['col'], g['rect'].center, int(s))
        
#         # Draw SQUARE collector (not a bar)
#         pygame.draw.rect(surf, self.player_color, self.player, border_radius=8)
#         pygame.draw.rect(surf, cfg.WHITE, self.player, 3, border_radius=8)
        
#         self.hud.draw(surf, self.score, self.time_left, "USE WASD or ARROWS TO MOVE")

# game_collector.py
import pygame
import random
import math
import config as cfg
from graphics import Particle

class Obstacle:
    def __init__(self, x, y, w, h, moving=False, speed=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.moving = moving
        self.speed = speed
        self.dir = 1
    def update(self, dt, bounds):
        if self.moving:
            self.rect.x += self.speed * self.dir * dt
            if self.rect.left < bounds[0] or self.rect.right > bounds[1]: self.dir *= -1
    def draw(self, surf):
        pygame.draw.rect(surf, cfg.ACCENT_RED, self.rect, border_radius=8)
        pygame.draw.rect(surf, cfg.WHITE, self.rect, 2, border_radius=8)

class ArenaGame:
    def __init__(self, audio, hud, particles):
        self.audio, self.hud, self.particles = audio, hud, particles
        self.reset()
    def reset(self, difficulty="MEDIUM"):
        self.difficulty = difficulty
        cfg_map = cfg.COLLECTOR_CFG[difficulty]
        self.player = pygame.Rect(550, 350, 40, 40)
        self.player_color = cfg.ACCENT_BLUE
        self.score, self.lives, self.time_left = 0, 3, 60.0
        self.gems, self.obstacles = [], []
        self.running, self.spawn_timer = True, 0
        self.obstacle_speed = cfg_map["obs_speed"]
        
        # Generate obstacles based on difficulty
        for _ in range(cfg_map["obs_count"]):
            m = random.choice([True, False])
            self.obstacles.append(Obstacle(
                random.randint(100, cfg.SCREEN_WIDTH-200),
                random.randint(100, cfg.SCREEN_HEIGHT-200),
                random.randint(80, 180), 20, moving=m, speed=self.obstacle_speed
            ))
        if cfg_map["has_bombs"]: self.has_bombs = True
        else: self.has_bombs = False

    def spawn_gem(self):
        x = random.randint(100, cfg.SCREEN_WIDTH-100)
        y = random.randint(100, cfg.SCREEN_HEIGHT-150)
        is_bomb = self.has_bombs and random.random() < 0.15
        val = 0 if is_bomb else random.choice([10, 20, 50])
        col = cfg.ACCENT_BLACK if is_bomb else (cfg.ACCENT_GREEN if val==50 else cfg.ACCENT_YELLOW if val==20 else cfg.ACCENT_BLUE)
        self.gems.append({'rect': pygame.Rect(x, y, 20, 20), 'val': val, 'col': col, 'pulse': 0, 'spawn_time': pygame.time.get_ticks()/1000})

    def update(self, dt, keys, clicks=None):
        if not self.running: return self.score, self.lives
        self.time_left -= dt
        if self.time_left <= 0 or self.lives <= 0:
            self.time_left = 0; self.running = False
            return self.score, self.lives

        spd = 450
        if keys[pygame.K_w] or keys[pygame.K_UP]: self.player.y -= spd*dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: self.player.y += spd*dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.player.x -= spd*dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.player.x += spd*dt
        self.player.x = max(50, min(cfg.SCREEN_WIDTH-90, self.player.x))
        self.player.y = max(50, min(cfg.SCREEN_HEIGHT-90, self.player.y))

        for obs in self.obstacles: obs.update(dt, (50, cfg.SCREEN_WIDTH-50))

        self.spawn_timer += dt
        if self.spawn_timer > (2.5 if self.difficulty=="HARD" else 3.5):
            self.spawn_gem(); self.spawn_timer = 0

        current_time = pygame.time.get_ticks()/1000
        for g in self.gems[:]:
            g['pulse'] += dt*3
            if current_time - g['spawn_time'] > 3.0: self.gems.remove(g); continue
            if self.player.colliderect(g['rect']):
                if g['val'] == 0: # Bomb
                    self.lives -= 1
                    self.audio.play_sfx(100, 0.4, 0.5)
                    for _ in range(15): self.particles.append(Particle(g['rect'].centerx, g['rect'].centery, cfg.ACCENT_RED, speed=5))
                else:
                    self.score += g['val']
                    self.audio.play_sfx(800, 0.1, 0.3)
                    # Grow player slightly
                    if self.player.w < 80:
                        self.player.w += 1.5; self.player.h += 1.5
                    for _ in range(10): self.particles.append(Particle(g['rect'].centerx, g['rect'].centery, g['col']))
                self.gems.remove(g)

        for obs in self.obstacles:
            if self.player.colliderect(obs.rect):
                self.lives -= 1
                self.audio.play_sfx(200, 0.2, 0.4)
                self.player.x, self.player.y = 550, 350
                for _ in range(10): self.particles.append(Particle(self.player.centerx, self.player.centery, cfg.ACCENT_RED))
                break
        return self.score, self.lives

    def draw(self, surf):
        for obs in self.obstacles: obs.draw(surf)
        for g in self.gems:
            s = 10 + math.sin(g['pulse'])*3
            pygame.draw.circle(surf, (*g['col'][:3], 180), g['rect'].center, int(s*1.3))
            pygame.draw.circle(surf, g['col'], g['rect'].center, int(s))
            if g['val'] == 0: # Bomb icon
                pygame.draw.circle(surf, cfg.WHITE, g['rect'].center, 4)
        pygame.draw.rect(surf, self.player_color, self.player, border_radius=10)
        pygame.draw.rect(surf, cfg.WHITE, self.player, 3, border_radius=10)
        self.hud.draw(surf, self.score, self.lives, f"DIFF: {self.difficulty}", time_left=self.time_left)