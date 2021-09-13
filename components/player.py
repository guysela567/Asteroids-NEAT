from utils.constants import Constants
from utils.common import Common

from components.bullet import Bullet

from arcade import Sprite
import math


class Player():
    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y

        self.__sprite = Sprite(
            'assets/sprites/player.png',
            Constants.PLAYER_SPRITE_SCALE)

        self.__boosting = False
        self.__rotating = False

        self.__vel_x = 0
        self.__vel_y = 0

        self.__rotate_dir = 0
        self.__angle = math.pi * .5
        self.__turn_speed = Constants.PLAYER_TURN_SPEED

        self.__bullets = []
        self.__can_shoot = True
        self.__shoot_cooldown_dur = 0

    @property
    def sprite(self) -> Sprite:
        return self.__sprite

    def update(self, delta_time: float) -> None:
        # Rotation
        if self.__rotating:
            self.__set_rotation()

        # Boost
        if self.__boosting:
            self.__set_velocity()

        # Manage cooldowns
        if not self.__can_shoot:
            if self.__shoot_cooldown_dur < Constants.SHOOT_COOLDOWN:
                self.__shoot_cooldown_dur += delta_time
            else:
                self.__can_shoot = True
                self.__shoot_cooldown_dur = 0

        # Move player
        self.__x += self.__vel_x
        self.__y += self.__vel_y
        self.__handle_offscreen()

        # Update sprite position
        self.__sprite.center_x = self.__x
        self.__sprite.center_y = self.__y

        # Update bullets
        self.__update_bullets()

    @property
    def rotate_dir(self) -> int:
        return self.__rotate_dir

    @property
    def bullets(self) -> Bullet:
        return self.__bullets

    def __update_bullets(self) -> None:
        for bullet in reversed(self.__bullets):
            if bullet.deleted:  # Remove deleted bullets
                self.__bullets.remove(bullet)
            else:  # Update bullet if not deleted
                bullet.update()

    def shoot(self) -> None:
        if not self.__can_shoot:
            return

        x = self.__x + math.cos(self.__angle) * self.__sprite.height * .5
        y = self.__y + math.sin(self.__angle) * self.__sprite.height * .5

        self.__bullets.append(Bullet(x, y, self.__angle))
        self.__can_shoot = False

    def offscreen(self) -> bool:
        # return self.__sprite.
        pass

    def __set_rotation(self) -> None:
        self.__angle += self.__turn_speed * self.__rotate_dir
        self.__sprite.angle = math.degrees(self.__angle) - 90

    def __set_velocity(self) -> None:
        self.__vel_x = math.cos(self.__angle) * \
            Constants.PLAYER_BOOST_SPEED
        self.__vel_y = math.sin(self.__angle) * \
            Constants.PLAYER_BOOST_SPEED

    def start_boost(self) -> None:
        self.__boosting = True

    def stop_boost(self) -> None:
        self.__boosting = False
        self.__vel_x = 0
        self.__vel_y = 0

    def start_rotate(self, dir: int) -> None:
        self.__rotating = True
        self.__rotate_dir = dir

    def stop_rotate(self) -> None:
        self.__rotating = False
        self.__rotate_dir = 0

    def __handle_offscreen(self) -> bool:
        self.__x, self.__y = Common.handle_offscreen(
            self.__x, self.__y, self.__sprite)
