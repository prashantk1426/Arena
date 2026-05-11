# # graphics.py
# import pygame
# import random

# class Particle:
#     def __init__(self, x, y, color, speed=3, life=1.0):
#         self.x, self.y = x, y
#         self.color = color
#         self.vx, self.vy = random.uniform(-speed, speed), random.uniform(-speed, speed)
#         self.life, self.max_life = life, life
#         self.size = random.randint(2, 6)
#     def update(self, dt):
#         self.x += self.vx * dt; self.y += self.vy * dt
#         self.vy += 200 * dt
#         self.life -= dt
#     def draw(self, surf):
#         if self.life <= 0: return
#         a = int(255 * (self.life / self.max_life))
#         s = max(1, int(self.size * (self.life / self.max_life)))
#         pygame.draw.circle(surf, (*self.color[:3], a), (int(self.x), int(self.y)), s)

# class Background:
#     def __init__(self, w, h):
#         self.w, self.h = w, h
#         self.offset = 0
#     def draw(self, surf, dt=0.016):
#         self.offset = (self.offset + 20 * dt) % 50
#         for x in range(-50, self.w + 50, 50):
#             pygame.draw.line(surf, (30, 30, 60), (x, 0), (x, self.h))
#         for y in range(int(-50 + self.offset), self.h + 50, 50):
#             pygame.draw.line(surf, (30, 30, 60), (0, y), (self.w, y))

# graphics.py
import pygame
import random
import math

from config import BG_SECONDARY, GRID_COLOR, BG_PRIMARY
import config as cfg

class Particle:
    def __init__(self, x, y, color, speed=4, life=1.0, size=4):
        self.x, self.y = x, y
        self.color = color
        angle = random.uniform(0, math.pi * 2)
        self.vx = math.cos(angle) * speed * random.uniform(0.5, 1.5)
        self.vy = math.sin(angle) * speed * random.uniform(0.5, 1.5)
        self.life, self.max_life = life, life
        self.size = size
        self.decay = random.uniform(0.8, 1.2)

    def update(self, dt):
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vy += 150 * dt  # gravity
        self.life -= dt * self.decay

    def draw(self, surf):
        if self.life <= 0: return
        alpha = int(255 * (self.life / self.max_life))
        sz = max(1, int(self.size * (self.life / self.max_life)))
        # Glow effect
        for r in range(sz, sz+3):
            a = alpha * (1 - r/sz/3)
            pygame.draw.circle(surf, (*self.color[:3], a), (int(self.x), int(self.y)), r)

class Background:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.offset = 0
        # Generate subtle gradient surface
        self.grad = pygame.Surface((w, h))
        for y in range(h):
            ratio = y / h
            r = int(BG_PRIMARY[0] * (1-ratio) + BG_SECONDARY[0] * ratio)
            g = int(BG_PRIMARY[1] * (1-ratio) + BG_SECONDARY[1] * ratio)
            b = int(BG_PRIMARY[2] * (1-ratio) + BG_SECONDARY[2] * ratio)
            pygame.draw.line(self.grad, (r, g, b), (0, y), (w, y))

    def draw(self, surf, dt=0.016):
        surf.blit(self.grad, (0, 0))
        self.offset = (self.offset + 25 * dt) % 60
        # Professional grid overlay
        for x in range(-60, self.w + 60, 60):
            pygame.draw.line(surf, GRID_COLOR, (x, 0), (x, self.h), 1)
        for y in range(int(-60 + self.offset), self.h + 60, 60):
            pygame.draw.line(surf, GRID_COLOR, (0, y), (self.w, y), 1)

class LobbyEffect:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.elements = []
        self.colors = [cfg.ACCENT_BLUE, cfg.ACCENT_PINK, cfg.ACCENT_PURPLE, cfg.ACCENT_GREEN, cfg.ACCENT_YELLOW]
        self.orbs = {}
        for c in self.colors:
            for sz in range(2, 12):
                surf = pygame.Surface((sz*4, sz*4), pygame.SRCALPHA)
                for r in range(sz*2, 0, -1):
                    a = max(0, int(100 * (1 - r/(sz*2))))
                    pygame.draw.circle(surf, (*c[:3], a), (sz*2, sz*2), r)
                pygame.draw.circle(surf, (*c[:3], 255), (sz*2, sz*2), max(1, sz//2))
                self.orbs[(c, sz)] = surf

    def update_and_draw(self, surf, dt):
        if random.random() < 0.2:
            size = random.randint(3, 10)
            x = random.uniform(0, self.w)
            y = self.h + size*4 + 10
            color = random.choice(self.colors)
            vx = random.uniform(-20, 20)
            vy = random.uniform(-30, -90)
            life = random.uniform(8.0, 18.0)
            self.elements.append({"x": x, "y": y, "vx": vx, "vy": vy, "color": color, "size": size, "life": life, "max_life": life})
            
        for e in self.elements[:]:
            e["x"] += e["vx"] * dt
            e["y"] += e["vy"] * dt
            
            # Subtle floating motion
            e["vx"] += math.sin(e["life"] * 2) * 15 * dt
            
            e["life"] -= dt
            if e["life"] <= 0 or e["y"] < -50:
                self.elements.remove(e)
            else:
                alpha = int(255 * (e["life"] / e["max_life"]))
                fade_in = e["max_life"] - e["life"]
                if fade_in < 1.0:
                    alpha = int(alpha * fade_in)
                
                orb = self.orbs[(e["color"], e["size"])]
                if alpha < 255:
                    tmp = orb.copy()
                    tmp.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                    surf.blit(tmp, (int(e["x"]) - e["size"]*2, int(e["y"]) - e["size"]*2))
                else:
                    surf.blit(orb, (int(e["x"]) - e["size"]*2, int(e["y"]) - e["size"]*2))