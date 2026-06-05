import pygame

class Button:
    def __init__(self, position, size, color, text, font_size):
        self.position = position
        self.size = size
        self.color = color
        self.text = text
        self.font_size = font_size
        self.rect = pygame.Rect((0,0), self.size)
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.rect.center = self.position
        self.text_surface = self.font.render(self.text, True, (0, 0, 255))
        self.text_rect = self.text_surface.get_rect()

    def draw(self, screen):
        self.text_rect.center = self.rect.center
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False