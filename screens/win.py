import pygame
from components.button import Button

def init(screen, score):
    graphics = {}

    try:
        bg_img = pygame.image.load("assets/images/win/win_bg.png").convert()
        graphics["bg"] = pygame.transform.smoothscale(bg_img, (screen.get_width(), screen.get_height()))
    except Exception as e:
        print(f"Error loading win screen background: {e}")
        graphics["bg"] = None

    font_small = pygame.font.SysFont("Arial", 40, bold=True)
    score_text = font_small.render(f"Score: {score}", True, (20, 35, 90))
    score_rect = score_text.get_rect(center=(screen.get_width() // 2, 430))

    play_again_btn = Button((365, 570), (240, 70), (76, 175, 80), border_radius=35)

    back_btn = Button((665, 570), (240, 70), (142, 115, 219), border_radius=35)

    return graphics, score_text, score_rect, play_again_btn, back_btn

def draw(screen, graphics, score_text, score_rect, play_again_btn, back_btn):
    if graphics["bg"]:
        screen.blit(graphics["bg"], (0, 0))
    else:
        screen.fill((185, 226, 245))
    screen.blit(score_text, score_rect)
    play_again_btn.draw(screen)
    pygame.draw.rect(screen, (50, 120, 50), play_again_btn.rect, width=4, border_radius=35)

    btn_font = pygame.font.SysFont("Arial", 30, bold=True)
    play_text = btn_font.render("Play Again", True, (255, 255, 255))
    play_rect = play_text.get_rect(center=play_again_btn.rect.center)
    screen.blit(play_text, play_rect)

    back_btn.draw(screen)
    pygame.draw.rect(screen, (90, 70, 150), back_btn.rect, width=4, border_radius=35)

    back_text = btn_font.render("Quit Game", True, (255, 255, 255))
    back_rect = back_text.get_rect(center=back_btn.rect.center)
    screen.blit(back_text, back_rect)

def handle_events(event, play_again_btn, back_btn):
    if play_again_btn.is_clicked(event):
        return "play_again"
    if back_btn.is_clicked(event):
        return "category"
    return None