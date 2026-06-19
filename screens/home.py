import pygame

_assets = {}
radius = 100
center_x = 1270 // 2
center_y = 670 // 2
arrow_size = radius * 0.45

_ui_state: dict[str, pygame.Surface | bool | None] = {
    "initialized": False,
    "home_btn": None,
    "font_surface": None,
    "gloss": None,
    "tri_pts": None,
    "arrow_pt": None
}

def run(screen, events):
    global _ui_state
    if not _ui_state["initialized"]:
        _ui_state["home_btn"], _ui_state["font_surface"] = init()
        _ui_state["gloss"] = create_gloss_surface()
        _ui_state["tri_pts"], _ui_state["arrow_pt"] = triangle_points()
        _ui_state["initialized"] = True

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if _ui_state["home_btn"].collidepoint(event.pos):
                return "category"

    draw(screen, _ui_state["gloss"], _ui_state["tri_pts"], _ui_state["arrow_pt"], _ui_state["font_surface"])

    return "home"

def init():
    btn = pygame.rect.Rect(center_x - radius, center_y - radius, radius * 2, radius * 2)

    background = pygame.image.load("assets/images/home/background.png").convert_alpha()
    _assets["background"] = load_image(background, 0.89)

    voice_icon = pygame.image.load("assets/images/home/recording.png").convert_alpha()
    _assets["voice_icon"] = load_image(voice_icon, 0.2)

    voice_font = pygame.font.SysFont("Comic Sans MS", 25)
    text_surface = voice_font.render("Say Play", True, (11, 37, 69))

    return btn, text_surface

def draw(screen,  gloss, triangle_point, arrow_point, font):
    screen.blit(_assets["background"], (0, 0))
    # btn.draw(screen)
    pygame.draw.circle(screen, (217, 144, 4), (center_x, center_y + 4), radius)
    pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), radius - 2)
    pygame.draw.circle(gloss, (255, 255, 255, 75), (radius, radius), radius - 3)
    pygame.draw.circle(gloss, (0, 0, 0, 0), (radius + 6, radius + 6), radius - 6)
    screen.blit(gloss, (center_x - radius, center_y - radius))
    pygame.draw.polygon(screen, (210, 130, 5), triangle_point)
    pygame.draw.polygon(screen,(255, 253, 240), arrow_point, 3)
    screen.blit(_assets["voice_icon"], (20, 500))
    screen.blit(font, (22, 600))

def load_image(image, scale):
    width = int(image.get_width() * scale)
    height = int(image.get_height() * scale)
    resize = pygame.transform.scale(image, (width, height))

    return resize

def create_gloss_surface():
    gloss_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    return gloss_surface

def triangle_points():
    shadow_pt1 = (center_x - arrow_size * 0.5, center_y - arrow_size * 0.7 + 3)
    shadow_pt2 = (center_x - arrow_size * 0.5, center_y + arrow_size * 0.7 + 3)
    shadow_pt3 = (center_x + arrow_size * 0.9, center_y + 3)
    arrow_pt1 = (center_x - arrow_size * 0.5, center_y - arrow_size * 0.7)
    arrow_pt2 = (center_x - arrow_size * 0.5, center_y + arrow_size * 0.7)
    arrow_pt3 = (center_x + arrow_size * 0.9, center_y)
    return [shadow_pt1, shadow_pt2, shadow_pt3], [arrow_pt1, arrow_pt2, arrow_pt3]

def is_clicked(event, btn):
    mouse_pos = pygame.mouse.get_pos()
    if btn.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
    return False
