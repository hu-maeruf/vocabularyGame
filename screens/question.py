import pygame
import math
import sound_manager
from vui_manager import vui
from game import Question
from components.button import Button
from words import init_animals, init_fruits_veg, init_colors

DIFFICULTY_EASY = "easy"
DIFFICULTY_DIFFICULT = "diff"

class QuestionBtn(Button):
    def __init__(self, position, size, color, text, border_radius):
        super().__init__(position, size, color, border_radius)
        self.text = text
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.radius = border_radius

        self.base_color = color
        self.current_color = color

        self.state = "NORMAL"
        self.shake_start_time = 0
        self.bounce_start_time = 0

    def mark_correct(self):
        self.state = "CORRECT"
        self.current_color = (130, 220, 130)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.bounce_start_time = pygame.time.get_ticks()

    def mark_wrong(self):
        self.state = "WRONG"
        self.current_color = (255, 120, 120)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.shake_start_time = pygame.time.get_ticks()

    def draw(self, screen):
        offset_x = 0
        offset_y = 0

        if self.state == "WRONG":
            elapsed_time = pygame.time.get_ticks() - self.shake_start_time
            if elapsed_time < 500:
                offset_x = math.sin(elapsed_time * 0.05) * 6
        elif self.state == "CORRECT":
            elapsed_time = pygame.time.get_ticks() - self.bounce_start_time
            if elapsed_time < 500:
                offset_y = -math.sin(elapsed_time * (math.pi / 500)) * 16

        draw_rect = self.rect.copy()
        draw_rect.x += offset_x
        draw_rect.y += offset_y

        shadow_rect = self.rect.copy()
        shadow_rect.x += offset_x
        shadow_rect.y += 4
        pygame.draw.rect(screen, (100, 100, 100), shadow_rect, border_radius=self.radius)

        pygame.draw.rect(screen, self.current_color, draw_rect, border_radius=self.radius)
        pygame.draw.rect(screen, (145, 185, 235), draw_rect, width=3, border_radius=self.radius)

        text_rect = self.text_surface.get_rect(center=draw_rect.center)
        screen.blit(self.text_surface, text_rect)

class SoundButton:
    def __init__(self, image_path, position=(30, 30), size=(70, 70)):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=(30, 30))
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.text_surface = self.font.render("Hear Sound", True, (255, 255, 255))

        self.text_rect = self.text_surface.get_rect()
        self.text_rect.centerx = self.rect.centerx
        self.text_rect.top = self.rect.bottom + 6

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            hover_img = pygame.transform.scale(self.image, (86, 86))
            hover_rect = hover_img.get_rect(center=self.rect.center)
            screen.blit(hover_img, hover_rect)
        else:
            screen.blit(self.image, self.rect)

        screen.blit(self.text_surface, self.text_rect)

class StarTracker:
    def __init__(self, filled_star_path, empty_star_path, screen_width, y_pos=20):
        self.star_filled = pygame.image.load(filled_star_path).convert_alpha()
        self.star_filled = pygame.transform.scale(self.star_filled, (40, 40))

        self.star_empty = pygame.image.load(empty_star_path).convert_alpha()
        self.star_empty = pygame.transform.scale(self.star_empty, (40, 40))

        self.max_stars = 5
        self.padding_x = 20
        self.padding_y = 10
        self.gap = 15

        self.pill_width = (40 * self.max_stars) + (self.gap * (self.max_stars - 1)) + (self.padding_x * 2)
        self.pill_height = 40 + (self.padding_y * 2)

        self.x = (screen_width - self.pill_width) // 2
        self.y = y_pos

        self.pill_rect = pygame.Rect(self.x, self.y, self.pill_width, self.pill_height)

    def draw(self, screen, current_score):
        pygame.draw.rect(screen, (20, 35, 90), self.pill_rect, border_radius=30)
        pygame.draw.rect(screen, (100, 130, 200), self.pill_rect, width=3, border_radius=30)

        for i in range(self.max_stars):
            star_x = self.x + self.padding_x + i * (40 + self.gap)
            star_y = self.y + self.padding_y

            if i < current_score:
                screen.blit(self.star_filled, (star_x, star_y))
            else:
                screen.blit(self.star_empty, (star_x, star_y))

_ui_state = {
    "current_word_loaded": None,
    "choice_buttons": None,
    "word_img": None,
    "img_rect": None,
    "bg_question": None,
    "box": None,
    "border_box": None,
    "sound_btn": None,
    "star_tracker": None,
    "rocket_data": None,
    "game_back_btn": None,
    "feedback_active": False,
    "feedback_start_time": 0,
    "feedback_type": None,
    "pending_answer": None,
    "vui_prompted": False
}

def load_all_images(session):
    easy_imgs = get_img(session.category, DIFFICULTY_EASY)
    diff_imgs = get_img(session.category, DIFFICULTY_DIFFICULT)
    return {**easy_imgs, **diff_imgs}

def init_ui(session, screen):
    global _ui_state
    img_dict = load_all_images(session)
    word = session.current_word

    word_img = img_dict[word]
    sound_btn = SoundButton("assets/images/question/volume_up.png", (screen.get_width() - 100, 10))

    bg_img = pygame.image.load("assets/images/question/background.png").convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (screen.get_width() * 0.999, screen.get_height() * 0.999))
    bg_rect = bg_img.get_rect(topleft=(0, 0))

    width = word_img.get_width() * 0.4
    height = word_img.get_height() * 0.4
    resize_img = pygame.transform.scale(word_img, (int(width), int(height)))

    img_rect = resize_img.get_rect()
    img_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 65)

    board_width = int(screen.get_width() * 0.45)
    board_height = int(screen.get_height() * 0.45)

    box = pygame.Rect(0, 0, board_width, board_height)
    box.center = img_rect.center

    border_thickness = 5
    border_box = box.inflate(border_thickness * 2, border_thickness * 2)

    star_tracker = StarTracker("assets/images/question/star.png", "assets/images/question/image.png", screen.get_width())
    rocket_img = pygame.image.load("assets/images/question/launch.png").convert_alpha()
    rocket_img = pygame.transform.scale(rocket_img, (110, 110))
    rocket_x = border_box.right + 70
    rocket_y = border_box.centery - 160
    rocket_rect = rocket_img.get_rect(topleft=(rocket_x, rocket_y))

    game_back_btn = Button((1080, 20), (170, 60), (200, 50, 50), border_radius=15)

    btn_width = screen.get_width() * 0.15
    btn_height = screen.get_height() * 0.1
    gap = screen.get_width() * 0.08
    y_pos = screen.get_height() * 0.75

    question_obj = Question(session.current_word, session.session_words)
    a, b, c, d = question_obj.create_question()
    options = [a, b, c, d]
    labels = ["A", "B", "C", "D"]
    choice_buttons = []

    for i in range(4):
        x_pos = gap + i * (btn_width + gap)
        choice_buttons.append(QuestionBtn((x_pos, y_pos), (btn_width, btn_height), (255, 255, 255), f"{labels[i]}. {options[i]}", 10))

    _ui_state.update({
        "current_word_loaded": word,
        "choice_buttons": choice_buttons,
        "word_img": resize_img,
        "img_rect": img_rect,
        "bg_question": {"rect": bg_rect, "img": bg_img},
        "box": box,
        "border_box": border_box,
        "sound_btn": sound_btn,
        "star_tracker": star_tracker,
        "rocket_data": (rocket_img, rocket_rect),
        "game_back_btn": game_back_btn,
        "feedback_active": False,
        "pending_answer": None
    })

def process_answer(session,  submitted_answer):
    global _ui_state

    _ui_state["feedback_active"] = True
    _ui_state["feedback_start_time"] = pygame.time.get_ticks()

    submitted_clean = submitted_answer.strip().lower()
    is_correct = session.current_word.lower() in submitted_clean

    _ui_state["pending_answer"] = session.current_word if is_correct else submitted_clean

    if is_correct:
        _ui_state["feedback_type"] = "correct"
        sound_manager.play_success_sound()
        _ui_state["target_score"] = session.game_state["round_score"] + 1
    else:
        _ui_state["feedback_type"] = "wrong"
        _ui_state["target_score"] = session.game_state["round_score"]

    for btn in _ui_state["choice_buttons"]:
        btn_word = btn.text.split(". ")[1].lower()
        if is_correct and btn_word == session.current_word.lower():
            btn.mark_correct()
        elif not is_correct and (btn_word == submitted_clean or btn_word in submitted_clean):
            btn.mark_wrong()

def run(screen, events, session, feedback_module, win_module, round_summary_module):
    global _ui_state

    if _ui_state["current_word_loaded"] != session.current_word:
        init_ui(session, screen)
        vui.speak_and_listen("Can you tell me what this is?")
        _ui_state["vui_prompted"] = True

    mouse_pos = pygame.mouse.get_pos()

    if not _ui_state["feedback_active"]:
        spoken_text = vui.get_recognized_text()
        if spoken_text:
            if spoken_text != "UNKNOWN_AUDIO":
                process_answer(session, spoken_text)
            else:
                vui.speak_and_listen("I didn't quite catch that. Try clicking a button!")

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if _ui_state["sound_btn"] and _ui_state["sound_btn"].rect.collidepoint(event.pos):
                    vui.speak_and_listen("Can you tell me what this is?")

                if _ui_state["game_back_btn"] and _ui_state["game_back_btn"].is_clicked(event):
                    session.game_state["round_score"] = 0
                    session.round_counter = 0
                    _ui_state["current_word_loaded"] = None
                    return "category"

                for btn in _ui_state["choice_buttons"]:
                    if btn.rect.collidepoint(event.pos):
                        selected_answer = btn.text.split(". ")[1]
                        _ui_state["feedback_active"] = True
                        _ui_state["feedback_start_time"] = pygame.time.get_ticks()
                        _ui_state["pending_answer"] = selected_answer

                        if selected_answer == session.current_word:
                            _ui_state["feedback_type"] = "correct"
                            btn.mark_correct()
                            sound_manager.play_success_sound()
                            _ui_state["target_score"] = session.game_state["round_score"] + 1
                        else:
                            _ui_state["feedback_type"] = "wrong"
                            btn.mark_wrong()
                            _ui_state["target_score"] = session.game_state["round_score"]
                        break

    draw(screen, _ui_state["word_img"], _ui_state["img_rect"], _ui_state["choice_buttons"],
         _ui_state["box"], _ui_state["border_box"], _ui_state["bg_question"],
         _ui_state["sound_btn"], mouse_pos, _ui_state["game_back_btn"], _ui_state["rocket_data"])

    if _ui_state["star_tracker"]:
        _ui_state["star_tracker"].draw(screen, session.game_state["round_score"])

    if _ui_state["feedback_active"]:
        current_time = pygame.time.get_ticks()
        anim_timer = current_time - _ui_state["feedback_start_time"]

        feedback_module.draw(screen, _ui_state["feedback_type"], anim_timer, session.hint_dict[session.current_word])

        if anim_timer >= 1000:
            _ui_state["feedback_active"] = False

            is_correct_bool = (_ui_state["pending_answer"] == session.current_word)
            status = session.advance(is_correct_bool)

            session.game_state["round_score"] = _ui_state["target_score"]

            if status == "game_over":
                sound_manager.play_victory_sound()
                return "win"
            elif status in ("round_complete", "difficulty_up"):
                _ui_state["current_word_loaded"] = None
                return "round_summary"
            else:
                _ui_state["current_word_loaded"] = None
                sound_manager.play_word_audio()
                return "question"

    return "question"

def draw(screen, word_img, img_rect, buttons, box, border_box, bg_question, sound_btn, mouse_pos, game_back_btn,
         rocket_data=None):
    screen.blit(bg_question["img"], bg_question["rect"])

    pygame.draw.rect(screen, (145, 185, 235), border_box, border_radius=28)
    pygame.draw.rect(screen, (255, 255, 255), box, border_radius=28)
    screen.blit(word_img, img_rect)

    if sound_btn:
        sound_btn.draw(screen, mouse_pos)

    if rocket_data:
        rocket_img, rocket_rect = rocket_data
        screen.blit(rocket_img, rocket_rect)

    if game_back_btn:
        game_back_btn.draw(screen)
        font = pygame.font.SysFont("Arial", 30, bold=True)
        text = font.render("Quit", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=game_back_btn.rect.center))

    for button in buttons:
        button.draw(screen)

def get_img(chosen_letter, difficulty):
    if chosen_letter == "animals":
        data = init_animals[difficulty]
    elif chosen_letter == "food":
        data = init_fruits_veg[difficulty]
    elif chosen_letter == "colors":
        data = init_colors[difficulty]
    else:
        data = init_animals[difficulty] + init_fruits_veg[difficulty] + init_colors[difficulty]

    img_dict = {d["name"]: pygame.image.load(d.get("image")) for d in data}
    return img_dict