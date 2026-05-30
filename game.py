import random
from words import init_animals, init_fruits_veg, init_colors

def get_user_input():
    while True:
        chosen_world = input(
            "**** Choose a world!! *****\n\tType 'A' for Animal\n\tType 'B' for Fruit & Vegetable\n\tType 'C' for Color\n\tType 'D' for Mixed\n\nInput: ").lower()
        if chosen_world == 'a' or chosen_world == 'b' or chosen_world == 'c' or chosen_world == 'd':
            return chosen_world
        else:
            print("Invalid input. Please try again.")

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

def get_session_list(chosen_letter, state):
    if chosen_letter == 'a':
        session_word = init_animals[state].copy()
    elif chosen_letter == 'b':
        session_word = init_fruits_veg[state].copy()
    elif chosen_letter == 'c':
        session_word = init_colors[state].copy()
    else:
        session_word = init_animals[state].copy() + init_fruits_veg[state].copy() + init_colors[state].copy()
    return session_word

def session_word_list(user_input, previous_score):
    # Shuffled list of words
    if previous_score >= 4:
        session_words = get_session_list(user_input, "diff")

    elif previous_score == 3:
        easy_words = get_session_list(user_input, "easy")
        diff_words = get_session_list(user_input, "diff")
        session_words = random.sample(easy_words,2) + random.sample(diff_words,3)

    else:
        session_words = get_session_list(user_input, "easy")

    random.shuffle(session_words)
    return session_words

def get_score():
    current_round = 0
    score = 0
    user_input = get_user_input()
    session_words = session_word_list(user_input)
    while current_round < 5:
        selected_word = session_words[current_round]
        current_round += 1
        print(f"****Round {current_round}****")
        question = Question(selected_word)
        question.get_user_answer()
        is_correct = question.check_answer()
        question.display()
        if is_correct:
            score += 1

    print(f"Final score: {score}/5")