# # config.py
# SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
# FPS = 60
# DARK_BG = (10, 10, 30)
# GRID_COLOR = (30, 30, 60)
# WHITE = (255, 255, 255)
# NEON_BLUE = (0, 255, 255)
# NEON_PINK = (255, 0, 255)
# NEON_GREEN = (0, 255, 128)
# NEON_ORANGE = (255, 128, 0)
# NEON_YELLOW = (255, 255, 0)
# NEON_RED = (255, 50, 50)
# NEON_PURPLE = (180, 50, 255)

# config.py
import pygame

# Fullscreen Target Resolution
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
FPS = 60

# Professional Color Palette
BG_PRIMARY = (10, 12, 24)
BG_SECONDARY = (22, 28, 52)
ACCENT_BLUE = (0, 212, 255)
ACCENT_PINK = (255, 40, 180)
ACCENT_GREEN = (0, 255, 130)
ACCENT_ORANGE = (255, 140, 30)
ACCENT_YELLOW = (255, 220, 50)
ACCENT_RED = (255, 60, 60)
ACCENT_PURPLE = (160, 80, 255)
ACCENT_BLACK = (30, 30, 35)
TEXT_PRIMARY = (240, 245, 255)
TEXT_SECONDARY = (160, 175, 200)
GRID_COLOR = (35, 42, 70)
WHITE = (255, 255, 255)

DIFFICULTIES = ["EASY", "MEDIUM", "HARD"]

# Collector Difficulty Config
COLLECTOR_CFG = {
    "EASY": {"obs_count": 3, "obs_speed": 100, "has_bombs": False},
    "MEDIUM": {"obs_count": 5, "obs_speed": 160, "has_bombs": True},
    "HARD": {"obs_count": 8, "obs_speed": 220, "has_bombs": True}
}

# Reaction Rush Difficulty Config
REACTION_CFG = {
    "EASY": {"grid": 3, "time_limit": 1.5, "score_mult": 1},
    "MEDIUM": {"grid": 4, "time_limit": 1.2, "score_mult": 1.5},
    "HARD": {"grid": 5, "time_limit": 0.9, "score_mult": 2}
}