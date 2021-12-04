from __future__ import annotations

from utils.vector import PositionalVector, DirectionalVector
from utils.constants import Constants
from utils.geometry.collision import Hitbox, SpriteDimensions
from utils.geometry.raycasting import RaySet

from components.projectile import Projectile

import math


class Player():
    def __init__(self, x, y) -> None:
        self.__pos = PositionalVector(x, y)

        self.__hitbox = Hitbox(self.__pos, 'player', Constants.PLAYER_SPRITE_SCALE)

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
        self.__ray_set = RaySet(self.__pos, self.__angle, Constants.RAY_AMOUNT)

    def update(self, delta_time: float) -> None:
        # Rotation
        if self.__rotating:
            self.__set_rotation()

        # Boost
        if self.__boosting:
            self.boost()
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
        self.__pos.handle_offscreen(self.__hitbox)

        # Update hitbox position
        self.__hitbox.pos = self.__pos

        # Update projectiles
        self.__update_projectiles()

        # Update ray set position
        self.__ray_set.pos = self.__pos

    def __update_projectiles(self) -> None:
        for projectile in reversed(self.__projectiles):
            if projectile.deleted:  # Remove deleted projectiles
                self.__projectiles.remove(projectile)
            else:  # Update projectile if not deleted
                projectile.update()

    def shoot(self) -> None:
        if not self.__can_shoot:
            return

        x = self.__pos.x - math.cos(self.__angle) * self.__hitbox.height * .5
        y = self.__pos.y - math.sin(self.__angle) * self.__hitbox.height * .5

        self.__projectiles.append(Projectile(x, y, self.__angle))
        self.__can_shoot = False

        # Apply knockback force
        # if not self.__boosting:
        #     self.__vel.angle = self.__angle
        #     self.__vel.mag += Constants.PLAYER_SHOOT_KNOCKBACK

    def __set_rotation(self) -> None:
        self.__angle += self.__turn_speed * self.__rotate_dir
        self.__ray_set.rotate(self.__turn_speed * self.__rotate_dir)

    def boost(self) -> None:
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

    def rotate(self, dir: int) -> None:
        self.__angle += self.__turn_speed * dir
        self.__ray_set.rotate(self.__turn_speed * dir)

    def stop_rotate(self) -> None:
        self.__rotating = False
        self.__rotate_dir = 0

    @property
    def ray_set(self) -> RaySet:
        return self.__ray_set

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    def can_shoot(self) -> bool:
        return self.__can_shoot

    @property
    def rotate_dir(self) -> int:
        return self.__rotate_dir

    @property
    def projectiles(self) -> list[Projectile]:
        return self.__projectiles
    
    @property
    def angle(self) -> float:
        return math.degrees(self.__angle) - 90