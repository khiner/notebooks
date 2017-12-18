import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, screen, settings):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = screen

        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False

        self.speed = settings.ship_speed

        self.centerx = float(self.rect.centerx)

    def update(self):
        """Update the ship's position."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.centerx -= self.speed
        self.rect.centerx = self.centerx

    def draw(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def width(self):
        return self.rect.width

    def height(self):
        return self.rect.height

    def move_right(self):
        self.moving_right = True

    def move_left(self):
        self.moving_left = True

    def stop_moving_left(self):
        self.moving_left = False

    def stop_moving_right(self):
        self.moving_right = False

    def center(self):
        """Center the ship on the screen."""
        self.centerx = self.screen_rect.centerx
