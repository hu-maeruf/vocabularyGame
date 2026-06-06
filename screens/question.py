import pygame
from game import Question
from components.button import Button

def init(word, img_dict, session_words):
    word_img = img_dict[word]
    width = word_img.get_width() * 0.5
    height = word_img.get_height() * 0.5
    resize_img = pygame.transform.scale(word_img, (int(width), int(height)))
    img_rect = resize_img.get_rect()
    img_rect.topleft = (469, 60)
    question = Question(word, session_words)
    a, b, c, d = question.create_question()
    buttons = [
        Button((150, 400), (200, 70), (0, 0, 0), f"A. {a}", 30),
        Button((450, 400), (200, 70), (0, 0, 0), f"B. {b}", 30),
        Button((750, 400), (200, 70), (0, 0, 0), f"C. {c}", 30),
        Button((1050, 400), (200, 70), (0, 0, 0), f"D. {d}", 30),
    ]
    return resize_img, img_rect, buttons

def draw(screen, word_img, img_rect, buttons):
    screen.blit(word_img, img_rect)
    for button in buttons:
        button.draw(screen)

def handle_events(buttons, event):
    for button in buttons:
        if button.is_clicked(event):
            full_text = button.text
            answer = full_text[3:].lower()
            return answer