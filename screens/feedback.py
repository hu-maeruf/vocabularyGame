import pygame

def draw(screen, feedback_type, animation_timer, current_hint):
    correct_img = pygame.image.load("assets/images/feedback/correct.png").convert_alpha()
    star_img = pygame.image.load("assets/images/feedback/star.png").convert_alpha()
    oops_img = pygame.image.load("assets/images/feedback/oops.png").convert_alpha()
    sad_star = pygame.image.load("assets/images/feedback/sad_star.png").convert_alpha()

    dim_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    dim_surface.fill((0, 0, 0, 120))
    screen.blit(dim_surface, (0, 0))

    overlay_rect = pygame.Rect(0, 0, 700, 400)
    overlay_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    pygame.draw.rect(screen, (255, 255, 255), overlay_rect, border_radius=40)
    pygame.draw.rect(screen, (145, 185, 235), overlay_rect, width=8, border_radius=40)

    if feedback_type == "correct":
        title_rect = correct_img.get_rect(center=(overlay_rect.centerx, overlay_rect.top + 80))
        screen.blit(correct_img, title_rect)
        progress = min(1.0, animation_timer / 300)
        size = int(180 * progress)
        star_scaled = pygame.transform.smoothscale(star_img, (size, size))
        screen.blit(star_scaled, star_scaled.get_rect(center=(overlay_rect.centerx, overlay_rect.centery)))

        font = pygame.font.SysFont("Arial", 40, bold=True)
        text_surf = font.render("Great job! You got it right!", True, (100, 100, 100))
        text_rect = text_surf.get_rect(center=(overlay_rect.centerx, overlay_rect.bottom - 60))
        screen.blit(text_surf, text_rect)

    elif feedback_type == "wrong":
        oops_rect = oops_img.get_rect(center=(overlay_rect.centerx, overlay_rect.top + 70))
        screen.blit(oops_img, oops_rect)
        max_star_size = 170
        star_scaled = pygame.transform.smoothscale(sad_star, (max_star_size, max_star_size))
        star_rect = star_scaled.get_rect(center=(overlay_rect.centerx, overlay_rect.centery))
        screen.blit(star_scaled, star_rect)

        hint_box = pygame.Rect(0, 0, 500, 80)
        hint_box.center = (overlay_rect.centerx, overlay_rect.centery + 130)
        pygame.draw.rect(screen, (255, 245, 200), hint_box, border_radius=15)
        pygame.draw.rect(screen, (230, 210, 150), hint_box, width=3, border_radius=15)

        font = pygame.font.SysFont("Arial", 30)
        hint_text = font.render(f"Hint: {current_hint}", True, (100, 80, 40))
        screen.blit(hint_text, hint_text.get_rect(center=hint_box.center))