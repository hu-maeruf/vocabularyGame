import pygame
import screens.home as home
import screens.category as cat
import screens.question as question
import screens.round_summary as round_summary
import screens.win as win
from game import GameSession, play_intro_phase

pygame.init()

DIFFICULTY_EASY = "easy"
DIFFICULTY_DIFFICULT = "diff"

def main():
    screen = pygame.display.set_mode((1270, 670))
    session = GameSession()
    home_btn, font_surface = home.init()
    gloss = home.create_gloss_surface()
    triangle_points, arrow_point = home.triangle_points()
    category_btn = cat.init()
    pygame.display.set_caption("Vocabulary Adventure")
    running = True
    state = "home"
    word_img = None
    img_rect = None
    choice_buttons = None
    feedback_active = False
    feedback_start_time = 0
    feedback_type = None
    pending_answer = None
    round_summary_btn = None
    round_summary_text = None
    round_summary_text_rect = None
    win_title = None
    win_title_rect = None
    win_score_text = None
    win_score_rect = None
    play_again_btn = None
    back_btn = None
    clock = pygame.time.Clock()
    while running:
        screen.fill((185, 226, 245))
        if state == "home":
            home.draw_space_gradient(screen)
            home.draw(screen, gloss, triangle_points, arrow_point, font_surface)
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
                    status = session.advance(pending_answer)
                    if status == "game_over":
                        state = "win"
                        win_title, win_title_rect, win_score_text, win_score_rect, play_again_btn, back_btn = win.init(
                            screen, session.game_state["score"])
                    elif status == "round_complete":
                        state = "round_summary"
                        round_summary_btn, round_summary_text, round_summary_text_rect = round_summary.init(screen)
                    elif status == "difficulty_up":
                        state = "round_summary"
                        round_summary_btn, round_summary_text, round_summary_text_rect = round_summary.init(screen)
                    else:
                        img_dict = load_image(session)
                        word_img, img_rect = question.init(session.current_word, img_dict)
                        choice_buttons = question.get_buttons(session)
        elif state == "round_summary":
            round_summary.draw(screen, round_summary_btn, round_summary_text, round_summary_text_rect)
        elif state == "win":
            win.draw(screen, win_title, win_title_rect, win_score_text, win_score_rect, play_again_btn, back_btn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == "home":
                if home.is_clicked(event, home_btn):
                    state = "category"
            elif state == "category":
                session.category = cat.handle_events(category_btn, event)
                if session.category:
                    state = "question"
                    play_intro_phase(session)
                    img_dict = question.get_img(session.category, DIFFICULTY_EASY)
                    word_img, img_rect = question.init(
                        session.current_word, img_dict)
                    choice_buttons = question.get_buttons(session)
            elif state == "question":
                answer = question.handle_events(choice_buttons, event)
                if answer:
                    is_correct = session.check_answer(answer, session.current_word)
                    feedback_active = True
                    feedback_start_time = pygame.time.get_ticks()
                    feedback_type = "correct" if is_correct else "wrong"
                    pending_answer = is_correct
            elif state == "round_summary":
                result = round_summary.handle_events(event, round_summary_btn)
                if result == "question":
                    state = "question"
                    img_dict = load_image(session)
                    word_img, img_rect = question.init(
                        session.current_word, img_dict)
                    choice_buttons = question.get_buttons(session)
            elif state == "win":
                result = win.handle_events(event, play_again_btn, back_btn)
                if result in ("play_again", "category"):
                    session = GameSession()
                    state = "category"
        clock.tick(60)
        pygame.display.update()

def load_image(session):
    easy_imgs = question.get_img(session.category, DIFFICULTY_EASY)
    diff_imgs = question.get_img(session.category, DIFFICULTY_DIFFICULT)
    img_dict = {**easy_imgs, **diff_imgs}
    return img_dict

if __name__ == "__main__":
    main()