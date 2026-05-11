# # game_dodge.py
# import pygame
# import random
# import config as cfg
# from graphics import Particle

# class DodgeGame:
#     def __init__(self, audio, hud, particles):
#         self.audio = audio
#         self.hud = hud
#         self.particles = particles
#         self.reset()
    
#     def reset(self):
#         # HORIZONTAL BAR (60x20 pixels) INSTEAD OF SQUARE
#         self.player = pygame.Rect(cfg.SCREEN_WIDTH // 2 - 30, cfg.SCREEN_HEIGHT - 80, 60, 20)
#         self.player_color = cfg.NEON_PINK
#         self.score = 0
#         self.time_left = 60.0
#         self.obstacles = []
#         self.stars = []
#         self.speed = 300
#         self.running = True
#         self.spawn_timer = 0
    
#     def update(self, dt, keys, clicks=None):
#         if not self.running:
#             return self.score
        
#         self.time_left -= dt
#         if self.time_left <= 0:
#             self.time_left = 0
#             self.running = False
#             return self.score
        
#         # Player movement (LEFT/RIGHT only)
#         spd = 500
#         if keys[pygame.K_a] or keys[pygame.K_LEFT]:
#             self.player.x -= spd * dt
#         if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
#             self.player.x += spd * dt
        
#         self.player.x = max(50, min(cfg.SCREEN_WIDTH - 110, self.player.x))
        
#         # Increase difficulty
#         self.speed += dt * 5
#         self.spawn_timer += dt
        
#         # Spawn obstacles and stars
#         if self.spawn_timer > max(0.4, 1.0 - self.score / 500):
#             if random.random() < 0.7:
#                 w = random.randint(40, 120)
#                 x = random.randint(50, cfg.SCREEN_WIDTH - 50 - w)
#                 self.obstacles.append({'rect': pygame.Rect(x, -50, w, 30), 'col': cfg.NEON_RED})
#             else:
#                 self.stars.append({'rect': pygame.Rect(random.randint(50, cfg.SCREEN_WIDTH - 90), -30, 20, 20), 'col': cfg.NEON_YELLOW})
#             self.spawn_timer = 0
        
#         # Update obstacles
#         for o in self.obstacles[:]:
#             o['rect'].y += self.speed * dt
#             if o['rect'].y > cfg.SCREEN_HEIGHT:
#                 self.obstacles.remove(o)
#             elif self.player.colliderect(o['rect']):
#                 self.running = False
#                 self.audio.play_sfx(150, 0.3, 0.5)
#                 return self.score
        
#         # Update stars (collectibles)
#         for s in self.stars[:]:
#             s['rect'].y += self.speed * dt * 0.8
#             if s['rect'].y > cfg.SCREEN_HEIGHT:
#                 self.stars.remove(s)
#             elif self.player.colliderect(s['rect']):
#                 self.score += 50
#                 self.audio.play_sfx(1000, 0.1, 0.3)
#                 for _ in range(8):
#                     self.particles.append(Particle(s['rect'].centerx, s['rect'].centery, s['col']))
#                 self.stars.remove(s)
        
#         return self.score
    
#     def draw(self, surf):
#         for o in self.obstacles:
#             pygame.draw.rect(surf, o['col'], o['rect'], border_radius=6)
        
#         for s in self.stars:
#             pygame.draw.circle(surf, s['col'], s['rect'].center, 10)
#             pygame.draw.circle(surf, cfg.WHITE, s['rect'].center, 10, 2)
        
#         # Draw BAR (horizontal rectangle)
#         pygame.draw.rect(surf, self.player_color, self.player, border_radius=10)
#         pygame.draw.rect(surf, cfg.WHITE, self.player, 3, border_radius=10)
#         self.hud.draw(surf, self.score, self.time_left, "DODGE RED | CATCH YELLOW")

# game_dodge.py
import pygame
import random
import config as cfg
from graphics import Particle

class DodgeGame:
    def __init__(self, audio, hud, particles):
        self.audio, self.hud, self.particles = audio, hud, particles
        self.reset()
    def reset(self, difficulty="MEDIUM"):
        self.difficulty = difficulty
        self.player = pygame.Rect(cfg.SCREEN_WIDTH//2-30, cfg.SCREEN_HEIGHT-100, 60, 20)
        self.player_color = cfg.ACCENT_PINK
        self.score, self.lives = 0, 3
        self.obstacles, self.stars = [], []
        self.speed, self.running, self.spawn_timer = 350, True, 0

    def update(self, dt, keys, clicks=None):
        if not self.running: return self.score, self.lives
        spd = 600
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.player.x -= spd*dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.player.x += spd*dt
        self.player.x = max(50, min(cfg.SCREEN_WIDTH-110, self.player.x))

        self.speed += dt * 8
        self.spawn_timer += dt
        if self.spawn_timer > max(0.3, 0.9 - self.score/600):
            if random.random() < 0.75:
                w = random.randint(50, 140)
                self.obstacles.append({'rect': pygame.Rect(random.randint(50, cfg.SCREEN_WIDTH-50-w), -50, w, 30), 'col': cfg.ACCENT_RED})
            else:
                self.stars.append({'rect': pygame.Rect(random.randint(50, cfg.SCREEN_WIDTH-90), -30, 22, 22), 'col': cfg.ACCENT_YELLOW})
            self.spawn_timer = 0

        for o in self.obstacles[:]:
            o['rect'].y += self.speed*dt
            if o['rect'].y > cfg.SCREEN_HEIGHT: self.obstacles.remove(o)
            elif self.player.colliderect(o['rect']):
                self.lives -= 1
                self.audio.play_sfx(150, 0.3, 0.5)
                for _ in range(12): self.particles.append(Particle(self.player.centerx, self.player.centery, cfg.ACCENT_RED, speed=4))
                if self.lives <= 0: self.running = False
                return self.score, self.lives

        for s in self.stars[:]:
            s['rect'].y += self.speed*dt*0.85
            if s['rect'].y > cfg.SCREEN_HEIGHT: self.stars.remove(s)
            elif self.player.colliderect(s['rect']):
                self.score += 50
                self.audio.play_sfx(1000, 0.1, 0.3)
                # Grow bar
                if self.player.w < cfg.SCREEN_WIDTH * 0.45:
                    self.player.w += 12
                for _ in range(10): self.particles.append(Particle(s['rect'].centerx, s['rect'].centery, s['col']))
                self.stars.remove(s)
        return self.score, self.lives

    def draw(self, surf):
        for o in self.obstacles:
            pygame.draw.rect(surf, o['col'], o['rect'], border_radius=8)
        for s in self.stars:
            pygame.draw.circle(surf, s['col'], s['rect'].center, 11)
            pygame.draw.circle(surf, cfg.WHITE, s['rect'].center, 11, 2)
        pygame.draw.rect(surf, self.player_color, self.player, border_radius=12)
        pygame.draw.rect(surf, cfg.WHITE, self.player, 3, border_radius=12)
        self.hud.draw(surf, self.score, self.lives, "TIMELESS", is_timeless=True)