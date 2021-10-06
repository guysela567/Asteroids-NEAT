from utils.vector import PositionalVector, DirectionalVector
from utils.constants import Constants
from utils.sprite import Sprite
from utils.geometry.raycasting import RaySet

from components.projectile import Projectile

import math


class Player():
    def __init__(self, x, y) -> None:
        self.__pos = PositionalVector(x, y)

        self.__sprite = Sprite(
            'assets/sprites/player.png',
            Constants.PLAYER_SPRITE_SCALE,
            self.__pos)

        self.__boosting = False
        self.__rotating = False

        self.__rotate_dir = 0
        self.__angle = math.pi * .5
        self.__turn_speed = Constants.PLAYER_TURN_SPEED

        self.__vel = DirectionalVector(0, self.__angle)

        self.__projectiles = []
        self.__can_shoot = True
        self.__shoot_cooldown_dur = 0

        # AI
        self.__ray_set = RaySet(self.__pos, 10)

        # TODO Add teleportation mechanics (cut candidate)

    @property
    def sprite(self) -> Sprite:
        return self.__sprite

    @property
    def can_shoot(self) -> bool:
        return self.__can_shoot

    def update(self, delta_time: float) -> None:
        # Rotation
        if self.__rotating:
            self.__set_rotation()

        # Boost
        if self.__boosting:
            self.__boost()
        else:
            self.__slow_down()

        # Manage cooldowns
        if not self.__can_shoot:
            if self.__shoot_cooldown_dur < Constants.SHOOT_COOLDOWN:
                self.__shoot_cooldown_dur += delta_time
            else:
                self.__can_shoot = True
                self.__shoot_cooldown_dur = 0

        # Move player
        self.__pos += self.__vel
        self.__pos.handle_offscreen(self.__sprite)

        # Update sprite position
        self.__sprite.pos = self.__pos

        # Update projectiles
        self.__update_projectiles()

        # Update ray set position
        self.__ray_set.pos = self.__pos

    @property
    def rotate_dir(self) -> int:
        return self.__rotate_dir

    @property
    def projectiles(self) -> Projectile:
        return self.__projectiles

    def __update_projectiles(self) -> None:
        for projectile in reversed(self.__projectiles):
            if projectile.deleted:  # Remove deleted projectiles
                self.__projectiles.remove(projectile)
            else:  # Update projectile if not deleted
                projectile.update()

    def shoot(self) -> None:
        if not self.__can_shoot:
            return

        x = self.__pos.x - math.cos(self.__angle) * self.__sprite.height * .5
        y = self.__pos.y - math.sin(self.__angle) * self.__sprite.height * .5

        self.__projectiles.append(Projectile(x, y, self.__angle))
        self.__can_shoot = False

        # Apply knockback force
        if not self.__boosting:
            self.__vel.angle = self.__angle
            self.__vel.mag += Constants.PLAYER_SHOOT_KNOCKBACK

    def __set_rotation(self) -> None:
        self.__angle += self.__turn_speed * self.__rotate_dir
        self.__sprite.angle = math.degrees(self.__angle) - 90

    def __boost(self) -> None:
        self.__vel.angle = self.__angle
        self.__vel.lerp_mag(-Constants.PLAYER_BOOST_SPEED,
                            Constants.PLAYER_AIR_FRICTION)

    def __slow_down(self) -> None:
        self.__vel.lerp_mag(0, Constants.PLAYER_AIR_FRICTION)

    def start_boost(self) -> None:
        self.__boosting = True

    def stop_boost(self) -> None:
        self.__boosting = False

    def start_rotate(self, dir: int) -> None:
        self.__rotating = True
        self.__rotate_dir = dir

    def stop_rotate(self) -> None:
        self.__rotating = False
        self.__rotate_dir = 0

    @property
    def ray_set(self) -> RaySet:
        return self.__ray_set