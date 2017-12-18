import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, game_objects, sb, screen, settings, stats):
    if event.key == pygame.K_RIGHT:
        game_objects.ship.move_right()
    if event.key == pygame.K_LEFT:
        game_objects.ship.move_left()
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_objects, screen, settings)
    elif event.key == pygame.K_q:
        quit(stats)
    elif event.key == pygame.K_p:
        start_game(game_objects, sb, screen, settings, stats)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.stop_moving_right()
    elif event.key == pygame.K_LEFT:
        ship.stop_moving_left()

def check_events(game_objects, sb, play_button, screen, settings, stats):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(stats)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_objects, sb, screen, settings, stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, game_objects.ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(mouse_x, mouse_y, game_objects, sb, play_button, screen, settings, stats)

def check_play_button(mouse_x, mouse_y, game_objects, sb, play_button, screen, settings, stats):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        start_game(game_objects, sb, screen, settings, stats)

def start_game(game_objects, sb, screen, settings, stats):
    """Starts the game if not already in play."""
    if not stats.game_active:
        pygame.mouse.set_visible(False)
        settings.initialize_dynamic_settings()
        stats.reset_stats(settings)
        reset_game(game_objects, screen, settings)
        stats.game_active = True

        sb.prep_all()

def update_screen(game_objects, screen, play_button, sb, settings, stats):
    """Update images on the screen and redraw."""
    screen.fill(settings.bg_color)
    game_objects.draw(screen)
    sb.draw()

    if not stats.game_active:
        play_button.draw()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def fire_bullet(game_objects, screen, settings):
    """Fire a bullet if limit not reached yet."""
    if len(game_objects.bullets) < settings.bullets_allowed:
        new_bullet = Bullet(screen, settings, game_objects.ship)
        game_objects.bullets.add(new_bullet)

def delete_stale_bullets(bullets):
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def update_bullets(game_objects, sb, screen, settings, stats):
    """Update position of bullets and get rid of old bullets."""
    game_objects.bullets.update()
    delete_stale_bullets(game_objects.bullets)

    check_bullet_alien_collisions(game_objects, sb, screen, settings, stats)

def check_bullet_alien_collisions(game_objects, sb, screen, settings, stats):
    """Respond to bullet-alien collisions."""
    collisions = pygame.sprite.groupcollide(game_objects.bullets, game_objects.aliens, not settings.super_bullets, True)

    if collisions:
        total_points = 0
        for aliens in collisions.values():
            total_points += settings.alien_points * len(game_objects.aliens)
        sb.increment_score(total_points)

    if len(game_objects.aliens) == 0:
        game_objects.bullets.empty()
        settings.increase_speed()
        sb.increment_level()
        create_fleet(game_objects, screen, settings)

def update_aliens(game_objects, sb, screen, settings, stats):
    """
    Check if the fleet is at an edge,
     and then update the positions of all aliens in the fleet.
    """
    if check_fleet_edges(game_objects.aliens, settings):
        change_fleet_direction(game_objects.aliens, settings)
    game_objects.aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(game_objects.ship, game_objects.aliens):
        ship_hit(game_objects, sb, screen, settings, stats)

    if check_aliens_bottom(game_objects, screen, settings, stats):
        # Treat this the same as if the ship got hit.
        ship_hit(game_objects, sb, screen, settings, stats)

def get_number_aliens_x(alien_width, settings):
    """Determine the number of aliens that fit in a row."""
    available_space_x = settings.screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))

def get_number_rows(ship_height, alien_height, settings):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = settings.screen_height - 3 * alien_height - ship_height
    return int(available_space_y / (2 * alien_height))

def create_alien(aliens, alien_number, row_number, screen, settings):
    """Create an alien and place it in the row."""
    alien = Alien(screen, settings)
    alien.set_x(alien.width() + 2 * alien.width() * alien_number)
    alien.set_y(alien.height() + 2 * alien.height() * row_number)
    aliens.add(alien)

def create_fleet(game_objects, screen, settings):
    """Create a full fleet of aliens."""
    # Spacing between each alien is one alien width.
    alien = Alien(screen, settings)

    for row_number in range(get_number_rows(game_objects.ship.height(), alien.height(), settings)):
        for alien_number in range(get_number_aliens_x(alien.width(), settings)):
            create_alien(game_objects.aliens, alien_number, row_number, screen, settings)

def check_fleet_edges(aliens, settings):
    """Returns True if any aliens have reached an adge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            return True
    return False

def check_aliens_bottom(game_objects, screen, settings, stats):
    """Returns True if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in game_objects.aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            return True
    return False

def change_fleet_direction(aliens, settings):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.set_y(alien.y + settings.fleet_drop_speed)
    settings.fleet_direction *= -1

def reset_game(game_objects, screen, settings):
    game_objects.aliens.empty()
    game_objects.bullets.empty()

    create_fleet(game_objects, screen, settings)
    game_objects.ship.center()

def ship_hit(game_objects, sb, screen, settings, stats):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        sb.decrement_ships()
        reset_game(game_objects, screen, settings)
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def quit(stats):
    with open('high_score.txt', 'w') as high_score_file:
        high_score_file.write(str(stats.high_score) + '\n')
    sys.exit()
