import pygame
from game import Question
from components.button import Button
from words import init_animals, init_fruits_veg, init_colors

def init(word, img_dict):
    word_img = img_dict[word]
    width = word_img.get_width() * 0.5
    height = word_img.get_height() * 0.5
    resize_img = pygame.transform.scale(word_img, (int(width), int(height)))
    img_rect = resize_img.get_rect()
    img_rect.topleft = (469, 60)
    return resize_img, img_rect

def get_buttons(session):
    question = Question(session.current_word, session.session_words)
    a, b, c, d = question.create_question()
    buttons = [
        Button((150, 400), (200, 70), (0, 0, 0), f"A. {a}", 30),
        Button((450, 400), (200, 70), (0, 0, 0), f"B. {b}", 30),
        Button((750, 400), (200, 70), (0, 0, 0), f"C. {c}", 30),
        Button((1050, 400), (200, 70), (0, 0, 0), f"D. {d}", 30),
    ]

    return buttons

def draw(screen, word_img, img_rect, buttons):
    screen.blit(word_img, img_rect)
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