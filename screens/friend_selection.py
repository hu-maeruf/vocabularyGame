import typing
import pygame
from vui_manager import vui

_ui_state: dict[str, typing.Any] = {
    "initialized": False,
    "cards": [],
    "title": None,
    "title_rect": None,
    "bg": None,
    "voice_prompted": False,
    "voice_timer": 0,
}

COMPANIONS = [
    {"id": "puppy", "color": (255, 182, 193), "shadow": (220, 130, 145)},
    {"id": "bunny", "color": (173, 216, 230), "shadow": (120, 165, 195)},
    {"id": "bear",  "color": (222, 184, 135), "shadow": (175, 135, 85)},
    {"id": "cat",   "color": (152, 251, 152), "shadow": (100, 200, 100)},
]

CARD_W, CARD_H = 220, 300
GAP = 50

def _load_companion_image(companion_id, card_w):
    try:
        img = pygame.image.load(f"assets/images/companion/{companion_id}/normal.png").convert_alpha()
        size = int(card_w * 0.82)
        return pygame.transform.smoothscale(img, (size, size))
    except Exception:
        surf = pygame.Surface((int(card_w * 0.82), int(card_w * 0.82)), pygame.SRCALPHA)
        pygame.draw.circle(surf, (200, 200, 200),(surf.get_width() // 2, surf.get_height() // 2), surf.get_width() // 2)
        return surf


def init(screen):
    try:
        title_font = pygame.font.Font("assets/fonts/kid_font.ttf", 52)
    except Exception:
        title_font = pygame.font.SysFont("Arial", 52, bold=True)

    title = title_font.render("Choose Your Friend!", True, (255, 255, 255))
    title_shadow = title_font.render("Choose Your Friend!", True, (80, 80, 160))
    title_rect = title.get_rect(center=(screen.get_width() // 2, 100))

    try:
        bg = pygame.image.load("assets/images/question/background.png").convert_alpha()
        bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
    except Exception:
        bg = None

    try:
        name_font = pygame.font.Font("assets/fonts/kid_font.ttf", 34)
    except Exception:
        name_font = pygame.font.SysFont("Arial", 34, bold=True)

    total_width = (CARD_W * len(COMPANIONS)) + (GAP * (len(COMPANIONS) - 1))
    start_x = (screen.get_width() - total_width) // 2
    card_y = (screen.get_height() - CARD_H) // 2 + 20

    cards = []
    for i, comp in enumerate(COMPANIONS):
        x = start_x + i * (CARD_W + GAP)
        rect = pygame.Rect(x, card_y, CARD_W, CARD_H)
        img = _load_companion_image(comp["id"], CARD_W)
        name_surf = name_font.render(comp["id"].capitalize(), True, (40, 40, 80))
        cards.append({
            "id": comp["id"],
            "rect": rect,
            "color": comp["color"],
            "shadow": comp["shadow"],
            "img": img,
            "name_surf": name_surf,
            "hovered": False,
        })

    return title, title_shadow, title_rect, cards, bg

def _draw_card(screen, card):
    rect = card["rect"]
    hover = card["hovered"]

    draw_rect = rect.move(0, -8 if hover else 0)

    # Shadow
    shadow_rect = draw_rect.move(0, 6)
    shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (*card["shadow"], 160),shadow_surf.get_rect(), border_radius=30)
    screen.blit(shadow_surf, shadow_rect)

    pygame.draw.rect(screen, card["color"], draw_rect, border_radius=30)

    border_w = 5 if hover else 3
    pygame.draw.rect(screen, (255, 255, 255), draw_rect, width=border_w, border_radius=30)

    img = card["img"]
    img_rect = img.get_rect(
        centerx=draw_rect.centerx,
        top=draw_rect.top + 14
    )
    screen.blit(img, img_rect)

    name_surf = card["name_surf"]
    name_rect = name_surf.get_rect(centerx=draw_rect.centerx, bottom=draw_rect.bottom - 18)
    screen.blit(name_surf, name_rect)

def run(screen, events, session):
    global _ui_state

    if not _ui_state["initialized"]:
        title, title_shadow, title_rect, cards, bg = init(screen)
        _ui_state.update({
            "initialized": True,
            "title": title,
            "title_shadow": title_shadow,
            "title_rect": title_rect,
            "cards": cards,
            "bg": bg,
            "voice_prompted": False,
            "voice_timer": pygame.time.get_ticks(),
        })

    if _ui_state["bg"]:
        screen.blit(_ui_state["bg"], (0, 0))
    else:
        screen.fill((20, 35, 90))

    mouse_pos = pygame.mouse.get_pos()

    for card in _ui_state["cards"]:
        card["hovered"] = card["rect"].collidepoint(mouse_pos)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for card in _ui_state["cards"]:
                if card["rect"].collidepoint(event.pos):
                    session.companion_id = card["id"]
                    _ui_state["initialized"] = False
                    return "question"

    shadow_rect = _ui_state["title_rect"].move(2, 3)
    screen.blit(_ui_state["title_shadow"], shadow_rect)
    screen.blit(_ui_state["title"], _ui_state["title_rect"])

    for card in _ui_state["cards"]:
        _draw_card(screen, card)

    if not _ui_state["voice_prompted"]:
        elapsed = pygame.time.get_ticks() - _ui_state["voice_timer"]
        if elapsed >= 500:
            vui.speak("Who do you want to be your friend? Pick your friend!")
            _ui_state["voice_prompted"] = True

    return "friend_selection"