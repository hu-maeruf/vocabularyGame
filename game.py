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
        print("Correct!" if self.correct else "Incorrect!")
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
    words = [d["name"] for d in data]
    # Build a dict mapping each word to its hint (None if no hint)
    hints = {d["name"]: d.get("hint") for d in data }
    return words, hints

#
def play_intro_phase(user_input, difficulty):
    round_number = 0
    current_difficulty = difficulty
    session_words, hint_dict = get_words_list(user_input, current_difficulty)
    seen_words = []
    random.shuffle(session_words)
    game_state = create_state(session_words)
    index = 0

    while len(seen_words) != len(session_words):
        # No two words in a round will be the same
        current_word = session_words[index]
        seen_words.append(current_word)
        round_number += 1
        index += 1
        print(f"****Round {round_number}****")
        is_correct = play_round(current_word, session_words)
        update_game_state(is_correct, game_state, current_word, hint_dict)

        if round_number == 5:
            show_status(game_state)
            round_number = 0

# Plays a single round of the game
def play_round(current_word, session_words):
    question = Question(current_word, session_words)
    question.get_user_answer()
    is_correct = question.check_answer()
    return is_correct

# Updates the streak based on the result of the round
def update_game_state(is_correct, game_state, current_word, hint_dict):
    game_state["attempt"][current_word] += 1

    mastered = game_state["mastered_words"]
    pending = game_state["pending_words"]
    wrong= game_state["wrong_words"]
    streak = game_state["streak"]

    if is_correct:
        game_state["score"] += 1
        streak[current_word] += 1
        if streak[current_word] >= 2:
                mastered.add(current_word)
                pending.discard(current_word)
                wrong.discard(current_word)
        else:
            pending.add(current_word)
            wrong.discard(current_word)
    else:
        hint = get_hint(current_word, hint_dict)
        print(f"Hint: {hint}")
        if current_word not in game_state["mastered_words"]:
            streak[current_word] = 0
            pending.discard(current_word)
            wrong.add(current_word)

def create_state(words):
    state = {
        "wrong_words": set(),
        "pending_words": set(),
        "mastered_words": set(),
        "streak": {},
        "attempt": {},
        "score": 0,
    }

    for word in words:
        state["streak"][word] = 0
        state["attempt"][word] = 0

    return state

def show_status(game_state):
    mastered_words = "\n".join(game_state["mastered_words"])
    wrong_words = ", ".join(game_state["wrong_words"])
    print(f"Mastered words: {mastered_words}")
    print(f"Wrong words: {wrong_words}")

# Returns the hint for the given word
def get_hint(word, hint_dict):
    return hint_dict[word]