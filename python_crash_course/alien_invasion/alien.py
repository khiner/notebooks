import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, screen, settings):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = screen

        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # Start each new alen near the top left of the screen.
        self.set_x(self.width())
        self.set_y(self.height())

        self.settings = settings
        self.speed = settings.fleet_speed

    def update(self):
        """Move the alien right."""
        self.set_x(self.x + self.speed * self.settings.fleet_direction)

    def draw(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def width(self):
        return self.rect.width

    def height(self):
        return self.rect.height

    def set_x(self, x):
        self.x = float(x)
        self.rect.x = int(x)

    def set_y(self, y):
        self.y = float(y)
        self.rect.y = int(y)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
