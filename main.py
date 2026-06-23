import pygame
import sound_manager
import screens.home as home
import screens.category as cat
import screens.friend_selection as friend_selection
import screens.question as question
import screens.feedback as feedback
import screens.round_summary as round_summary
import screens.win as win
from game import GameSession
from components.transition_manager import TransitionManager

pygame.init()
pygame.mixer.init()
sound_manager.start_background_music()

def main():
    screen = pygame.display.set_mode((1270, 670))
    session = GameSession()
    pygame.display.set_caption("Vocabulary Adventure")

    transition = TransitionManager(duration_ms=300)
    running = True
    state = "home"
    clock = pygame.time.Clock()

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        next_state = state
        active_events = [] if transition.phase != TransitionManager.IDLE else events

        if state == "home":
            next_state = home.run(screen, active_events)

        elif state == "category":
            next_state = cat.run(screen, active_events, session)

        elif state == "friend_selection":
            next_state = friend_selection.run(screen, active_events, session)

        elif state == "question":
            next_state = question.run(screen, active_events, session, feedback)

        elif state == "round_summary":
            next_state = round_summary.run(screen, active_events, session)

        elif state == "win":
            next_state = win.run(screen, events, session)

        if next_state != state and transition.phase == TransitionManager.IDLE:
            transition.request(next_state)

        state = transition.update(screen, state)

        clock.tick(60)
        pygame.display.update()

if __name__ == "__main__":
    main()