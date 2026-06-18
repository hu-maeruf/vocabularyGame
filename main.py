import pygame
import components.tts_helper as tts
import screens.home as home
import screens.category as cat
import screens.question as question
import screens.feedback as feedback
import screens.round_summary as round_summary
import screens.win as win
from game import GameSession, play_intro_phase

pygame.init()
pygame.mixer.init()

try:
    pygame.mixer.music.load("assets/audio/music/background.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    print("Background music started!")
except Exception as e:
    print(f"Could not load background music: {e}")

DIFFICULTY_EASY = "easy"
DIFFICULTY_DIFFICULT = "diff"

def main():
    screen = pygame.display.set_mode((1270, 670))
    session = GameSession()
    home_btn, font_surface = home.init()
    gloss = home.create_gloss_surface()
    choice_buttons = None
    triangle_points, arrow_point = home.triangle_points()
    category_btn, cat_title, cat_back_btn = cat.init(screen)
    pygame.display.set_caption("Vocabulary Adventure")
    running = True
    state = "home"
    word_img = None
    img_rect = None
    feedback_active = False
    feedback_start_time = 0
    feedback_type = None
    pending_answer = None
    continue_btn = None
    graphics = None
    summary_star_tracker = None
    game_back_btn = None
    win_score_text = None
    win_score_rect = None
    play_again_btn = None
    back_btn = None
    bg_question = None
    box = None
    border_box = None
    sound_btn = None
    star_tracker = None
    rocket_data = None
    clock = pygame.time.Clock()

    while running:
        screen.fill((185, 226, 245))
        mouse_pos = pygame.mouse.get_pos()

        if state == "home":
            home.draw(screen, gloss, triangle_points, arrow_point, font_surface)
        elif state == "category":
            cat.draw_space_gradient(screen)
            cat.draw_btn(category_btn, screen, cat_title, cat_back_btn)
        elif state == "question":
            if word_img and img_rect and choice_buttons and star_tracker:
                question.draw(screen, word_img, img_rect, choice_buttons, box, border_box, bg_question, sound_btn,mouse_pos, game_back_btn,rocket_data)
                star_tracker.draw(screen, session.game_state["round_score"])

            if feedback_active:
                current_time = pygame.time.get_ticks()
                anim_timer = pygame.time.get_ticks() - feedback_start_time
                feedback.draw(screen, feedback_type, anim_timer, session.hint_dict[session.current_word])

                if current_time - feedback_start_time >= 1000:
                    feedback_active = False
                    status = session.advance(pending_answer)

                    if status == "game_over":
                        state = "win"
                        graphics, win_score_text, win_score_rect, play_again_btn, back_btn = win.init(screen, session.game_state["score"])
                    elif status in ("round_complete", "difficulty_up"):
                        state = "round_summary"
                        continue_btn, graphics, summary_star_tracker = round_summary.init(screen, session.game_state["round_score"])
                    else:
                        img_dict = load_image(session)
                        word_img, img_rect, bg_question, box, border_box, sound_btn, star_tracker, rocket_data, game_back_btn = question.init(session.current_word, img_dict, screen)
                        choice_buttons = question.get_buttons(session, screen)
                        play_word_audio()

        elif state == "round_summary":
            round_summary.draw(screen, bg_question, continue_btn, graphics, summary_star_tracker)
        elif state == "win":
            win.draw(screen, graphics, win_score_text, win_score_rect, play_again_btn, back_btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == "question" and not feedback_active:
                    if sound_btn and sound_btn.rect.collidepoint(event.pos):
                        play_word_audio()
                        continue
                    if game_back_btn.is_clicked(event):
                        session.game_state["round_score"] = 0
                        session.round_counter = 0
                        state = "category"
                    else:
                        for btn in choice_buttons:
                            if btn.rect.collidepoint(event.pos):
                                selected_answer = btn.text.split(". ")[1]
                                feedback_active = True
                                feedback_start_time = pygame.time.get_ticks()

                                if selected_answer == session.current_word:
                                    feedback_type = "correct"
                                    pending_answer = True
                                    btn.mark_correct()
                                else:
                                    feedback_type = "wrong"
                                    pending_answer = False
                                    btn.mark_wrong()
                                break

            if state == "home":
                if home.is_clicked(event, home_btn):
                    state = "category"
            elif state == "category":
                if cat_back_btn and cat_back_btn.is_clicked(event):
                    state = "home"
                else:
                    session.category = cat.handle_events(category_btn, event)
                    if session.category:
                        state = "question"
                        play_intro_phase(session)
                        session.game_state["round_score"] = 0
                        session.round_counter = 0
                        img_dict = question.get_img(session.category, DIFFICULTY_EASY)
                        word_img, img_rect, bg_question, box, border_box, sound_btn, star_tracker, rocket_data, game_back_btn = question.init(session.current_word, img_dict, screen)
                        choice_buttons = question.get_buttons(session, screen)
                        play_word_audio()
            elif state == "round_summary":
                result = round_summary.handle_events(event, continue_btn)
                if result == "question":
                    session.game_state["round_score"] = 0
                    state = "question"
                    img_dict = load_image(session)
                    word_img, img_rect, bg_question, box, border_box, sound_btn, star_tracker, rocket_data, game_back_btn = question.init(session.current_word, img_dict, screen)
                    choice_buttons = question.get_buttons(session, screen)
                    play_word_audio()
            elif state == "win":
                result = win.handle_events(event, play_again_btn, back_btn)
                if result == "play_again":
                    session = GameSession()
                    session.category = session.category  # preserves selected category if applicable, or resets fully
                    state = "category"
                    choice_buttons = None
                elif result == "category":
                    # "Quit Game" should take them completely back to the main home screen
                    session = GameSession()
                    state = "home"
                    choice_buttons = None

        clock.tick(60)
        pygame.display.update()


def load_image(session):
    easy_imgs = question.get_img(session.category, DIFFICULTY_EASY)
    diff_imgs = question.get_img(session.category, DIFFICULTY_DIFFICULT)
    img_dict = {**easy_imgs, **diff_imgs}
    return img_dict

def play_word_audio():
    full_sentence = "What is this?"
    tts_sound = tts.speak_word(full_sentence, "question_prompt")
    if tts_sound:
        try:
            voice_channel = pygame.mixer.Channel(7)
            voice_channel.stop()
            voice_channel.play(tts_sound)
            tts_sound.set_volume(0.5)
        except Exception as e:
            print(f"Audio playback error: {e}")

if __name__ == "__main__":
    main()