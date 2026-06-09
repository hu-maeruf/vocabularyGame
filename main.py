import pygame
import screens.home as home
import screens.category as cat
import screens.question as question
from game import GameSession, play_intro_phase

pygame.init()

DIFFICULTY_EASY = "easy"
DIFFICULTY_DIFFICULT = "diff"

def main():
    screen = pygame.display.set_mode((1200, 600))
    home_btn = home.init(screen)
    category_btn = cat.init()
    pygame.display.set_caption("Vocabulary Adventure")
    running = True
    session = GameSession()
    state = "home"
    word_img = None
    img_rect = None
    choice_buttons = None
    img_dict = None
    feedback_active = False
    feedback_start_time = 0
    feedback_type = None
    pending_answer = None
    clock = pygame.time.Clock()
    while running:
        screen.fill((185, 226, 245))
        if state == "home":
            home.draw(home_btn, screen)
        elif state == "category":
            cat.draw(category_btn, screen)
        elif state == "question":
            if word_img and img_rect and choice_buttons:
                question.draw(screen, word_img, img_rect, choice_buttons)
            if feedback_active:
                current_time = pygame.time.get_ticks()
                if feedback_type == "correct":
                    pygame.draw.rect(screen, (0, 255, 0), screen.get_rect(), 10)  # green border
                else:
                    pygame.draw.rect(screen, (255, 0, 0), screen.get_rect(), 10)
                if current_time - feedback_start_time >= 1000:
                    feedback_active = False
                    session.advance(pending_answer)
                    if session.game_over:
                        state = "win"
                    else:
                        img_dict = question.get_img(session.category, session.difficulty)
                        word_img, img_rect, choice_buttons = question.init(session.current_word, img_dict, session.session_words)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == "home":
                if home_btn.is_clicked(event):
                    state = "category"
            elif state == "category":
                session.category = cat.handle_events(category_btn, event)
                if session.category:
                    state = "question"
                    play_intro_phase(session, DIFFICULTY_EASY)
                    img_dict = question.get_img(session.category, DIFFICULTY_EASY)
                    word_img, img_rect, choice_buttons = question.init(
                        session.current_word, img_dict, session.session_words
                    )
            elif state == "question":
                answer = question.handle_events(choice_buttons, event)
                if answer:
                    is_correct = session.check_answer(answer, session.current_word)
                    feedback_active = True
                    feedback_start_time = pygame.time.get_ticks()
                    feedback_type = "correct" if is_correct else "wrong"
                    pending_answer = is_correct
            elif state == "win":
                pass
        clock.tick(60)
        pygame.display.update()

if __name__ == "__main__":
    main()