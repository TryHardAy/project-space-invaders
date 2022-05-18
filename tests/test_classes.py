import pytest
from Space_Invaders_game.classes import (
    Baricade,
    Bullet,
    Enemy,
    MoveShootObject,
    NegativeVelocityError,
    Object,
    GetShottedObject,
    PersonShootingError,
    Player
)


class Window:
    def __init__(self, size):
        self.size = size

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]


def test_Object_create():
    window = Window((700, 500))
    test_object = Object(window, 50, 70, 40)
    assert test_object.x_cord() == 50
    assert test_object.y_cord() == 70
    assert test_object.size() == 40
    assert test_object.window() == window


def test_GetShottedObject_True():
    window = Window((700, 500))
    test_object = GetShottedObject(window, 50, 70, 40)
    assert test_object.get_shotted((55, 75))


def test_GetShottedObject_False():
    window = Window((700, 500))
    test_object = GetShottedObject(window, 50, 70, 40)
    assert not test_object.get_shotted((200, 300))


def test_MoveShootObject_shoot_PLayer():
    window = Window((700, 500))
    test_object = MoveShootObject(window, 50, 70, 40)
    bullet = test_object.shoot('player')
    assert bullet.window() == window
    assert bullet.x_cord() == 70
    assert bullet.y_cord() == 70
    assert bullet.player()


def test_MoveShootObject_shoot_Enemy():
    window = Window((700, 500))
    test_object = MoveShootObject(window, 200, 150, 40)
    bullet = test_object.shoot('enemy', test_object.size())
    assert bullet.window() == window
    assert bullet.x_cord() == 220
    assert bullet.y_cord() == 190
    assert not bullet.player()


def test_MoveShootObject_change_x_cord_typical():
    window = Window((700, 500))
    test_object = MoveShootObject(window, 200, 150, 40)
    test_object.change_x_cord(30, 30, 30)
    assert test_object.x_cord() == 230


def test_MoveShootObject_change_x_cord_negative_velocity():
    window = Window((700, 500))
    test_object = MoveShootObject(window, 200, 150, 40)
    test_object.change_x_cord(-30, 30, 30)
    assert test_object.x_cord() == 170


def test_MoveShootObject_change_x_cord_zero_velocity():
    window = Window((700, 500))
    test_object = MoveShootObject(window, 200, 150, 40)
    test_object.change_x_cord(0, 30, 30)
    assert test_object.x_cord() == 200


def test_MoveShootObject_change_x_cord_out_of_range():
    window = Window((700, 500))
    test_object = MoveShootObject(window, 10, 150, 40)
    test_object.change_x_cord(-30)
    assert test_object.x_cord() == 10


def test_MoveShootObject_change_x_cord_out_of_range_right_wall():
    window = Window((700, 500))
    test_object = MoveShootObject(window, 690, 150, 40)
    test_object.change_x_cord(30)
    assert test_object.x_cord() == 690


def test_Player_create():
    window = Window((700, 500))
    player = Player(window, 50, 70, 40)
    assert player.x_cord() == 50
    assert player.y_cord() == 70
    assert player.size() == 40
    assert player.lives() == 3
    assert player.score() == 0
    assert player.high_score() == 0


def test_Player_is_alive():
    window = Window((700, 500))
    player = Player(window, 50, 70, 40)
    assert player.lives() == 3
    assert player.is_alive()
    player.kill_player()
    assert player.lives() == 0
    assert not player.is_alive()


def test_Player_reset_lives():
    window = Window((700, 500))
    player = Player(window, 50, 70, 40)
    player.kill_player()
    assert player.lives() == 0
    player.reset_lives()
    assert player.lives() == 3


def test_Player_kill_player():
    window = Window((700, 500))
    player = Player(window, 50, 70, 40)
    assert player.lives() == 3
    player.kill_player()
    assert player.lives() == 0


def test_Player_get_hit():
    window = Window((700, 500))
    player = Player(window, 50, 70, 40)
    assert player.lives() == 3
    player.get_hit()
    assert player.lives() == 2


def test_Player_change_x_cord():
    window = Window((700, 500))
    player = Player(window, 50, 70, 40)
    assert player.x_cord() == 50
    player.change_x_cord(50)
    assert player.x_cord() == 100


def test_Player_change_x_cord_negative_velocity():
    window = Window((700, 500))
    player = Player(window, 200, 70, 40)
    assert player.x_cord() == 200
    player.change_x_cord(-50)
    assert player.x_cord() == 150


def test_Player_add_score_typical():
    window = Window((700, 500))
    player = Player(window, 200, 70, 40)
    assert player.score() == 0
    assert player.high_score() == 0
    player.add_score(100)
    assert player.score() == 100
    assert player.high_score() == 100


def test_Player_add_score():
    window = Window((700, 500))
    player = Player(window, 200, 70, 40)
    assert player.score() == 0
    assert player.high_score() == 0
    player.add_score(100)
    assert player.score() == 100
    assert player.high_score() == 100
    player.reset_score()
    player.add_score(50)
    assert player.score() == 50
    assert player.high_score() == 100


def test_Player_reset_score():
    window = Window((700, 500))
    player = Player(window, 200, 70, 40)
    assert player.score() == 0
    assert player.high_score() == 0
    player.add_score(100)
    assert player.score() == 100
    assert player.high_score() == 100
    player.reset_score()
    assert player.score() == 0
    assert player.high_score() == 100


def test_Player_reset_position():
    window = Window((700, 500))
    player = Player(window, 200, 70, 40)
    player.change_x_cord(-50)
    assert player.x_cord() == 150
    player.reset_position()
    assert player.x_cord() == 200


def test_Player_shoot():
    window = Window((700, 500))
    player = Player(window, 200, 70, 40)
    bullet = player.shoot()
    assert bullet.window() == window
    assert bullet.x_cord() == 220
    assert bullet.y_cord() == 70
    assert bullet.player()


def test_Enemy_create():
    window = Window((700, 500))
    enemy = Enemy(window, 100, 300, 40, (255, 0, 255), 30)
    assert enemy.x_cord() == 100
    assert enemy.y_cord() == 300
    assert enemy.size() == 40
    assert enemy.window() == window
    assert enemy.color() == (255, 0, 255)
    assert enemy.points() == 30


def test_Enemy_shoot():
    window = Window((700, 500))
    enemy = Enemy(window, 100, 300, 40, (255, 0, 255), 30)
    bullet = enemy.shoot()
    assert bullet.window() == window
    assert bullet.x_cord() == 120
    assert bullet.y_cord() == 340
    assert not bullet.player()


def test_Enemy_change_y_cord():
    window = Window((700, 500))
    enemy = Enemy(window, 100, 300, 40, (255, 0, 255), 30)
    assert enemy.y_cord() == 300
    enemy.change_y_cord(50)
    assert enemy.y_cord() == 350


def test_Enemy_change_y_cord_negative_velocity():
    window = Window((700, 500))
    enemy = Enemy(window, 100, 300, 40, (255, 0, 255), 30)
    assert enemy.y_cord() == 300
    enemy.change_y_cord(-50)
    assert enemy.y_cord() == 250


def test_Enemy_change_y_cord_zero_velocity():
    window = Window((700, 500))
    enemy = Enemy(window, 100, 300, 40, (255, 0, 255), 30)
    assert enemy.y_cord() == 300
    enemy.change_y_cord(0)
    assert enemy.y_cord() == 300


def test_Bullet_create_player():
    window = Window((700, 500))
    bullet = Bullet(window, 200, 400, 'player')
    assert bullet.x_cord() == 200
    assert bullet.y_cord() == 400
    assert bullet.size() == 2
    assert bullet.window() == window
    assert bullet.player()


def test_Bullet_create_enemy():
    window = Window((700, 500))
    bullet = Bullet(window, 200, 400, 'enemy')
    assert bullet.x_cord() == 200
    assert bullet.y_cord() == 400
    assert bullet.size() == 2
    assert bullet.window() == window
    assert not bullet.player()


def test_Bullet_create_wrong_person_shooting():
    window = Window((700, 500))
    with pytest.raises(PersonShootingError):
        Bullet(window, 200, 400, 'friend')


def test_Bullet_change_y_cord_player():
    window = Window((700, 500))
    bullet = Bullet(window, 200, 400, 'player')
    assert bullet.y_cord() == 400
    bullet.change_y_cord(40)
    assert bullet.y_cord() == 360


def test_Bullet_change_y_cord_enemy():
    window = Window((700, 500))
    bullet = Bullet(window, 200, 400, 'enemy')
    assert bullet.y_cord() == 400
    bullet.change_y_cord(40)
    assert bullet.y_cord() == 440


def test_Bullet_change_y_cord_VelocityError():
    window = Window((700, 500))
    bullet = Bullet(window, 200, 400, 'enemy')
    with pytest.raises(NegativeVelocityError):
        bullet.change_y_cord(0)


def test_Bullet_cord():
    window = Window((700, 500))
    bullet = Bullet(window, 200, 400, 'player')
    assert bullet.cord() == (200, 400)


def test_Baricade_create():
    window = Window((700, 500))
    baricade = Baricade(window, 400, 50, 50)
    assert baricade.window() == window
    assert baricade.x_cord() == 400
    assert baricade.y_cord() == 50
    assert baricade.size() == 50
    assert baricade.health() == 10


def test_Baricade_get_hit():
    window = Window((700, 500))
    baricade = Baricade(window, 400, 50, 50)
    assert baricade.health() == 10
    baricade.get_hit()
    assert baricade.health() == 9


def test_Baricade_is_destroyed_typical():
    window = Window((700, 500))
    baricade = Baricade(window, 400, 50, 50)
    assert baricade.health() == 10
    assert not baricade.is_destroyed()
    baricade.get_hit()
    assert baricade.health() == 9
    assert not baricade.is_destroyed()


def test_Baricade_is_destroyed():
    window = Window((700, 500))
    baricade = Baricade(window, 400, 50, 50)
    assert baricade.health() == 10
    assert not baricade.is_destroyed()
    for x in range(10):
        baricade.get_hit()
    assert baricade.health() == 0
    assert baricade.is_destroyed()
