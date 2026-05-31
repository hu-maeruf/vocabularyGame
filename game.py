import random
from words import init_animals, init_fruits_veg, init_colors

CATEGORY_ANIMALS = "a"
CATEGORY_FRUITS_VEG = "b"
CATEGORY_COLORS = "c"
CATEGORY_MIXED = "d"

DIFFICULTY_EASY = "easy"
DIFFICULTY_DIFFICULT = "diff"

class Question:
    def __init__(self, word, word_list):
        self.word = word
        self.word_list = word_list
        self.answer = None

    def create_question(self):
        self.remaining_words = [item for item in self.word_list if item != self.word]
        self.choice_list = random.sample(self.remaining_words, 3)
        self.choice_list.append(self.word)
        random.shuffle(self.choice_list)

        return f"What is this {self.word}?\nA. {self.choice_list[0]}\nB. {self.choice_list[1]}\nC. {self.choice_list[2]}\nD. {self.choice_list[3]}"

    def get_user_answer(self):
        self.question = self.create_question()
        while True:
            self.answer = input(f"{self.question}\n").strip().lower()
            if self.answer in ["a", "b", "c", "d"]:
                break
            print("Invalid input. Please enter A, B, C or D.")

    def check_answer(self):
        index = {"a": 0, "b": 1, "c": 2, "d": 3}
        self.correct = self.choice_list[index[self.answer]] == self.word
        # print("Correct!" if self.correct else "Incorrect!")
        return self.correct

# Choose a category/world
def choose_category():
    while True:
        chosen_world = input(
            "**** Choose a world!! *****\n\tType 'A' for Animal\n\tType 'B' for Fruit & Vegetable\n\tType 'C' for Color\n\tType 'D' for Mixed\n\nInput: ").lower()
        if chosen_world in [CATEGORY_ANIMALS, CATEGORY_FRUITS_VEG, CATEGORY_COLORS, CATEGORY_MIXED]:
            return chosen_world
        else:
            print("Invalid input. Please try again.")

# Returns both word list and hints dictionary for the given category and difficulty
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
    words = [d["word"] for d in data]

    # Build a dict mapping each word to its hint (None if no hint)
    hints = {d["word"]: d.get("hint") for d in data }
    return words, hints

# Create a list of words for one game session
def create_session_words(user_input, previous_score):
    # Shuffled list of words
    if previous_score >= 4:
        session_words, hint = get_words_list(user_input, DIFFICULTY_DIFFICULT)
        print("Session words are from Difficult category.")

    elif previous_score == 3:
        easy_words, hint = get_words_list(user_input, DIFFICULTY_EASY)
        diff_words, hint = get_words_list(user_input, DIFFICULTY_DIFFICULT)
        session_words = random.sample(easy_words,2) + random.sample(diff_words,3)
        print("Session words are mix of Easy and Difficult category.")

    else:
        session_words, hint = get_words_list(user_input, DIFFICULTY_EASY)
        print("Session words are from Easy category.")

    random.shuffle(session_words)
    return session_words, hint

# Play 5 rounds in one game session
def play_game_session(previous_score, user_input):
    round_number = 0
    score = 0
    session_words, hint = create_session_words(user_input, previous_score)
    while round_number < 5:
        current_word = session_words[round_number]
        round_number += 1
        print(f"****Round {round_number}****")
        question = Question(current_word, session_words)
        question.get_user_answer()
        is_correct = question.check_answer()
        if is_correct:
            score += 1
            print("Correct!")
        else:
            hint = get_hint(current_word, hint)
            print(hint)
    print(f"Final score: {score}/5")
    return score

# Returns the hint for the given word
def get_hint(word, hint_dict):
    return hint_dict[word]