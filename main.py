import pygame
import sound_manager
import screens.home as home
import screens.category as cat
import screens.question as question
import screens.feedback as feedback
import screens.round_summary as round_summary
import screens.win as win
from game import GameSession

pygame.init()
pygame.mixer.init()
sound_manager.start_background_music()


def main():
    screen = pygame.display.set_mode((1270, 670))
    session = GameSession()
    pygame.display.set_caption("Vocabulary Adventure")

    running = True
    state = "home"
    clock = pygame.time.Clock()

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if state == "home":
            state = home.run(screen, events)

        elif state == "category":
            state = cat.run(screen, events, session)

        elif state == "question":
            state = question.run(screen, events, session, feedback, win, round_summary)

        elif state == "round_summary":
            pass

        elif state == "win":
            pass

        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    main()