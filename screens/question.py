import pygame

def init(word, img_dict):
    word_img = img_dict[word]
    width = word_img.get_width() * 0.5
    height = word_img.get_height() * 0.5
    img_rect = word_img.get_rect()
    img_rect.topleft = (469, 60)
    resize_img = pygame.transform.scale(word_img, (int(width), int(height)))

    print(f"width: {width} and height: {height} ")
    return resize_img, img_rect

def draw(screen, word_img, img_rect):
    screen.blit(word_img, img_rect)