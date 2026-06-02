import random

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

    def ask(self):
        self.get_user_answer()
        return self.check_answer()

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

# Introducing all new words for the first time
def play_intro_phase(session_words, hint_dict):
    round_number = 0
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
    return game_state

# Plays the mastery phase of the game
def play_mastery_phase(game_state, session_words, hint_dict):
    total_words = len(session_words)

    wrong = list(game_state["wrong_words"])
    pending = list(game_state["pending_words"])
    mastered = list(game_state["mastered_words"])

    random.shuffle(wrong)
    random.shuffle(pending)
    random.shuffle(mastered)

    # Add the remaining words with wrong first priority, then pending, then mastered, then the rest of the words
    pool = (wrong + pending + mastered + session_words)[:5]

    for round_number, word in enumerate(pool, start=1):
        play_one_round(word, session_words, game_state,hint_dict, round_number)

    show_status(game_state)

    return game_state

# Plays a single round of the game
def play_round(current_word, session_words):
    question = Question(current_word, session_words)
    question.get_user_answer()
    is_correct = question.check_answer()
    return is_correct

def play_one_round(current_word, session_words, game_state, hint_dict, round_number):
    question = Question(current_word, session_words)
    print(f"****Round {round_number}****")
    is_correct = question.ask()
    update_game_state(is_correct, game_state, current_word, hint_dict)

# Updates the streak based on the result of the round
def update_game_state(is_correct, game_state, current_word, hint_dict):

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

# Show wrong and mastered words
def show_status(game_state):
    mastered_words = "\n".join(game_state["mastered_words"])
    wrong_words = ", ".join(game_state["wrong_words"])
    print(f"Mastered words: {mastered_words}" if mastered_words else "No words mastered yet.")
    print(f"Wrong words: {wrong_words}" if wrong_words else "No wrong words yet.")

def create_state(words):
    state = {
        "wrong_words": set(),
        "pending_words": set(),
        "mastered_words": set(),
        "streak": {},
        "score": 0,
    }

    for word in words:
        state["streak"][word] = 0

    return state

# Returns the hint for the given word
def get_hint(word, hint_dict):
    return hint_dict[word]

# Returns the list of wrong words and their hints
def wrong_words_hint(hint_dict, game_state):
    words = list(game_state["wrong_words"])
    hint = {}
    for word in words:
        hint[word] = hint_dict[word]

    return words, hint