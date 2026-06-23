import pygame

class TransitionManager:
    FADE_OUT = "fade_out"
    FADE_IN = "fade_in"
    IDLE = "idle"

    def __init__(self, duration_ms=300):
        self.duration = duration_ms
        self.phase = self.IDLE
        self.start_time = 0
        self.pending_state = None
        self._overlay = None

    def request(self, new_state):
        if self.phase == self.IDLE:
            self.pending_state = new_state
            self.phase = self.FADE_OUT
            self.start_time = pygame.time.get_ticks()

    def update(self, screen, current_state):
        if self.phase == self.IDLE:
            return current_state

        if self._overlay is None or self._overlay.get_size() != screen.get_size():
            self._overlay = pygame.Surface(screen.get_size())
            self._overlay.fill((0, 0, 0))

        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(1.0, elapsed / self.duration)

        if self.phase == self.FADE_OUT:
            alpha = int(255 * progress)
            self._overlay.set_alpha(alpha)
            screen.blit(self._overlay, (0, 0))

            if progress >= 1.0:
                self.phase = self.FADE_IN
                self.start_time = pygame.time.get_ticks()
                return self.pending_state

        elif self.phase == self.FADE_IN:
            alpha = int(255 * (1.0 - progress))
            self._overlay.set_alpha(alpha)
            screen.blit(self._overlay, (0, 0))

            if progress >= 1.0:
                self.phase = self.IDLE
                self.pending_state = None

        return current_state