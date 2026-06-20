from typing import Any
import pygame
from components.button import Button
import sound_manager

_ui_state: dict[str, Any] = {
    "initialized": False,
    "graphics": None,
    "score_text": None,
    "score_rect": None,
    "play_again_btn": None,
    "back_btn": None,
    "current_score_loaded": -1
}

def init(screen, score):
    graphics = {}

    try:
        bg_img = pygame.image.load("assets/images/win/win_bg.png").convert()
        graphics["bg"] = pygame.transform.smoothscale(bg_img, (screen.get_width(), screen.get_height()))
    except Exception as e:
        print(f"Error loading win screen background: {e}")
        graphics["bg"] = None

    font_small = pygame.font.SysFont("Arial", 40, bold=True)
    score_text = font_small.render(f"Score: {score}", True, (20, 35, 90))
    score_rect = score_text.get_rect(center=(screen.get_width() // 2, 430))

    play_again_btn = Button((365, 570), (240, 70), (76, 175, 80), border_radius=35)
    back_btn = Button((665, 570), (240, 70), (142, 115, 219), border_radius=35)

    return graphics, score_text, score_rect, play_again_btn, back_btn

def run(screen, events, session):
    global _ui_state

    current_score = session.game_state.get("score", 0)

    if not _ui_state["initialized"] or _ui_state["current_score_loaded"] != current_score:
        graphics, score_text, score_rect, play_again_btn, back_btn = init(screen, current_score)
        _ui_state.update({
            "initialized": True,
            "graphics": graphics,
            "score_text": score_text,
            "score_rect": score_rect,
            "play_again_btn": play_again_btn,
            "back_btn": back_btn,
            "current_score_loaded": current_score
        })

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if _ui_state["play_again_btn"] and _ui_state["play_again_btn"].is_clicked(event):
                session.game_state["score"] = 0
                session.game_state["round_score"] = 0
                session.round_counter = 0
                _ui_state["initialized"] = False
                sound_manager.start_background_music()
                return "category"

            if _ui_state["back_btn"] and _ui_state["back_btn"].is_clicked(event):
                session.game_state["score"] = 0
                session.game_state["round_score"] = 0
                session.round_counter = 0
                _ui_state["initialized"] = False
                sound_manager.start_background_music()
                return "home"

    graphics = _ui_state["graphics"]
    if graphics and graphics.get("bg"):
        screen.blit(graphics["bg"], (0, 0))
    else:
        screen.fill((185, 226, 245))

    if _ui_state["score_text"] and _ui_state["score_rect"]:
        screen.blit(_ui_state["score_text"], _ui_state["score_rect"])

    btn_font = pygame.font.SysFont("Arial", 30, bold=True)

    if _ui_state["play_again_btn"]:
        _ui_state["play_again_btn"].draw(screen)
        pygame.draw.rect(screen, (50, 120, 50), _ui_state["play_again_btn"].rect, width=4, border_radius=35)
        play_text = btn_font.render("Play Again", True, (255, 255, 255))
        screen.blit(play_text, play_text.get_rect(center=_ui_state["play_again_btn"].rect.center))

    if _ui_state["back_btn"]:
        _ui_state["back_btn"].draw(screen)
        pygame.draw.rect(screen, (90, 70, 150), _ui_state["back_btn"].rect, width=4, border_radius=35)
        back_text = btn_font.render("Quit Game", True, (255, 255, 255))
        screen.blit(back_text, back_text.get_rect(center=_ui_state["back_btn"].rect.center))

    return "win"