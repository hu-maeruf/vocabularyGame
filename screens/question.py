import pygame
from game import Question
from components.button import Button
from words import init_animals, init_fruits_veg, init_colors

class QuestionBtn(Button):
    def __init__(self, position, size, color, text, border_radius):
        super().__init__(position, size, color, border_radius)
        self.text = text
        self.font = pygame.font.SysFont("Arial", 30)
        self.text_surface = self.font.render(self.text, True, (0,0,0))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.radius = border_radius

    def draw(self, screen):
        shadow_rect = self.rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(screen, (100, 100, 100), shadow_rect, border_radius=self.radius)
        super().draw(screen)
        pygame.draw.rect(screen, (145, 185, 235), self.rect, width=3,  border_radius=self.radius)
        screen.blit(self.text_surface, self.text_rect)


class SoundButton:
    def __init__(self, image_path, position=(30, 30), size=(70, 70)):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=(30,30))
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

    return resize_img, img_rect, {"rect":bg_rect, "img":bg_img}, box, border_box, sound_btn

def get_buttons(session,  screen):
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
        buttons.append(QuestionBtn((x_pos, y_pos), (btn_width, btn_height), (255, 255, 255), f"{labels[i]}. {options[i]}", 10))


    return buttons

def draw(screen, word_img, img_rect, buttons, box, border_box,bg_question, sound_btn, mouse_pos):
    screen.blit(bg_question["img"], bg_question["rect"])
    pygame.draw.rect(screen, (145, 185, 235), border_box, border_radius=28)
    pygame.draw.rect(screen, (255, 255, 255), box, border_radius=28)
    screen.blit(word_img, img_rect)
    sound_btn.draw(screen, mouse_pos)
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