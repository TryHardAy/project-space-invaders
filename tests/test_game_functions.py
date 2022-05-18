import pytest
from Space_Invaders_game.game_functions import VelocityError
from Space_Invaders_game.game_functions import (
    cooldown_minus_one,
    create_baricades,
    bullet_hit_baricade_check,
    create_enemies,
    bullet_reach_enemy_check,
    enemies_move_down,
    enemies_move_sides,
    is_any_enemy_near_wall,
    enemy_colision_with_objects,
    move_bullets,
    bullet_reach_player_check
)
from Space_Invaders_game.classes import Bullet, Player


class Window:
    def __init__(self, size):
        self.size = size

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]


def test_cooldown_minus_one():
    cooldown = 60
    cooldown = cooldown_minus_one(cooldown)
    assert cooldown == 59


def test_cooldown_minus_one_zero():
    cooldown = 0
    cooldown = cooldown_minus_one(cooldown)
    assert cooldown == 0


def test_cooldown_minus_one_negative():
    cooldown = -10
    cooldown = cooldown_minus_one(cooldown)
    assert cooldown == 0


def test_create_baricades():
    window = Window((700, 500))
    baricades = create_baricades(window)
    assert len(baricades) == 4
    assert baricades[0].window() == window
    assert baricades[0].x_cord() == 120
    assert baricades[0].y_cord() == 350
    assert baricades[0].size() == 40
    assert baricades[0].health() == 10

    assert baricades[1].window() == window
    assert baricades[1].x_cord() == 260
    assert baricades[1].y_cord() == 350
    assert baricades[1].size() == 40
    assert baricades[1].health() == 10

    assert baricades[2].window() == window
    assert baricades[2].x_cord() == 400
    assert baricades[2].y_cord() == 350
    assert baricades[2].size() == 40
    assert baricades[2].health() == 10

    assert baricades[3].window() == window
    assert baricades[3].x_cord() == 540
    assert baricades[3].y_cord() == 350
    assert baricades[3].size() == 40
    assert baricades[3].health() == 10


def test_bullet_hit_baricade_check_enemy():
    window = Window((700, 500))
    baricades = create_baricades(window)
    bullets = [Bullet(window, 100, 50, 'enemy'), Bullet(window, 550, 360, 'enemy')]
    bullet_hit_baricade_check(baricades, bullets)
    assert len(bullets) == 1
    assert baricades[0].health() == 10
    assert baricades[1].health() == 10
    assert baricades[2].health() == 10
    assert baricades[3].health() == 9


def test_bullet_hit_baricade_check_player():
    window = Window((700, 500))
    baricades = create_baricades(window)
    bullets = [Bullet(window, 200, 100, 'player'), Bullet(window, 410, 370, 'player')]
    bullet_hit_baricade_check(baricades, bullets)
    assert len(bullets) == 1
    assert baricades[0].health() == 10
    assert baricades[1].health() == 10
    assert baricades[2].health() == 9
    assert baricades[3].health() == 10


def test_create_enemies():
    window = Window((700, 500))
    enemies = create_enemies(window)
    assert len(enemies) == 50

    assert enemies[0].window() == window
    assert enemies[0].x_cord() == 65
    assert enemies[0].y_cord() == 50
    assert enemies[0].color() == (255, 0, 255)
    assert enemies[0].points() == 30

    assert enemies[10].window() == window
    assert enemies[10].x_cord() == 65
    assert enemies[10].y_cord() == 100
    assert enemies[10].color() == (0, 255, 255)
    assert enemies[10].points() == 20

    assert enemies[20].window() == window
    assert enemies[20].x_cord() == 65
    assert enemies[20].y_cord() == 150
    assert enemies[20].color() == (0, 255, 255)
    assert enemies[20].points() == 20

    assert enemies[30].window() == window
    assert enemies[30].x_cord() == 65
    assert enemies[30].y_cord() == 200
    assert enemies[30].color() == (255, 255, 0)
    assert enemies[30].points() == 10

    assert enemies[39].window() == window
    assert enemies[39].x_cord() == 605
    assert enemies[39].y_cord() == 200
    assert enemies[39].color() == (255, 255, 0)
    assert enemies[39].points() == 10

    assert enemies[40].window() == window
    assert enemies[40].x_cord() == 65
    assert enemies[40].y_cord() == 250
    assert enemies[40].color() == (255, 255, 0)
    assert enemies[40].points() == 10

    assert enemies[45].window() == window
    assert enemies[45].x_cord() == 365
    assert enemies[45].y_cord() == 250
    assert enemies[45].color() == (255, 255, 0)
    assert enemies[45].points() == 10

    assert enemies[49].window() == window
    assert enemies[49].x_cord() == 605
    assert enemies[49].y_cord() == 250
    assert enemies[49].color() == (255, 255, 0)
    assert enemies[49].points() == 10


def test_bullet_reach_enemy_check():
    window = Window((700, 500))
    enemies = create_enemies(window)
    player = Player(window, 500, 400, 40)
    bullets = [Bullet(window, 80, 260, 'player'), Bullet(window, 500, 500, 'player')]
    bullet_reach_enemy_check(bullets, enemies, player)
    assert len(bullets) == 1
    assert len(enemies) == 49
    assert player.score() == 10


def test_enemies_move_sides_left():
    window = Window((700, 500))
    enemies = create_enemies(window)
    x_cord = []
    for enemy in enemies:
        x_cord.append(enemy.x_cord())
    enemies_move_sides(20, enemies, 'left')
    pos = 0
    for enemy in enemies:
        assert enemy.x_cord() == x_cord[pos] - 20
        pos += 1


def test_enemies_move_sides_rigth():
    window = Window((700, 500))
    enemies = create_enemies(window)
    x_cord = []
    for enemy in enemies:
        x_cord.append(enemy.x_cord())
    enemies_move_sides(20, enemies, 'right')
    pos = 0
    for enemy in enemies:
        assert enemy.x_cord() == x_cord[pos] + 20
        pos += 1


def test_enemies_move_down():
    window = Window((700, 500))
    enemies = create_enemies(window)
    y_cord = []
    for enemy in enemies:
        y_cord.append(enemy.y_cord())
    enemies_move_down(20, enemies)
    pos = 0
    for enemy in enemies:
        assert enemy.y_cord() == y_cord[pos] + 20
        pos += 1


def test_enemies_move_down_velocityError():
    window = Window((700, 500))
    enemies = create_enemies(window)
    with pytest.raises(VelocityError):
        enemies_move_down(-20, enemies)


def test_is_any_enemy_near_wall_left_True():
    window = Window((700, 500))
    enemies = create_enemies(window)
    enemies_move_sides(50, enemies, 'left')
    assert is_any_enemy_near_wall(enemies)


def test_is_any_enemy_near_wall_right_True():
    window = Window((700, 500))
    enemies = create_enemies(window)
    enemies_move_sides(60, enemies, 'right')
    assert is_any_enemy_near_wall(enemies)


def test_is_any_enemy_near_wall_False():
    window = Window((700, 500))
    enemies = create_enemies(window)
    enemies_move_sides(30, enemies, 'left')
    assert not is_any_enemy_near_wall(enemies)


def test_enemy_colision_with_objects_True():
    window = Window((700, 500))
    enemies = create_enemies(window)
    player = Player(window, 80, 160, 30)
    assert enemy_colision_with_objects(enemies, player)


def test_enemy_colision_with_objects_False():
    window = Window((700, 500))
    enemies = create_enemies(window)
    player = Player(window, 600, 400, 30)
    assert not enemy_colision_with_objects(enemies, player)


def test_move_bullets_player():
    window = Window((700, 500))
    bullets = [Bullet(window, 80, 260, 'player'), Bullet(window, 300, 300, 'player')]
    move_bullets(window, bullets)
    assert bullets[0].y_cord() == 255
    assert bullets[1].y_cord() == 295


def test_move_bullets_enemy():
    window = Window((700, 500))
    bullets = [Bullet(window, 80, 100, 'enemy'), Bullet(window, 300, 200, 'enemy')]
    move_bullets(window, bullets)
    assert bullets[0].y_cord() == 105
    assert bullets[1].y_cord() == 205


def test_move_bullets_out_of_range():
    window = Window((700, 500))
    bullets = [Bullet(window, 80, -5, 'player'), Bullet(window, 300, 100, 'player')]
    move_bullets(window, bullets)
    assert len(bullets) == 1
    assert bullets[0].y_cord() == 95


def test_move_bullets_out_of_range_too_high():
    window = Window((700, 500))
    bullets = [Bullet(window, 80, 100, 'enemy'), Bullet(window, 300, 800, 'enemy')]
    move_bullets(window, bullets)
    assert len(bullets) == 1
    assert bullets[0].y_cord() == 105


def test_bullet_reach_player_check():
    window = Window((700, 500))
    bullets = [Bullet(window, 80, 100, 'enemy'), Bullet(window, 300, 300, 'enemy')]
    player = Player(window, 70, 105, 30)
    bullet_reach_player_check(bullets, player)
    assert len(bullets) == 1
    assert player.lives() == 2


def test_bullet_reach_player_check_double_hit():
    window = Window((700, 500))
    bullets = [Bullet(window, 80, 100, 'enemy'), Bullet(window, 110, 95, 'enemy')]
    player = Player(window, 80, 100, 30)
    bullet_reach_player_check(bullets, player)
    assert not bullets
    assert player.lives() == 1
