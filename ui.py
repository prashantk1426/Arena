# # # ui.py
# # import pygame
# # import config as cfg

# # class Button:
# #     def __init__(self, text, x, y, w, h, color, callback=None, font=None):
# #         self.rect = pygame.Rect(x, y, w, h)
# #         self.text = text
# #         self.color = color
# #         self.callback = callback
# #         self.font = font or pygame.font.SysFont('arial', 32)
# #         self.hover = False
    
# #     def draw(self, surf):
# #         col = tuple(min(c + 40, 255) for c in self.color) if self.hover else self.color
# #         pygame.draw.rect(surf, col, self.rect, border_radius=12)
# #         pygame.draw.rect(surf, cfg.WHITE, self.rect, 2, border_radius=12)
# #         txt = self.font.render(self.text, True, (0,0,0))
# #         surf.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))
    
# #     def update(self, pos):
# #         self.hover = self.rect.collidepoint(pos)
    
# #     def click(self, pos):
# #         if self.hover and self.callback:
# #             self.callback()

# # class HUD:
# #     def __init__(self, font_l, font_m, font_s):
# #         self.fl = font_l
# #         self.fm = font_m
# #         self.fs = font_s
    
# #     def draw(self, surf, score, time_left, extra=""):
# #         surf.blit(self.fs.render(f"SCORE: {score}", True, cfg.WHITE), (20, 20))
# #         tc = cfg.NEON_RED if time_left < 10 else cfg.NEON_YELLOW
# #         surf.blit(self.fm.render(f"TIME: {int(time_left)}s", True, tc), (surf.get_width()//2 - 70, 15))
# #         if extra:
# #             surf.blit(self.fs.render(extra, True, cfg.NEON_GREEN), (surf.get_width() - 250, 20))

# # ui.py
# import pygame
# import config as cfg


# class Button:
#     def __init__(self, text, x, y, w, h, color, callback=None, font=None):
#         self.rect = pygame.Rect(x, y, w, h)
#         self.text = text
#         self.base_color = color
#         self.callback = callback
#         self.font = font or pygame.font.SysFont('arial', 32, bold=True)
#         self.hover = False
#         self.pressed = False

#     def draw(self, surf):
#         col = self.base_color
#         if self.pressed: col = tuple(max(c-40, 0) for c in col)
#         elif self.hover: col = tuple(min(c+30, 255) for c in col)
        
#         # Glow shadow
#         shadow_rect = self.rect.copy()
#         shadow_rect.y += 4
#         pygame.draw.rect(surf, (0,0,0,80), shadow_rect, border_radius=12)
        
#         # Main button
#         pygame.draw.rect(surf, col, self.rect, border_radius=12)
#         pygame.draw.rect(surf, cfg.WHITE, self.rect, 2, border_radius=12)
        
#         txt = self.font.render(self.text, True, BLACK := (10,10,15))
#         surf.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

#     def update(self, pos, events):
#         self.hover = self.rect.collidepoint(pos)
#         self.pressed = any(e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos) for e in events)
#         if self.pressed and self.callback:
#             self.callback()

# class HUD:
#     def __init__(self, font_l, font_m, font_s):
#         self.fl, self.fm, self.fs = font_l, font_m, font_s

#     def draw(self, surf, score, lives, extra="", is_timeless=False, time_left=0):
#         # Score
#         surf.blit(self.fs.render(f"SCORE: {score}", True, cfg.TEXT_PRIMARY), (40, 40))
        
#         # Lives (Hearts)
#         for i in range(3):
#             col = cfg.ACCENT_RED if i < lives else (60, 60, 70)
#             pygame.draw.circle(surf, col, (surf.get_width() - 60 - i*40, 50), 14)
#             pygame.draw.circle(surf, cfg.WHITE, (surf.get_width() - 60 - i*40, 50), 14, 2)
            
#         # Timer or Game Mode
#         if not is_timeless:
#             tc = cfg.ACCENT_RED if time_left < 10 else cfg.ACCENT_YELLOW
#             surf.blit(self.fm.render(f"TIME: {int(time_left)}s", True, tc), (surf.get_width()//2 - 70, 30))
#         else:
#             surf.blit(self.fm.render("TIMELESS", True, cfg.ACCENT_GREEN), (surf.get_width()//2 - 80, 30))
            
#         if extra:
#             surf.blit(self.fs.render(extra, True, cfg.ACCENT_ORANGE), (surf.get_width() - 280, 90))

# class ModalInput:
#     def __init__(self, prompt, options=None):
#         self.prompt = prompt
#         self.options = options
#         self.input_text = ""
#         self.selected_idx = 0
#         self.active = True

#     def draw(self, surf, font_l, font_m, font_s):
#         overlay = pygame.Surface(surf.get_size())
#         overlay.fill((0,0,0))
#         overlay.set_alpha(200)
#         surf.blit(overlay, (0,0))
        
#         title = font_m.render(self.prompt, True, cfg.ACCENT_YELLOW)
#         surf.blit(title, (surf.get_width()//2 - title.get_width()//2, 200))
        
#         if self.options:
#             for i, opt in enumerate(self.options):
#                 col = cfg.ACCENT_GREEN if i == self.selected_idx else cfg.TEXT_SECONDARY
#                 bg = (30, 40, 70) if i == self.selected_idx else (20, 25, 45)
#                 rect = pygame.Rect(surf.get_width()//2 - 200, 280 + i*70, 400, 55)
#                 pygame.draw.rect(surf, bg, rect, border_radius=10)
#                 pygame.draw.rect(surf, col, rect, 2 if i==self.selected_idx else 1, border_radius=10)
#                 txt = font_m.render(opt, True, col)
#                 surf.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
#         else:
#             box = pygame.Rect(surf.get_width()//2 - 250, 280, 500, 65)
#             pygame.draw.rect(surf, (20, 25, 45), box, border_radius=12)
#             pygame.draw.rect(surf, cfg.ACCENT_GREEN, box, 3, border_radius=12)
#             cursor = "_" if pygame.time.get_ticks() % 1000 < 500 else ""
#             txt = font_m.render(self.input_text + cursor, True, cfg.TEXT_PRIMARY)
#             surf.blit(txt, (box.x + 20, box.y + 15))
            
#         hint = font_s.render("ENTER to confirm | ESC to cancel", True, cfg.TEXT_SECONDARY)
#         surf.blit(hint, (surf.get_width()//2 - hint.get_width()//2, 400))

# ui.py
import pygame
import config as cfg

def get_font(size, bold=False):
    """Robust font loader with fallback."""
    # Try preferred fonts
    preferred = ['arial', 'segoe ui', 'roboto', 'helvetica', 'verdana']
    for font_name in preferred:
        try:
            return pygame.font.SysFont(font_name, size, bold=bold)
        except:
            continue
    # Fallback to default
    return pygame.font.SysFont(None, size, bold=bold)

class Button:
    def __init__(self, text, x, y, w, h, color, callback=None, font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = color
        self.callback = callback
        self.font = font or get_font(32, bold=True)
        self.hover = False
        self.pressed = False

    def draw(self, surf):
        col = self.base_color
        if self.pressed: col = tuple(max(c-40, 0) for c in col)
        elif self.hover: col = tuple(min(c+30, 255) for c in col)
        
        # Glow shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(surf, (0,0,0,80), shadow_rect, border_radius=12)
        
        # Main button
        pygame.draw.rect(surf, col, self.rect, border_radius=12)
        pygame.draw.rect(surf, cfg.WHITE, self.rect, 2, border_radius=12)
        
        txt = self.font.render(self.text, True, (10,10,15))
        surf.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

    def update(self, pos, events):
        self.hover = self.rect.collidepoint(pos)
        self.pressed = any(e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos) for e in events)
        if self.pressed and self.callback:
            self.callback()

class HUD:
    def __init__(self, font_l, font_m, font_s):
        self.fl, self.fm, self.fs = font_l, font_m, font_s

    def draw(self, surf, score, lives, extra="", is_timeless=False, time_left=0):
        # Score
        surf.blit(self.fs.render(f"SCORE: {score}", True, cfg.TEXT_PRIMARY), (40, 40))
        
        # Lives (Hearts)
        for i in range(3):
            col = cfg.ACCENT_RED if i < lives else (60, 60, 70)
            pygame.draw.circle(surf, col, (surf.get_width() - 60 - i*40, 50), 14)
            pygame.draw.circle(surf, cfg.WHITE, (surf.get_width() - 60 - i*40, 50), 14, 2)
            
        # Timer or Game Mode
        if not is_timeless:
            tc = cfg.ACCENT_RED if time_left < 10 else cfg.ACCENT_YELLOW
            surf.blit(self.fm.render(f"TIME: {int(time_left)}s", True, tc), (surf.get_width()//2 - 70, 30))
        else:
            surf.blit(self.fm.render("TIMELESS", True, cfg.ACCENT_GREEN), (surf.get_width()//2 - 80, 30))
            
        if extra:
            surf.blit(self.fs.render(extra, True, cfg.ACCENT_ORANGE), (surf.get_width() - 280, 90))

class ModalInput:
    def __init__(self, prompt, options=None):
        self.prompt = prompt
        self.options = options
        self.input_text = ""
        self.selected_idx = 0
        self.active = True

    def draw(self, surf, font_l, font_m, font_s):
        overlay = pygame.Surface(surf.get_size())
        overlay.fill((0,0,0))
        overlay.set_alpha(200)
        surf.blit(overlay, (0,0))
        
        title = font_m.render(self.prompt, True, cfg.ACCENT_YELLOW)
        surf.blit(title, (surf.get_width()//2 - title.get_width()//2, 200))
        
        if self.options:
            for i, opt in enumerate(self.options):
                col = cfg.ACCENT_GREEN if i == self.selected_idx else cfg.TEXT_SECONDARY
                bg = (30, 40, 70) if i == self.selected_idx else (20, 25, 45)
                rect = pygame.Rect(surf.get_width()//2 - 200, 280 + i*70, 400, 55)
                pygame.draw.rect(surf, bg, rect, border_radius=10)
                pygame.draw.rect(surf, col, rect, 2 if i==self.selected_idx else 1, border_radius=10)
                txt = font_m.render(opt, True, col)
                surf.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
        else:
            box = pygame.Rect(surf.get_width()//2 - 250, 280, 500, 65)
            pygame.draw.rect(surf, (20, 25, 45), box, border_radius=12)
            pygame.draw.rect(surf, cfg.ACCENT_GREEN, box, 3, border_radius=12)
            cursor = "_" if pygame.time.get_ticks() % 1000 < 500 else ""
            txt = font_m.render(self.input_text + cursor, True, cfg.TEXT_PRIMARY)
            surf.blit(txt, (box.x + 20, box.y + 15))
            
        hint = font_s.render("ENTER to confirm | ESC to cancel", True, cfg.TEXT_SECONDARY)
        
        # Calculate safe Y position based on whether it's options or text input
        if self.options:
            hint_y = 280 + len(self.options) * 70 + 20
        else:
            hint_y = 400
            
        surf.blit(hint, (surf.get_width()//2 - hint.get_width()//2, hint_y))

    def update(self, pos, events):
        """Update modal state based on mouse position and clicks."""
        if self.options:
            for i, opt in enumerate(self.options):
                rect = pygame.Rect(cfg.SCREEN_WIDTH//2 - 200, 280 + i*70, 400, 55)
                if rect.collidepoint(pos):
                    self.selected_idx = i
                    if any(e.type == pygame.MOUSEBUTTONDOWN for e in events):
                        # Return True to signal that an option was selected via click
                        return True
        return False