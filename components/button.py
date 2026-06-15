import pygame

class Button:
    def __init__(self, position, size, color, border_radius=0):
        self.color = color
        self.rect = pygame.Rect(position, size)
        self.border_radius = border_radius

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False