from pygame.sprite import Group

from ship import Ship
from alien import Alien
from bullet import Bullet

class GameObjects():
    """
    Holds and provides access to all visible, stateful game object.
    (Ship, aliens, bullets)
    """

    def __init__(self, screen, settings):
        self.ship = Ship(screen, settings)
        self.bullets = Group()
        self.aliens = Group()

    def draw(self, screen):
        for bullet in self.bullets.sprites():
            bullet.draw()
        self.ship.draw()
        self.aliens.draw(screen)