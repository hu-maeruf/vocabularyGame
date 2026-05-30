import random
from words import init_animals, init_fruits_veg, init_colors

CATEGORY_ANIMALS = "a"
CATEGORY_FRUITS_VEG = "b"
CATEGORY_COLORS = "c"
CATEGORY_MIXED = "d"

DIFFICULTY_EASY = "easy"
DIFFICULTY_DIFFICULT = "diff"

class Question:
    def __init__(self, word):
        self.word = word
        self.answer = None

    def get_user_answer(self):
        self.answer = input(f"What is this {self.word}?\nAnswer: ").strip().lower()

    def display(self):
        if self.check_answer():
            print("Correct!")
        else:
            print("Incorrect!")

    def check_answer(self):
        return self.answer == self.word.lower()

# Choose a category/world
def choose_category():
    while True:
        chosen_world = input(
            "**** Choose a world!! *****\n\tType 'A' for Animal\n\tType 'B' for Fruit & Vegetable\n\tType 'C' for Color\n\tType 'D' for Mixed\n\nInput: ").lower()
        if chosen_world in [CATEGORY_ANIMALS, CATEGORY_FRUITS_VEG, CATEGORY_COLORS, CATEGORY_MIXED]:
            return chosen_world
        else:
            print("Invalid input. Please try again.")

# Get words by category and difficulty
def get_words_list(chosen_letter, difficulty):
    if chosen_letter == CATEGORY_ANIMALS:
        words = init_animals[difficulty].copy()
    elif chosen_letter == CATEGORY_FRUITS_VEG:
        words = init_fruits_veg[difficulty].copy()
    elif chosen_letter == CATEGORY_COLORS:
        words = init_colors[difficulty].copy()
    else:
        words = init_animals[difficulty].copy() + init_fruits_veg[difficulty].copy() + init_colors[difficulty].copy()
    return words

# Create a list of words for one game session
def create_session_words(user_input, previous_score):
    # Shuffled list of words
    if previous_score >= 4:
        session_words = get_words_list(user_input, DIFFICULTY_DIFFICULT)

    elif previous_score == 3:
        easy_words = get_words_list(user_input, DIFFICULTY_EASY)
        diff_words = get_words_list(user_input, DIFFICULTY_DIFFICULT)
        session_words = random.sample(easy_words,2) + random.sample(diff_words,3)

    else:
        session_words = get_words_list(user_input, DIFFICULTY_EASY)

    random.shuffle(session_words)
    return session_words

# Play 5 rounds in one game session
def play_game_session(previous_score, user_input):
    round_number = 0
    score = 0
    session_words = create_session_words(user_input, previous_score)
    while round_number < 5:
        current_word = session_words[round_number]
        round_number += 1
        print(f"****Round {round_number}****")
        question = Question(current_word)
        question.get_user_answer()
        is_correct = question.check_answer()
        question.display()
        if is_correct:
            score += 1
    print(f"Final score: {score}/5")
    return score