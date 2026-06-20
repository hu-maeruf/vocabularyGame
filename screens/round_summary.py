from typing import Any
import pygame
from components.button import Button
from screens.question import StarTracker

_ui_state: dict[str, Any] = {
    "initialized": False,
    "continue_btn": None,
    "graphics": None,
    "star_tracker": None,
    "bg_img": None
}

def init(screen, round_score):
    card_height = 550
    card_top = (screen.get_height() - card_height) // 2
    card_centerx = screen.get_width() // 2

    btn_size = (300, 70)
    btn_pos = (card_centerx - btn_size[0] // 2, card_top + 450)
    continue_btn = Button(btn_pos, btn_size, (76, 175, 80), border_radius=30)
    graphics = {"score": round_score}

    try:
        graphics["level"] = pygame.transform.smoothscale(pygame.image.load("assets/images/round_summary/level.png").convert_alpha(), (400, 170))
        graphics["completed"] = pygame.transform.smoothscale(pygame.image.load("assets/images/round_summary/completed.png").convert_alpha(), (400, 170))
        graphics["trophy"] = pygame.transform.smoothscale(pygame.image.load("assets/images/round_summary/trophy.png").convert_alpha(), (250, 250))
    except Exception as e:
        print(f"Loading Error: {e}")

    star_tracker = StarTracker("assets/images/question/star.png", "assets/images/question/image.png",screen.get_width(), y_pos=card_top + 380)
    return continue_btn, graphics, star_tracker

def run(screen, events, session):
    global _ui_state

    if not _ui_state["initialized"]:
        current_score = session.game_state.get("round_score", 0)
        continue_btn, graphics, star_tracker = init(screen, current_score)
        _ui_state["continue_btn"] = continue_btn
        _ui_state["graphics"] = graphics
        _ui_state["star_tracker"] = star_tracker

        try:
            bg = pygame.image.load("assets/images/question/background.png").convert_alpha()
            _ui_state["bg_img"] = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
        except Exception:
            _ui_state["bg_img"] = None

        _ui_state["initialized"] = True

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if _ui_state["continue_btn"] and _ui_state["continue_btn"].is_clicked(event):
                session.game_state["round_score"] = 0

                _ui_state["initialized"] = False
                return "question"

    if _ui_state["bg_img"]:
        screen.blit(_ui_state["bg_img"], (0, 0))
    else:
        screen.fill((20, 35, 70))

    card_rect = pygame.Rect(0, 0, 800, 550)
    card_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    pygame.draw.rect(screen, (255, 255, 255), card_rect, border_radius=40)
    pygame.draw.rect(screen, (145, 185, 235), card_rect, width=8, border_radius=40)

    graphics = _ui_state["graphics"]
    if graphics:
        if "level" in graphics and graphics["level"]:
            screen.blit(graphics["level"], graphics["level"].get_rect(center=(card_rect.centerx, card_rect.top + 70)))
        if "completed" in graphics and graphics["completed"]:
            screen.blit(graphics["completed"],graphics["completed"].get_rect(center=(card_rect.centerx, card_rect.top + 120)))
        if "trophy" in graphics and graphics["trophy"]:
            screen.blit(graphics["trophy"],graphics["trophy"].get_rect(center=(card_rect.centerx, card_rect.top + 250)))

    if _ui_state["star_tracker"] and graphics:
        _ui_state["star_tracker"].draw(screen, graphics["score"])

    if _ui_state["continue_btn"]:
        _ui_state["continue_btn"].draw(screen)
        font = pygame.font.SysFont("Arial", 30, bold=True)
        text = font.render("Continue", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=_ui_state["continue_btn"].rect.center))

    return "round_summary"