import pygame.font

class Button():
    def __init__(self, message, screen, settings):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 200, 50
        self.color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_message(message)

    def prep_message(self, message):
        """Turn message into a rendered image and center text on the button."""
        self.message_image = self.font.render(message, True, self.text_color, self.color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
