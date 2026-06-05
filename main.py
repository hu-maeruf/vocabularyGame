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
    screen = pygame.display.set_mode((1200, 600))
    home_btn = home.init(screen)
    pygame.display.set_caption("Vocabulary Adventure")
    running = True
    state = "home"
    while running:
        screen.fill((185, 226, 245))
        if state == "home":
            home.draw(home_btn, screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == "home":
                if home_btn.is_clicked(event):
                    state = "category"
            elif state == "category":
                pass
            elif state == "question":
                pass
            elif state == "win":
                pass

        pygame.display.update()

if __name__ == "__main__":
    main()