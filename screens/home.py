import pygame
import components.button as button

def init(screen):
    btn_center = screen.get_rect().center
    btn = button.Button(btn_center, (200, 70), (255, 255, 255), "Play", 50)
    return btn
#
def draw(btn, screen):
    btn.draw(screen)