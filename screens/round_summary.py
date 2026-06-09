import pygame
from components.button import Button

def init(screen):
    continue_btn = Button(
        screen.get_rect().center,
        (200, 70), (0, 200, 0), "Continue", 35
    )
    font = pygame.font.SysFont("Arial", 50)
    text_surface = font.render("You finished this round!", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (screen.get_width() // 2, 200)
    return continue_btn, text_surface, text_rect

def draw(screen, continue_btn, text_surface, text_rect):
    screen.blit(text_surface, text_rect)
    continue_btn.draw(screen)

def handle_events(event, continue_btn):
    if continue_btn.is_clicked(event):
        return "question"
    return None