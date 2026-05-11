# # game_reaction.py
# import pygame
# import random
# import config as cfg
# from graphics import Particle

# class ReactionGame:
#     def __init__(self, audio, hud, particles):
#         self.audio, self.hud, self.particles = audio, hud, particles
#         self.reset()
    
#     def reset(self):
#         self.score, self.time_left, self.combo = 0, 60.0, 0
#         self.running, self.spawn_timer = True, 0
#         self.target_color = cfg.NEON_BLUE
#         self.colors = [cfg.NEON_BLUE, cfg.NEON_PINK, cfg.NEON_GREEN, cfg.NEON_YELLOW]
#         self.grid = []
#         for r in range(3):
#             for c in range(3):
#                 self.grid.append({'rect': pygame.Rect(300+c*200, 200+r*180, 160, 140), 'col': random.choice(self.colors), 'active': False, 'timer': 0})
#         self.pick_new_target()
    
#     def pick_new_target(self):
#         self.target_color = random.choice(self.colors)
#         for t in self.grid: t['active'] = False
#         for _ in range(random.randint(1,3)):
#             opts = [g for g in self.grid if not g['active'] and g['col']==self.target_color]
#             if opts: t=random.choice(opts); t['active']=True; t['timer']=1.5
    
#     def update(self, dt, keys, clicks=None):
#         if not self.running: return self.score
#         self.time_left -= dt
#         if self.time_left <= 0: self.time_left=0; self.running=False; return self.score
#         self.spawn_timer += dt
#         if self.spawn_timer > 1.2: self.pick_new_target(); self.spawn_timer = 0
#         for t in self.grid:
#             if t['active']:
#                 t['timer'] -= dt
#                 if t['timer'] <= 0: t['active']=False; self.combo=0
#         if clicks:
#             for click in clicks:
#                 for t in self.grid:
#                     if t['rect'].collidepoint(click):
#                         if t['active'] and t['col']==self.target_color:
#                             self.score += 100*(self.combo+1); self.combo+=1
#                             self.audio.play_sfx(600+self.combo*100, 0.15, 0.3)
#                             for _ in range(12): self.particles.append(Particle(t['rect'].centerx, t['rect'].centery, t['col']))
#                             t['active']=False
#                         else: self.combo=0; self.audio.play_sfx(200,0.2,0.4)
#         return self.score
    
#     def draw(self, surf):
#         for t in self.grid:
#             col = t['col'] if not t['active'] else tuple(min(c+60,255) for c in t['col'])
#             pygame.draw.rect(surf, col, t['rect'], border_radius=12)
#             pygame.draw.rect(surf, cfg.WHITE, t['rect'], 3, border_radius=12)
#             if t['active']: pygame.draw.circle(surf, cfg.WHITE, t['rect'].center, 8)
#         pygame.draw.rect(surf, self.target_color, (500, 80, 200, 60), border_radius=10)
#         surf.blit(pygame.font.SysFont('arial', 24).render("MATCH THIS!", True, (0,0,0)), (510, 95))
#         self.hud.draw(surf, self.score, self.time_left, f"COMBO: x{self.combo}")

# game_reaction.py
import pygame
import random
import config as cfg
from graphics import Particle

class ReactionGame:
    def __init__(self, audio, hud, particles):
        self.audio, self.hud, self.particles = audio, hud, particles
        self.reset()
    def reset(self, difficulty="MEDIUM"):
        self.difficulty = difficulty
        cfg_map = cfg.REACTION_CFG[difficulty]
        self.score, self.lives, self.time_left = 0, 3, 60.0
        self.running, self.spawn_timer = True, 0
        self.target_color = cfg.ACCENT_BLUE
        self.colors = [cfg.ACCENT_BLUE, cfg.ACCENT_PINK, cfg.ACCENT_GREEN, cfg.ACCENT_YELLOW]
        self.grid_size = cfg_map["grid"]
        self.time_limit = cfg_map["time_limit"]
        self.score_mult = cfg_map["score_mult"]
        self.grid = []
        self.calculate_grid_positions()
        self.pick_new_target()

    def calculate_grid_positions(self):
        self.grid = []
        cell_w, cell_h = 140, 120
        start_x = (cfg.SCREEN_WIDTH - (self.grid_size * cell_w)) // 2
        start_y = (cfg.SCREEN_HEIGHT - (self.grid_size * cell_h)) // 2
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.grid.append({
                    'rect': pygame.Rect(start_x + c*cell_w, start_y + r*cell_h, cell_w-10, cell_h-10),
                    'col': random.choice(self.colors), 'active': False, 'timer': 0
                })

    def pick_new_target(self):
        self.target_color = random.choice(self.colors)
        for t in self.grid: t['active'] = False
        count = random.randint(1, min(3, self.grid_size))
        for _ in range(count):
            opts = [g for g in self.grid if not g['active'] and g['col']==self.target_color]
            if opts:
                t = random.choice(opts)
                t['active'] = True
                t['timer'] = self.time_limit

    def update(self, dt, keys, clicks=None):
        if not self.running: return self.score, self.lives
        self.time_left -= dt
        if self.time_left <= 0 or self.lives <= 0:
            self.time_left = 0; self.running = False; return self.score, self.lives
        self.spawn_timer += dt
        if self.spawn_timer > self.time_limit + 0.3:
            self.pick_new_target(); self.spawn_timer = 0
        for t in self.grid:
            if t['active']:
                t['timer'] -= dt
                if t['timer'] <= 0:
                    t['active'] = False
        if clicks:
            for click in clicks:
                for t in self.grid:
                    if t['rect'].collidepoint(click):
                        if t['active'] and t['col']==self.target_color:
                            pts = int(100 * self.score_mult)
                            self.score += pts
                            self.audio.play_sfx(600 + self.grid_size*50, 0.15, 0.3)
                            for _ in range(12): self.particles.append(Particle(t['rect'].centerx, t['rect'].centery, t['col']))
                            t['active'] = False
                        else:
                            self.lives -= 1
                            self.audio.play_sfx(250, 0.2, 0.4)
                            for _ in range(8): self.particles.append(Particle(t['rect'].centerx, t['rect'].centery, cfg.ACCENT_RED))
        return self.score, self.lives

    def draw(self, surf):
        for t in self.grid:
            col = t['col'] if not t['active'] else tuple(min(c+60,255) for c in t['col'])
            pygame.draw.rect(surf, col, t['rect'], border_radius=12)
            pygame.draw.rect(surf, cfg.WHITE, t['rect'], 3 if t['active'] else 1, border_radius=12)
            if t['active']: pygame.draw.circle(surf, cfg.WHITE, t['rect'].center, 8)
        pygame.draw.rect(surf, self.target_color, (cfg.SCREEN_WIDTH//2-100, 60, 200, 60), border_radius=10)
        surf.blit(pygame.font.SysFont('arial', 22, bold=True).render("MATCH THIS!", True, (10,10,15)), (cfg.SCREEN_WIDTH//2-80, 75))
        self.hud.draw(surf, self.score, self.lives, f"DIFF: {self.difficulty} | GRID: {self.grid_size}x{self.grid_size}", time_left=self.time_left)