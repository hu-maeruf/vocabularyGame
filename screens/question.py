import pygame
import math
from game import Question
from components.button import Button
from words import init_animals, init_fruits_veg, init_colors


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

    def draw(self, screen,current_score):
        pygame.draw.rect(screen, (20, 35, 90), self.pill_rect, border_radius=30)
        pygame.draw.rect(screen, (100, 130, 200), self.pill_rect, width=3, border_radius=30)

        for i in range(self.max_stars):
            star_x = self.x + self.padding_x + i * (40 + self.gap)
            star_y = self.y + self.padding_y

            if i < current_score:
                screen.blit(self.star_filled, (star_x, star_y))
            else:
                screen.blit(self.star_empty, (star_x, star_y))


def init(word, img_dict, screen):
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

    star_tracker = StarTracker("assets/images/question/star.png", "assets/images/question/image.png",screen.get_width())
    rocket_img = pygame.image.load("assets/images/question/launch.png").convert_alpha()
    rocket_img = pygame.transform.scale(rocket_img, (110, 110))
    rocket_x = border_box.right + 70
    rocket_y = border_box.centery - 160
    rocket_rect = rocket_img.get_rect(topleft=(rocket_x,rocket_y))

    game_back_btn = Button((1080, 20), (170, 60), (200, 50, 50), border_radius=15)

    return resize_img, img_rect, {"rect": bg_rect, "img": bg_img}, box, border_box, sound_btn, star_tracker, (
        rocket_img, rocket_rect), game_back_btn


def get_buttons(session, screen):
    width = screen.get_width()
    height = screen.get_height()

    btn_width = width * 0.15
    btn_height = height * 0.1
    gap = width * 0.08
    y_pos = height * 0.75

    question = Question(session.current_word, session.session_words)
    a, b, c, d = question.create_question()
    options = [a, b, c, d]
    labels = ["A", "B", "C", "D"]
    buttons = []

    for i in range(4):
        x_pos = gap + i * (btn_width + gap)
        buttons.append(
            QuestionBtn((x_pos, y_pos), (btn_width, btn_height), (255, 255, 255), f"{labels[i]}. {options[i]}", 10))

    return buttons


def draw(screen, word_img, img_rect, buttons, box, border_box, bg_question, sound_btn, mouse_pos, game_back_btn,rocket_data=None):
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

def handle_events(buttons, event):
    for button in buttons:
        if button.is_clicked(event):
            full_text = button.text
            answer = full_text[3:]
            return answer

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