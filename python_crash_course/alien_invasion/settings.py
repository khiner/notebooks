class Settings():
    """Stores all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (100, 100, 240)
        self.ship_limit = 3
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 30
        self.fleet_drop_speed = 10.0

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        # For testing:
        self.super_bullets = True

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 10
        self.bullet_speed = 30
        self.fleet_speed = 10.0
        # fleet_direction of 1 respresents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.fleet_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
