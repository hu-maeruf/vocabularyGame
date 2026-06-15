import pygame
from components.button import Button

class BtnCategory(Button):
    def __init__(self, position, size, top_color, text, img, color=(255, 255, 255), border_radius=20, font_color=(50, 65, 95)):
        super().__init__(position, size, color, border_radius)
        self.top_color = top_color
        self.text = text
        self.bar_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 50)
        self.font = pygame.font.SysFont("Arial", 30)
        self.text_surface = self.font.render(text, True, font_color)
        self.text_rect = self.text_surface.get_rect(midbottom=self.rect.midbottom)
        self.img = pygame.image.load(f"assets/images/category/{img}").convert_alpha()
        self.img = pygame.transform.scale(self.img, (int(self.rect.width * 0.4), int(self.rect.height * 0.4)))
        self.img_rect = self.img.get_rect(midtop=self.bar_rect.midbottom)

    def draw(self, screen):
        super().draw(screen)
        pygame.draw.rect(screen, self.top_color, self.bar_rect, border_top_left_radius=self.border_radius, border_top_right_radius=self.border_radius)
        screen.blit(self.img, self.img_rect)
        screen.blit(self.text_surface, self.text_rect)

def init(screen,):
    img = pygame.image.load("assets/images/category/title.png").convert_alpha()
    width = int(screen.get_width()) * 0.6
    height = int(screen.get_height()) * 0.3
    img = pygame.transform.scale(img, (width, height))
    buttons = [
        BtnCategory((350, 150), (250, 230), (255, 150, 130), "Animals", "animal.png"),
        BtnCategory((650, 150), (250, 230), (120, 210, 150), "Food", "food.png"),
        BtnCategory((350, 400), (250, 230), (140, 195, 240), "Colors", "color.png"),
        BtnCategory((650, 400), (250, 230), (245, 195, 90), "Mixed", "mixed.png")
    ]
    return buttons, img

def draw_btn(buttons, screen, img):
    width = screen.get_width()
    width_half = width // 2
    rect = img.get_rect()
    rect.center = (width_half, 80)
    for button in buttons:
        button.draw(screen)
    screen.blit(img, rect)
def handle_events(buttons, event):
    for button in buttons:
        if button.is_clicked(event):
            return button.text.lower()

def draw_space_gradient(surface, top_color = (20, 35, 70), bottom_color = (70, 110, 160)):
    height = surface.get_height()
    width = surface.get_width()
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        color = (r, g, b)
        pygame.draw.line(surface, color, (0, y), (width, y))