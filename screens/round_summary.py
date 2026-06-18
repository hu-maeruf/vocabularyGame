import pygame
from components.button import Button
from screens.question import StarTracker

def init(screen, round_score):
    card_height = 550
    card_top = (screen.get_height() - card_height) // 2
    card_centerx = screen.get_width() // 2

    btn_size = (300, 70)
    btn_pos = (card_centerx - btn_size[0] // 2, card_top + 450)
    continue_btn = Button(btn_pos, btn_size, (76, 175, 80), border_radius=30)
    graphics = {"score": round_score}

    try:
        graphics["level"] = pygame.transform.smoothscale(
            pygame.image.load("assets/images/round_summary/level.png").convert_alpha(), (400, 170))
        graphics["completed"] = pygame.transform.smoothscale(
            pygame.image.load("assets/images/round_summary/completed.png").convert_alpha(), (400, 170))
        graphics["trophy"] = pygame.transform.smoothscale(pygame.image.load("assets/images/round_summary/trophy.png").convert_alpha(), (250, 250))
    except Exception as e:
        print(f"Loading Error: {e}")

    star_tracker = StarTracker("assets/images/question/star.png", "assets/images/question/image.png",screen.get_width(), y_pos=card_top + 380)
    return continue_btn, graphics, star_tracker

def draw(screen, bg_img_dict, continue_btn, graphics, star_tracker):
    screen.blit(bg_img_dict["img"], bg_img_dict["rect"])
    card_rect = pygame.Rect(0, 0, 800, 550)
    card_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    pygame.draw.rect(screen, (255, 255, 255), card_rect, border_radius=40)
    pygame.draw.rect(screen, (145, 185, 235), card_rect, width=8, border_radius=40)
    screen.blit(graphics["level"], graphics["level"].get_rect(center=(card_rect.centerx, card_rect.top + 70)))
    screen.blit(graphics["completed"], graphics["completed"].get_rect(center=(card_rect.centerx, card_rect.top + 120)))
    screen.blit(graphics["trophy"], graphics["trophy"].get_rect(center=(card_rect.centerx, card_rect.top + 250)))
    star_tracker.draw(screen, graphics["score"])

    continue_btn.draw(screen)
    font = pygame.font.SysFont("Arial", 30, bold=True)
    text = font.render("Continue", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=continue_btn.rect.center))

def handle_events(event, continue_btn):
    if continue_btn.is_clicked(event):
        return "question"
    return None