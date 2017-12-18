import pygame

import game_functions as gf
from game_objects import GameObjects
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

def run_game():
    pygame.init()
    settings = Settings()
    stats = GameStats(settings)
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    sb = Scoreboard(screen, settings, stats)
    play_button = Button('Play', screen, settings)
    game_objects = GameObjects(screen, settings)
    gf.create_fleet(game_objects, screen, settings)

    while True:
        gf.check_events(game_objects, sb, play_button, screen, settings, stats)

        if stats.game_active:
            game_objects.ship.update()
            gf.update_bullets(game_objects, sb, screen, settings, stats)
            gf.update_aliens(game_objects, sb, screen, settings, stats)

        gf.update_screen(game_objects, screen, play_button, sb, settings, stats)

run_game()
