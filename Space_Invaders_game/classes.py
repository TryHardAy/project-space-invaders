import pygame


class PersonShootingError(Exception):
    pass


class NegativeVelocityError(Exception):
    pass


class Object:
    def __init__(self, window, x_cord, y_cord, size):
        """
        Base to the rest of the object in this file
        """
        self._x_cord = x_cord
        self._y_cord = y_cord
        self._window = window
        self._size = size

    def draw(self, color):
        """
        Draws an Object on the screen
        """
        cord = (self._x_cord, self._y_cord, self._size, self._size)
        pygame.draw.rect(self._window, color, cord)

    def x_cord(self):
        return self._x_cord

    def y_cord(self):
        return self._y_cord

    def size(self):
        return self._size

    def window(self):
        return self._window


class GetShottedObject(Object):
    def get_shotted(self, bullet_cord: tuple):
        """
        Returns True when detects colision with a bullet
        """
        bullet_down_cord = bullet_cord[1] + 10
        if (
            self._x_cord <= bullet_cord[0] <= self._x_cord + self._size
            and (
                self._y_cord <= bullet_cord[1] <= self._y_cord + self._size
                or
                self._y_cord <= bullet_down_cord <= self._y_cord + self._size
            )
        ):
            return True
        else:
            return False


class MoveShootObject(GetShottedObject):
    def shoot(self, who_shoots, y_correction=0):
        """
        Shoot a bullet
        """
        bullet = Bullet(
            self._window,
            self._x_cord + self._size/2,
            self._y_cord + y_correction,
            who_shoots
        )
        return bullet

    def change_x_cord(self, velocity, left_wall=0, right_wall=0):
        """
        Changes place on screen in x line
        """
        if velocity == 0:
            return
        if (
            left_wall <= self._x_cord + velocity <=
            self._window.get_width() - self._size - right_wall
        ):
            self._x_cord += velocity


class Player(MoveShootObject):
    """
    Player class
    """
    def __init__(self, window, x_cord, y_cord, size):
        """
        Creates player
        """
        super().__init__(window, x_cord, y_cord, size)
        self._start_x_pos = x_cord
        self._lives = 3
        self._score = 0
        self._high_score = 0

    def lives(self):
        return self._lives

    def score(self):
        return self._score

    def high_score(self):
        return self._high_score

    def is_alive(self) -> bool:
        """
        Checks if player is still alive
        """
        return True if self._lives > 0 else False

    def reset_lives(self):
        """
        Resets lives
        """
        self._lives = 3

    def kill_player(self):
        """
        Sets player lives to 0
        """
        self._lives = 0

    def get_hit(self):
        """
        Takes 1 live from player
        """
        self._lives -= 1

    def draw(self, color):
        """
        Draw a player
        """
        super().draw(color)

    def change_x_cord(self, velocity):
        """
        Changes x cordinates of a player
        """
        return super().change_x_cord(velocity, 30, 30)

    def add_score(self, score):
        """
        Adds given score to the player score
        and changes high score if score is higher
        """
        self._score += score
        if self._score > self._high_score:
            self._high_score = self._score

    def reset_score(self):
        """
        Resets player score back to 0
        """
        self._score = 0

    def reset_position(self):
        """
        Place player to the strating position
        """
        self._x_cord = self._start_x_pos

    def shoot(self):
        """
        Shoots a bullet and returns it
        """
        return super().shoot('player')

    def import_high_score(self, path):
        """
        Imports high score from a file
        if file dont exist does nothing
        """
        try:
            with open(path, 'r') as handle:
                self._high_score = int(handle.readline())
        except FileNotFoundError:
            return

    def save_high_score(self, path):
        """
        Saves high score to the file
        """
        with open(path, 'w') as handle:
            handle.write(str(self._high_score))


class Enemy(MoveShootObject):
    def __init__(self, window, x_cord, y_cord, size, color, points):
        """
        Creates an Enemy
        """
        super().__init__(window, x_cord, y_cord, size)
        self._color = color
        self._points = points

    def color(self):
        return self._color

    def points(self):
        return self._points

    def draw(self):
        """
        Draws an Enemy
        """
        return super().draw(self._color)

    def shoot(self):
        """
        Shoot a bullet and returns it
        """
        return super().shoot('enemy', self._size)

    def change_y_cord(self, velocity):
        """
        Moves enemy down
        """
        if velocity == 0:
            return
        if (
            self._y_cord + velocity <=
            self._window.get_height() - 50
        ):
            self._y_cord += velocity


class Bullet(Object):
    def __init__(self, window, x_cord, y_cord, who_shoot):
        """
        Creates bullet
        """
        super().__init__(window, x_cord, y_cord, 2)
        if who_shoot == 'player':
            self._player = True
        elif who_shoot == 'enemy':
            self._player = False
        else:
            raise PersonShootingError('Incorrect person shooting data')

    def player(self):
        return self._player

    def change_y_cord(self, velocity):
        """
        Moves bullet
        """
        if velocity <= 0:
            raise NegativeVelocityError('Velocity has to be greater than 0')
        if self._player:
            self._y_cord -= velocity
        else:
            self._y_cord += velocity

    def cord(self):
        """
        Returns bullet cordinates as a tuple
        """
        return (self._x_cord, self._y_cord)

    def draw(self):
        """
        Draws bullet
        """
        red = (255, 0, 0)
        if self._player:
            second_cord = (self._x_cord, self._y_cord+10)
        else:
            second_cord = (self._x_cord, self._y_cord-10)
        pygame.draw.line(
            self._window,
            red,
            (self._x_cord, self._y_cord),
            second_cord,
            self._size
        )


class Baricade(GetShottedObject):
    def __init__(self, window, x_cord, y_cord, size):
        """
        Creates Baricade
        """
        super().__init__(window, x_cord, y_cord, size)
        self._health = 10

    def get_hit(self):
        """
        Takes 1 health from baricade
        """
        self._health -= 1

    def health(self):
        return self._health

    def is_destroyed(self) -> bool:
        """
        Returns True if Baricade is destroyed
        """
        return False if self._health > 0 else True
