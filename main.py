import pygame
import screens.home as home
from words import init_animals, init_fruits_veg, init_colors
from game import play_intro_phase, play_mastery_phase, intro_phase_diff

CATEGORY_ANIMALS = "animals"
CATEGORY_FRUITS_VEG = "fruits_veg"
CATEGORY_COLORS = "colors"
CATEGORY_MIXED = "mixed"

DIFFICULTY_EASY = "easy"
DIFFICULTY_DIFFICULT = "diff"

pygame.init()

def main():
    screen = pygame.display.set_mode((800, 600))
    button_rec, text_surface, text_rect = home.init()
    pygame.display.set_caption("Vocabulary Adventure")
    running = True
    state = "home"
    while running:
        screen.fill((185, 226, 245))
        if state == "home":
            home.draw(screen, button_rec, text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == "home":
                state = home.handle_events(event, state, button_rec)
            elif state == "category":
                pass
            elif state == "question":
                pass
            elif state == "win":
                pass

        pygame.display.update()

if __name__ == "__main__":
    main()