from Space_Invaders_game.classes import Enemy, Baricade
from random import randint


class VelocityError(Exception):
    pass


def cooldown_minus_one(cooldown):
    """
    Make cooldown go down
    """
    if cooldown > 0:
        cooldown -= 1
    elif cooldown < 0:
        cooldown = 0
    return cooldown


def draw_enemies(enemies):
    """
    Draws enemies on the screen
    """
    if not enemies:
        return
    for enemy in enemies:
        enemy.draw()


def create_baricades(window):
    """
    Creates 4 baricades
    """
    baricades = []
    w_width = window.get_width()
    w_height = window.get_height()
    size = 40
    for num in range(1, 5):
        baricade = Baricade(
            window,
            w_width // 5 * num - size / 2,
            w_height - 150,
            size
        )
        baricades.append(baricade)
    return baricades


def bullet_hit_baricade_check(baricades, bullets):
    """
    Check if bullet hit baricade
    """
    for baricade in baricades:
        for bullet in bullets:
            if baricade.get_shotted(bullet.cord()):
                baricade.get_hit()
                bullets.remove(bullet)


def draw_baricades(baricades, color):
    """
    Draws baricades
    """
    if not baricades:
        return
    for baricade in baricades:
        baricade.draw(color)


def create_enemies(window):
    """
    Creates enemies
    """
    pink = (255, 0, 255)
    light_blue = (0, 255, 255)
    yellow = (255, 255, 0)
    enemies = []
    xcord = 65
    ycord = 50
    for row in range(5):
        for column in range(10):
            if row == 0:
                color = pink
                points = 30
            elif row in (1, 2):
                color = light_blue
                points = 20
            else:
                color = yellow
                points = 10
            enemy = Enemy(window, xcord+column*60, ycord, 30, color, points)
            enemies.append(enemy)
        ycord += 50
    return enemies


def bullet_reach_enemy_check(bullets, enemies, player):
    """
    Checks if a bullet hit an Enemy
    """
    enemies_bullets_to_remove = []
    for enemy in enemies:
        for bullet in bullets:
            if enemy.get_shotted(bullet.cord()):
                player.add_score(enemy.points())
                enemies_bullets_to_remove.append((enemy, bullet))
    for enemy, bullet in enemies_bullets_to_remove:
        enemies.remove(enemy)
        bullets.remove(bullet)


def enemies_move_sides(velocity, enemies, enemy_move_side):
    """
    Makes Enemy move left and right
    """
    for enemy in enemies:
        if enemy_move_side == 'left':
            enemy.change_x_cord(-velocity)
        else:
            enemy.change_x_cord(velocity)


def enemies_move_down(velocity, enemies):
    """
    Makes Enemy move down
    """
    if velocity < 1:
        raise VelocityError('Velocity value cannot be lower than 1')
    for enemy in enemies:
        enemy.change_y_cord(velocity)


def is_any_enemy_near_wall(enemies):
    """
    Checks if Enemy is near the wall
    """
    for enemy in enemies:
        if enemy.x_cord() <= 20 or enemy.x_cord() >= 650:
            return True
    return False


def enemies_random_shooting(enemies):
    """
    Shoots bullets randomly
    """
    bullets = []
    for enemy in enemies:
        if randint(0, len(enemies) * 50) == 0:
            bullets.append(enemy.shoot())
    return bullets


def enemy_colision_with_objects(enemies, object):
    """
    Checks if Enemy colide with player or baricade
    """
    x_p_cord = object.x_cord()
    y_p_cord = object.y_cord()
    p_size = object.size()
    for enemy in enemies:
        e_size = enemy.size()
        if (
            (
                x_p_cord <= enemy.x_cord() <= x_p_cord + p_size
                and y_p_cord <= enemy.y_cord() <= y_p_cord + p_size
            )
            or (
                x_p_cord <= enemy.x_cord() + e_size <= x_p_cord + p_size
                and y_p_cord <= enemy.y_cord() + e_size <= y_p_cord + p_size
            )
            or (
                x_p_cord <= enemy.x_cord() + e_size <= x_p_cord + p_size
                and y_p_cord <= enemy.y_cord() <= y_p_cord + p_size
            )
            or (
                x_p_cord <= enemy.x_cord() <= x_p_cord + p_size
                and y_p_cord <= enemy.y_cord() + e_size <= y_p_cord + p_size
            )
        ):
            return True
    return False


def move_bullets(window, bullets):
    """
    Moves bullet on the map
    """
    bullets_to_remove = []
    for bullet in bullets:
        if 0 < bullet.y_cord() < window.get_height():
            bullet.change_y_cord(5)
        else:
            bullets_to_remove.append(bullet)
    for bullet in bullets_to_remove:
        bullets.remove(bullet)


def bullet_reach_player_check(bullets, player):
    """
    Checks if bullet reach player
    """
    bullets_to_remove = []
    for bullet in bullets:
        if player.get_shotted(bullet.cord()):
            player.get_hit()
            bullets_to_remove.append(bullet)
    for bullet in bullets_to_remove:
        bullets.remove(bullet)


def draw_bullets(bullets):
    """
    Draws bullets
    """
    for bullet in bullets:
        bullet.draw()


def enemy_movement(enemies, velocity, move_side, moved_down):
    """
    Decides about Enemy movement
    """
    if is_any_enemy_near_wall(enemies) and not moved_down:
        enemies_move_down(velocity // 2, enemies)
        move_side = (
            'right'
            if move_side == 'left'
            else 'left'
        )
        moved_down = True
    else:
        enemies_move_sides(velocity, enemies, move_side)
        moved_down = False
    return move_side, moved_down
