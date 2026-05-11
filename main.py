
# main.py
import pygame
import sys
import config as cfg
from audio import AudioManager
from graphics import Background, Particle, LobbyEffect
from ui import Button, HUD, ModalInput
from game_collector import ArenaGame
from game_dodge import DodgeGame
from game_reaction import ReactionGame
from leaderboard import Leaderboard

def main():
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE)
    pygame.display.set_caption("ARENA - Professional Arcade Suite")
    clock = pygame.time.Clock()

    fL = pygame.font.SysFont('arial', 72, bold=True)
    fM = pygame.font.SysFont('arial', 44, bold=True)
    fS = pygame.font.SysFont('arial', 30)

    audio = AudioManager()
    bg = Background(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    lobby_fx = LobbyEffect(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    hud = HUD(fL, fM, fS)
    lb = Leaderboard()
    particles = []

    games = {
        'collector': ArenaGame(audio, hud, particles),
        'dodge': DodgeGame(audio, hud, particles),
        'reaction': ReactionGame(audio, hud, particles)
    }

    current_game = None
    game_name = ""
    player_name = ""
    selected_difficulty = "MEDIUM"
    state = 'menu'
    final_score = 0
    is_paused = False
    modal = None
    selected_game_key = None

    pause_resume_btn = Button("RESUME", cfg.SCREEN_WIDTH//2-180, 350, 360, 60, cfg.ACCENT_GREEN, None, fM)
    pause_menu_btn = Button("MAIN MENU", cfg.SCREEN_WIDTH//2-180, 430, 360, 60, cfg.ACCENT_RED, None, fM)

    def go_back():
        nonlocal state, current_game, is_paused, modal
        state = 'menu'
        current_game = None
        is_paused = False
        modal = None
        audio.start_lobby_music()

    def start_game():
        nonlocal state, current_game, is_paused, modal, selected_difficulty
        state = 'playing'
        current_game = games[selected_game_key]
        particles.clear()
        diff = selected_difficulty if selected_game_key != 'dodge' else "MEDIUM"
        current_game.reset(diff)
        is_paused = False
        modal = None

    def prep_start(key, name):
        nonlocal state, selected_game_key, modal
        selected_game_key = key
        state = 'input_name'
        modal = ModalInput("ENTER PLAYER NAME:")
        audio.stop_music()

    menu_btns = [
        Button("COLLECTOR", cfg.SCREEN_WIDTH//2-180, 250, 360, 60, cfg.ACCENT_GREEN, lambda: prep_start('collector', 'COLLECTOR'), fM),
        Button("NEON DODGE", cfg.SCREEN_WIDTH//2-180, 330, 360, 60, cfg.ACCENT_ORANGE, lambda: prep_start('dodge', 'NEON DODGE'), fM),
        Button("REACTION RUSH", cfg.SCREEN_WIDTH//2-180, 410, 360, 60, cfg.ACCENT_PINK, lambda: prep_start('reaction', 'REACTION RUSH'), fM),
        Button("LEADERBOARD", cfg.SCREEN_WIDTH//2-180, 490, 360, 60, cfg.ACCENT_YELLOW, lambda: set_state('leaderboard'), fM),
        Button("QUIT", cfg.SCREEN_WIDTH//2-180, 570, 360, 60, cfg.ACCENT_RED, lambda: [pygame.quit(), sys.exit()], fM)
    ]

    def set_state(s):
        nonlocal state
        state = s

    audio.start_lobby_music()
    running = True

    while running:
        dt = clock.tick(cfg.FPS) / 1000.0
        events = pygame.event.get()
        clicks = [e.pos for e in events if e.type == pygame.MOUSEBUTTONDOWN]
        pos = pygame.mouse.get_pos()

        for ev in events:
            if ev.type == pygame.QUIT: running = False
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                if state == 'playing': is_paused = not is_paused
                elif state in ['gameover', 'leaderboard', 'input_name', 'input_diff']: go_back()

        screen.fill(cfg.BG_PRIMARY)
        bg.draw(screen, dt)

        if state != 'playing':
            lobby_fx.update_and_draw(screen, dt)

        if state == 'menu':
            title = fL.render("ARENA", True, cfg.ACCENT_BLUE)
            screen.blit(title, (cfg.SCREEN_WIDTH//2 - title.get_width()//2, 120))
            sub = fS.render("Professional Interactive Arcade Suite", True, cfg.TEXT_SECONDARY)
            screen.blit(sub, (cfg.SCREEN_WIDTH//2 - sub.get_width()//2, 190))
            for b in menu_btns: b.update(pos, events); b.draw(screen)

        elif state == 'input_name':
            modal.draw(screen, fL, fM, fS)
            for ev in events:
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN and modal.input_text.strip():
                        player_name = modal.input_text.strip()
                        if selected_game_key == 'dodge':
                            start_game()
                        else:
                            state = 'input_diff'
                            modal = ModalInput("SELECT DIFFICULTY:", options=cfg.DIFFICULTIES)
                    elif ev.key == pygame.K_BACKSPACE: modal.input_text = modal.input_text[:-1]
                    elif ev.unicode.isalpha() and len(modal.input_text) < 15: modal.input_text += ev.unicode

        elif state == 'input_diff':
            modal.draw(screen, fL, fM, fS)
            for ev in events:
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN:
                        selected_difficulty = modal.options[modal.selected_idx]
                        start_game()
                    elif ev.key == pygame.K_UP: modal.selected_idx = (modal.selected_idx - 1) % len(modal.options)
                    elif ev.key == pygame.K_DOWN: modal.selected_idx = (modal.selected_idx + 1) % len(modal.options)

        elif state == 'playing' and current_game:
            if not is_paused:
                res = current_game.update(dt, pygame.key.get_pressed(), clicks)
                final_score, lives = res[0], res[1]
                current_game.draw(screen)
                if not current_game.running:
                    state = 'gameover'
                    lb.add(player_name, final_score, game_name, getattr(current_game, 'difficulty', 'N/A'))
                    audio.play_sfx(523, 0.5, 0.4)
            else:
                overlay = pygame.Surface(screen.get_size()); overlay.fill((0,0,0)); overlay.set_alpha(220)
                screen.blit(overlay, (0,0))
                screen.blit(fL.render("PAUSED", True, cfg.ACCENT_YELLOW), (cfg.SCREEN_WIDTH//2-100, 220))
                pause_resume_btn.update(pos, events); pause_resume_btn.draw(screen)
                pause_menu_btn.update(pos, events); pause_menu_btn.draw(screen)
                for c in clicks:
                    if pause_resume_btn.rect.collidepoint(c): is_paused = False
                    if pause_menu_btn.rect.collidepoint(c): go_back()

        elif state == 'gameover':
            # Full dark overlay
            overlay = pygame.Surface(screen.get_size()); overlay.fill(cfg.BG_PRIMARY); overlay.set_alpha(240)
            screen.blit(overlay, (0,0))
            
            # FIXED: Made box TALLER to contain both buttons (height increased from 450 to 550)
            pygame.draw.rect(screen, (20, 25, 45), (cfg.SCREEN_WIDTH//2-250, 100, 500, 550), border_radius=15)
            pygame.draw.rect(screen, cfg.ACCENT_BLUE, (cfg.SCREEN_WIDTH//2-250, 100, 500, 550), 3, border_radius=15)
            
            # Adjusted vertical spacing
            screen.blit(fL.render("GAME OVER", True, cfg.ACCENT_RED), (cfg.SCREEN_WIDTH//2-180, 130))
            screen.blit(fM.render(f"Player: {player_name}", True, cfg.ACCENT_BLUE), (cfg.SCREEN_WIDTH//2-150, 220))
            screen.blit(fL.render(f"SCORE: {final_score}", True, cfg.ACCENT_YELLOW), (cfg.SCREEN_WIDTH//2-150, 290))
            
            # FIXED: Moved buttons DOWN and INSIDE the box
            pause_resume_btn.text = "PLAY AGAIN"
            pause_resume_btn.rect.y = 470  # Moved down significantly
            pause_menu_btn.rect.y = 550    # Moved down significantly
            
            pause_resume_btn.update(pos, events); pause_resume_btn.draw(screen)
            pause_menu_btn.update(pos, events); pause_menu_btn.draw(screen)
            
            for c in clicks:
                if pause_resume_btn.rect.collidepoint(c): start_game(); is_paused=False
                if pause_menu_btn.rect.collidepoint(c): go_back()

        elif state == 'leaderboard':
            # Full background overlay
            overlay = pygame.Surface(screen.get_size()); overlay.fill(cfg.BG_PRIMARY); overlay.set_alpha(240)
            screen.blit(overlay, (0,0))
            
            # Draw container - made it taller
            pygame.draw.rect(screen, (20, 25, 45), (cfg.SCREEN_WIDTH//2-350, 60, 700, 650), border_radius=15)
            pygame.draw.rect(screen, cfg.ACCENT_YELLOW, (cfg.SCREEN_WIDTH//2-350, 60, 700, 650), 3, border_radius=15)
            
            screen.blit(fL.render("LEADERBOARD", True, cfg.ACCENT_YELLOW), (cfg.SCREEN_WIDTH//2-180, 80))
            
            # FIXED: Reduced to top 10 entries and increased spacing
            top = lb.scores[:10]  # Changed from 12 to 10
            for i, e in enumerate(top):
                c = cfg.ACCENT_YELLOW if i==0 else cfg.ACCENT_BLUE if i<3 else cfg.TEXT_PRIMARY
                diff = e.get('diff', 'N/A')
                game = e.get('game', 'UNKNOWN')
                name = e.get('name', 'Player')
                score = e.get('score', 0)
                
                s = fS.render(f"{i+1}. {name} | {score} pts | {game} ({diff})", True, c)
                # Increased vertical spacing from 50 to 55 pixels
                screen.blit(s, (cfg.SCREEN_WIDTH//2 - s.get_width()//2, 150 + i*52))
            
            # FIXED: Moved ESC hint DOWN and made it more visible
            esc_hint = fM.render("Press ESC to go back", True, cfg.ACCENT_GREEN)
            screen.blit(esc_hint, (cfg.SCREEN_WIDTH//2 - esc_hint.get_width()//2, 730))

        for p in particles[:]: p.update(dt); p.draw(screen)
        particles[:] = [p for p in particles if p.life > 0]
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()