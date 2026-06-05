import pygame
import screens.home as home
import screens.category as cat
from words import init_animals, init_fruits_veg, init_colors
from game import create_state

CATEGORY_ANIMALS = "animals"
CATEGORY_FRUITS_VEG = "food"
CATEGORY_COLORS = "colors"
CATEGORY_MIXED = "mixed"

DIFFICULTY_EASY = "easy"
DIFFICULTY_DIFFICULT = "diff"

pygame.init()

def main():
    screen = pygame.display.set_mode((1200, 600))
    home_btn = home.init(screen)
    cat_btn = cat.init()
    pygame.display.set_caption("Vocabulary Adventure")
    running = True
    state = "home"
    selected = None
    session_words = None
    hint_dict = None
    game_state = None
    while running:
        screen.fill((185, 226, 245))
        if state == "home":
            home.draw(home_btn, screen)
        elif state == "category":
            cat.draw(cat_btn, screen)
        elif state == "question":
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == "home":
                if home_btn.is_clicked(event):
                    state = "category"
            elif state == "category":
                selected = cat.handle_events(cat_btn, event)
                if selected:
                    state = "question"
                    session_words, hint_dict = get_words_list(selected, DIFFICULTY_EASY)
                    game_state = create_state(session_words)
            elif state == "question":
                pass
            elif state == "win":
                pass

        pygame.display.update()

def get_words_list(chosen_letter, difficulty):
    if chosen_letter == CATEGORY_ANIMALS:
        data = init_animals[difficulty]
    elif chosen_letter == CATEGORY_FRUITS_VEG:
        data = init_fruits_veg[difficulty]
    elif chosen_letter == CATEGORY_COLORS:
        data = init_colors[difficulty]
    else:
        data = init_animals[difficulty] + init_fruits_veg[difficulty] + init_colors[difficulty]

    # Build a list of word strings from the list of dicts
    words = [d["name"] for d in data]
    # Build a dict mapping each word to its hint (None if no hint)
    hints = {d["name"]: d.get("hint") for d in data }

    return words, hints

if __name__ == "__main__":
    main()