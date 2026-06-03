from words import init_animals, init_fruits_veg, init_colors
from game import play_intro_phase, play_mastery_phase, intro_phase_diff

CATEGORY_ANIMALS = "a"
CATEGORY_FRUITS_VEG = "b"
CATEGORY_COLORS = "c"
CATEGORY_MIXED = "d"

DIFFICULTY_EASY = "easy"
DIFFICULTY_DIFFICULT = "diff"

def main():
    while True:
        user_input = choose_category()
        difficulty = DIFFICULTY_EASY
        while True:
            session_words, hint_dict = get_words_list(user_input, difficulty)
            game_state = play_intro_phase(session_words, hint_dict)
            total_words = len(session_words)
            threshold = 0

            while threshold < 75:
                game_state = play_mastery_phase(game_state, session_words, hint_dict)
                mastered_words = len(game_state["mastered_words"])
                threshold = (mastered_words / total_words) * 100

            if difficulty == DIFFICULTY_EASY:
                difficulty = DIFFICULTY_DIFFICULT
                session_words, hint_diff = get_words_list(user_input, difficulty)
                game_state = intro_phase_diff(hint_dict, game_state, session_words, hint_diff)
                total_words = len(session_words)
                threshold = 0

                while threshold < 100:
                    hint_dict.update(hint_diff)
                    game_state = play_mastery_phase(game_state, session_words, hint_dict)
                    mastered_words = len(game_state["mastered_words"])
                    threshold = (mastered_words / total_words) * 100

            else:
                break
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != "y":
            break


def play_game(user_input, difficulty):
    session_words, hint_dict = get_words_list(user_input, difficulty)
    game_state = play_intro_phase(session_words, hint_dict)
    return play_mastery_phase(game_state, session_words, hint_dict)

# Choose a category/world
def choose_category():
    while True:
        chosen_world = input(
            "**** Choose a world!! *****\n\tType 'A' for Animal\n\tType 'B' for Fruit & Vegetable\n\tType 'C' for Color\n\tType 'D' for Mixed\n\nInput: ").strip().lower()
        if chosen_world in [CATEGORY_ANIMALS, CATEGORY_FRUITS_VEG, CATEGORY_COLORS, CATEGORY_MIXED]:
            return chosen_world
        else:
            print("Invalid input. Please try again.")

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