import pygame

def init():
    button_rect = pygame.Rect(0, 0, 200, 70)
    button_rect.center = (400, 300)
    text_font = pygame.font.Font("assets/fonts/AtkinsonHyperlegible-Regular.ttf", 50)
    text_surface = text_font.render("Play", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = button_rect.center
    return button_rect, text_surface, text_rect

def draw(screen, button_rect, text, text_rect):
    pygame.draw.rect(screen, (0, 0, 0), button_rect)
    screen.blit(text, text_rect)

def handle_events(event, state, button_rect):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_rect.collidepoint(event.pos):
            print("Button clicked!")
            state = "category"
        else:
            state = "home"
    return state