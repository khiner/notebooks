import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Manage bullets fired from the ship."""

    def __init__(self, screen, settings, ship):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.set_y(self.rect.y)

        self.color = settings.bullet_color
        self.speed = settings.bullet_speed

    def update(self):
        """Move the bullet up the screen."""
        self.set_y(self.y - self.speed)

    def draw(self):
        """Draw the bullet."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def set_x(self, x):
        self.x = float(x)
        self.rect.x = int(x)

    def set_y(self, y):
        self.y = float(y)
        self.rect.y = int(y)
