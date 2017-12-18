class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, settings):
        """Initialize statistics."""
        self.reset_stats(settings)
        self.game_active = False
        try:
            with open('high_score.txt') as high_score_file:
                self.high_score = int(high_score_file.read().strip())
        except FileNotFoundError:
            self.high_score = 0

    def reset_stats(self, settings):
        """Initialize statistics that can change during the game."""
        self.ships_left = settings.ship_limit
        self.score = 0
        self.level = 1
