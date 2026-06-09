import pygame
from components.button import Button


def init(screen, score):
    font_big = pygame.font.SysFont("Arial", 60)
    font_small = pygame.font.SysFont("Arial", 35)

    title = font_big.render("You Win!", True, (255, 215, 0))
    title_rect = title.get_rect(center=(screen.get_width() // 2, 150))

    score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(screen.get_width() // 2, 250))

    play_again_btn = Button((400, 400), (200, 70), (0, 200, 0), "Play Again", 30)
    back_btn = Button((800, 400), (200, 70), (0, 100, 200), "Back to Worlds", 30)

    return title, title_rect, score_text, score_rect, play_again_btn, back_btn


def draw(screen, title, title_rect, score_text, score_rect, play_again_btn, back_btn):
    screen.blit(title, title_rect)
    screen.blit(score_text, score_rect)
    play_again_btn.draw(screen)
    back_btn.draw(screen)


def handle_events(event, play_again_btn, back_btn):
    if play_again_btn.is_clicked(event):
        return "play_again"
    if back_btn.is_clicked(event):
        return "category"
    return None