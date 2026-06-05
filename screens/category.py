from components.button import Button

def init():
    buttons = [
        Button((300, 150), (200, 70), (255, 0, 0), "Animals", 30),
        Button((900, 150), (200, 70), (0, 255, 0), "Food", 30),
        Button((300, 450), (200, 70), (0, 0, 255), "Colors", 30),
        Button((900, 450), (200, 70), (255, 255, 0), "Mixed", 30),
    ]
    return buttons

def draw(buttons, screen):
    for button in buttons:
        button.draw(screen)

def handle_events(buttons, event):
    for button in buttons:
        if button.is_clicked(event):
            return button.text.lower()