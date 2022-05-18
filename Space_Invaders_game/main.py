import sys
sys.path.append('../project-space-invaders')
import pygame
import time
from classes import Player
from game_functions import (
    bullet_hit_baricade_check,
    bullet_reach_player_check,
    create_baricades,
    create_enemies,
    draw_baricades,
    draw_bullets,
    draw_enemies,
    bullet_reach_enemy_check,
    enemy_movement,
    cooldown_minus_one,
    enemies_random_shooting,
    enemy_colision_with_objects,
    move_bullets
)


def show_high_score(window, player, font, color):
    """
    Shows Player high score
    """
    HIGH_SCORE_text = font.render(
        f'HIGH SCORE: {player.high_score()}',
        True, color)
    window.blit(HIGH_SCORE_text, (window.get_width()/2, 0))


def game_won_lost_window(window, color, winner):
    """
    Show result of the game
    """
    black = (0, 0, 0)
    window.fill(black)
    font = pygame.font.SysFont('TEXT', 200)
    text = 'WON' if winner == 'player' else 'LOST'
    GAME_text = font.render("GAME", True, color)
    result_text = font.render(text, True, color)
    GAME_text_size = ((window.get_width() - GAME_text.get_width()) / 2, 100)
    result_text_size = (
        (window.get_width() - result_text.get_width()) / 2,
        100 + GAME_text.get_height()
    )
    window.blit(GAME_text, GAME_text_size)
    window.blit(result_text, result_text_size)
    pygame.display.update()
    time.sleep(3)
    window.fill(black)


def game_window(window, player):
    """
    Game window
    """
    green = (0, 255, 0)
    red = (255, 0, 0)

    player_velocity = 3
    enemy_velocity = 20
    player_shooting_cooldown = 0
    player_bullets = []
    enemy_bullets = []
    enemy_move_side = 'left'
    enemy_move_cooldown = 50
    enemies_moved_down = False
    enemies = create_enemies(window)
    baricades = create_baricades(window)

    lives_font = pygame.font.SysFont('TEXT', 50)
    score_font = pygame.font.SysFont('TEXT', 40)

    def re_draw_game_window():
        """
        Refresh data showed at window
        """
        blue = (0, 0, 255)
        white = (255, 255, 255)
        black = (0, 0, 0)
        window.fill(black)

        # Draws player lives
        LIVES_text = lives_font.render(f'LIVES: {player.lives()}', True, green)
        LIVES_text_height = lives_font.get_height()
        window.blit(LIVES_text, (0, window.get_height() - LIVES_text_height))

        # Draws player score
        SCORE_text = score_font.render(f'SCORE: {player.score()}', True, green)
        window.blit(SCORE_text, (0, 0))

        # Draws player high score
        show_high_score(window, player, score_font, green)

        # Draws player
        player.draw(white)

        # Draws enemies
        draw_enemies(enemies)

        # Draws bullets
        if player_bullets:
            draw_bullets(player_bullets)
        if enemy_bullets:
            draw_bullets(enemy_bullets)

        # Draw baricades
        draw_baricades(baricades, blue)

    while True:
        # clock
        clock = pygame.time.Clock()
        clock.tick(60)

        re_draw_game_window()

        # Player shooting cooldown
        player_shooting_cooldown = cooldown_minus_one(player_shooting_cooldown)

        # Enemy movement cooldown
        enemy_move_cooldown = cooldown_minus_one(enemy_move_cooldown)

        # Quits game when 'X' is selected
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if player_bullets:
            # Checks if a player_bullets are on the map and moves them
            move_bullets(window, player_bullets)

            # Checks if bullet shot enemy
            bullet_reach_enemy_check(player_bullets, enemies, player)

            # Checks if player_bullet hits baricade
            bullet_hit_baricade_check(baricades, player_bullets)

        if enemy_bullets:
            # Moves enemy_bulletes
            move_bullets(window, enemy_bullets)

            # Checks if a bullet reach a player
            bullet_reach_player_check(enemy_bullets, player)

            # Checks if enemy_bullet hits baricade
            bullet_hit_baricade_check(baricades, enemy_bullets)

        if baricades:
            # Checks if baricade is destroyed
            for baricade in baricades:
                if baricade.is_destroyed():
                    baricades.remove(baricade)

        # Allows player to move
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.change_x_cord(-player_velocity)
        if keys[pygame.K_d]:
            player.change_x_cord(player_velocity)

        # Allows player to shoot
        if keys[pygame.K_SPACE] and player_shooting_cooldown == 0:
            player_bullets.append(player.shoot())
            player_shooting_cooldown = 45

        # Allows enemy to move
        if enemies and enemy_move_cooldown == 0:
            enemy_move_side, enemies_moved_down = enemy_movement(
                enemies,
                enemy_velocity,
                enemy_move_side,
                enemies_moved_down
            )
            enemy_move_cooldown = len(enemies)

        # Allows enemy to shoot
        if enemies:
            bullets = enemies_random_shooting(enemies)
            enemy_bullets += bullets

            # Kills player if he touched an enemy
            if enemy_colision_with_objects(enemies, player):
                player.kill_player()

            # Destroys barier if it colide with an enemy
            if baricades:
                for baricade in baricades:
                    if enemy_colision_with_objects(enemies, baricade):
                        baricades.remove(baricade)

            # Kills player when enemy escapes map
            for enemy in enemies:
                if enemy.y_cord() >= window.get_height() - 50:
                    player.kill_player()

        # Player Won when he kills all enemies
        if not enemies:
            game_won_lost_window(window, green, 'player')
            break
        # Enemies wons when player dies
        if not player.is_alive():
            game_won_lost_window(window, red, 'enemy')
            break

        pygame.display.update()


def main():
    """
    Game main manu window
    """
    width = 700
    height = 500
    pygame.init()
    green = (0, 255, 0)
    white = (255, 255, 255)
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Space Invaders")

    # Decides about buttons coordinates and render thems
    font = pygame.font.SysFont('TEXT', 40)
    START_text = font.render('Start', True, green, white)
    EXIT_text = font.render('Exit', True, green, white)
    Start_size = font.size("Start")
    Exit_size = font.size("Exit")
    Start_cord = (width/2 - Start_size[0]/2, height/2 - Start_size[1] - 5)
    Exit_cord = (width/2 - Exit_size[0]/2, height/2 + 5)

    # Creates player
    player = Player(window, 330, 430, 30)
    player.import_high_score('Space_Invaders_game/high_score.txt')

    def event_check():
        """
        Checks if any important event happends
        """
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()

            # If player exit, game will close
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Quits when player click EXIT
                if (
                    Exit_cord[0] <= mouse[0] <= width/2 + Exit_size[0]/2
                    and Exit_cord[1] <= mouse[1] <= height/2 + 5 + Exit_size[1]
                ):
                    pygame.quit()

                # Starts game when player click START
                if (
                    Start_cord[0] <= mouse[0] <= width/2 + Start_size[0]/2
                    and Start_cord[1] <= mouse[1] <=
                    height/2 - 5 + Start_size[1]
                ):
                    player.reset_lives()
                    player.reset_score()
                    game_window(window, player)
                    player.reset_position()
                    player.save_high_score(
                        'Space_Invaders_game/high_score.txt'
                    )

    while True:
        # clock
        clock = pygame.time.Clock()
        clock.tick(60)

        event_check()

        green = (0, 255, 0)
        show_high_score(window, player, font, green)

        # Shows START and EXIT buttons on screen
        window.blit(START_text, Start_cord)   # (64,27)
        window.blit(EXIT_text, Exit_cord)    # (54,27)

        pygame.display.update()


if __name__ == "__main__":
    main()
