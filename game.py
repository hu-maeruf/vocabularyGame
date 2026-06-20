import random
from words import init_animals, init_fruits_veg, init_colors

CATEGORY_ANIMALS = "animals"
CATEGORY_FRUITS_VEG = "food"
CATEGORY_COLORS = "colors"
CATEGORY_MIXED = "mixed"

DIFFICULTY_EASY = "easy"
DIFFICULTY_DIFFICULT = "diff"

class Question:
    def __init__(self, word, word_list):
        self.word = word
        self.word_list = word_list

    def create_question(self):
        self.remaining_words = [item for item in self.word_list if item != self.word]
        self.choice_list = random.sample(self.remaining_words, 3)
        self.choice_list.append(self.word)
        random.shuffle(self.choice_list)
        return self.choice_list[0], self.choice_list[1], self.choice_list[2], self.choice_list[3]

class GameSession:
    def __init__(self):
        self.session_words = None
        self.hint_dict = None
        self.game_state = None
        self.current_word = None
        self.current_index = 0
        self.pool = []
        self.pool_index = 0
        self.phase = "intro"
        self.game_over = False
        self.difficulty = "easy"
        self.category = None
        self.round_counter = 0

    def check_answer(self, answer, word):
        return answer == word

    def advance(self, is_correct):
        update_game_state(is_correct, self.game_state, self.current_word, self.hint_dict)
        self.round_counter += 1
        status = self._advance_word()

        if status in ("difficulty_up", "game_over"):
            self.round_counter = 0
            self.game_state["round_score"] = 0
            return status

        if self.round_counter == 5:
            self.round_counter = 0
            return "round_complete"

        return "next_word"

    def _advance_word(self):
        if self.phase == "intro":
            self.current_index += 1
            if self.current_index >= len(self.session_words):
                self.phase = "mastery"
                self.build_pool()
            else:
                self.current_word = self.session_words[self.current_index]
            return "next_word"
        else:
            self.pool_index += 1
            if self.pool_index >= len(self.pool):
                if self.check_threshold():
                    if self.difficulty == DIFFICULTY_EASY:
                        self.difficulty = DIFFICULTY_DIFFICULT
                        self.intro_phase_diff()
                        return "difficulty_up"
                    else:
                        self.game_over = True
                        return "game_over"
                self.build_pool()
                return "next_word"
            else:
                self.current_word = self.pool[self.pool_index]
                return "next_word"

    def build_pool(self):
        wrong = list(self.game_state["wrong_words"])
        pending = list(self.game_state["pending_words"])
        mastered = list(self.game_state["mastered_words"])

        remaining = [w for w in self.session_words if w not in self.game_state["mastered_words"] and w not in self.game_state["wrong_words"] and w not in self.game_state["pending_words"]]

        random.shuffle(wrong)
        random.shuffle(pending)
        random.shuffle(remaining)

        active_pool = wrong + pending + remaining

        if len(active_pool) < 5:
            random.shuffle(mastered)
            active_pool += mastered

        self.pool = active_pool[:5]
        self.pool_index = 0
        if self.pool:
            self.current_word = self.pool[0]

    def check_threshold(self):
        no_mastered = len(self.game_state["mastered_words"])
        total = len(self.session_words)
        if self.difficulty == DIFFICULTY_EASY:
            return ((no_mastered / total) * 100) > 75
        else:
            return no_mastered == total

    def intro_phase_diff(self):
        words, hint = self.wrong_words_hint()
        self.session_words, self.hint_dict = get_words_list(self)
        for word in words:
            if word not in self.session_words:
                self.session_words.append(word)
        self.hint_dict.update(hint)
        self.game_state = create_state(self.session_words)
        for word in self.session_words:
            if word not in self.game_state["streak"]:
                self.game_state["streak"][word] = 0
        self.current_index = 0
        self.current_word = self.session_words[0]
        self.phase = "intro"

    def wrong_words_hint(self):
        words = list(self.game_state["wrong_words"])
        hint = {}
        for word in words:
            hint[word] = self.hint_dict.get(word, f"This is {word}.")
        return words, hint

def play_intro_phase(session):
    session.session_words, session.hint_dict = get_words_list(session)
    random.shuffle(session.session_words)
    session.game_state = create_state(session.session_words)
    session.current_index = 0
    session.current_word = session.session_words[0]
    session.phase = "intro"

def get_words_list(session):
    if session.category == CATEGORY_ANIMALS:
        data = init_animals[session.difficulty]
    elif session.category == CATEGORY_FRUITS_VEG:
        data = init_fruits_veg[session.difficulty]
    elif session.category == CATEGORY_COLORS:
        data = init_colors[session.difficulty]
    else:
        data = init_animals[session.difficulty] + init_fruits_veg[session.difficulty] + init_colors[session.difficulty]
    words = [d["name"] for d in data]
    hints = {d["name"]: d.get("hint") for d in data}
    return words, hints

def update_game_state(is_correct, game_state, current_word, hint_dict):
    mastered = game_state["mastered_words"]
    pending = game_state["pending_words"]
    wrong = game_state["wrong_words"]
    streak = game_state["streak"]

    if is_correct:
        game_state["score"] += 1
        game_state["round_score"] += 1
        streak[current_word] = streak.get(current_word, 0) + 1
        if streak[current_word] >= 2:
            mastered.add(current_word)
            pending.discard(current_word)
            wrong.discard(current_word)
        else:
            pending.add(current_word)
            wrong.discard(current_word)
    else:
        if current_word not in mastered:
            streak[current_word] = 0
            pending.discard(current_word)
            wrong.add(current_word)

def create_state(words):
    return {
        "wrong_words": set(),
        "pending_words": set(),
        "mastered_words": set(),
        "streak": {word: 0 for word in words},
        "score": 0,
        "round_score": 0,
    }

def get_hint(word, hint_dict):
    return hint_dict.get(word, f"This is {word}.")