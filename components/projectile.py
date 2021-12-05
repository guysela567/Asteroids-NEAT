from utils.vector import PositionalVector, DirectionalVector
from utils.constants import Constants
from utils.geometry.collision import Hitbox

import numpy as np
import math


class Projectile:
    def __init__(self, x: float, y: float, angle: float) -> None:
        self.__pos = PositionalVector(x, y)
        self.__angle = angle

        self.__hitbox = Hitbox(self.__pos, 'projectile', Constants.PROJECTILE_SPRITE_SCALE)

        self.__vel = DirectionalVector(
            Constants.PROJECTILE_SPEED, self.__angle + math.pi)

        self.__distance_traveled = 0
        self.__max_distance = 750
        self.__deleted = False

    def delete(self) -> None:
        self.__deleted = True

    def update(self) -> None:
        self.__pos += self.__vel
        self.__pos.handle_offscreen(self.__hitbox)

        self.__hitbox.pos = self.__pos  # Update sprite position
        self.__distance_traveled += Constants.PROJECTILE_SPEED  # Add travel distance

        # Delete projectile if traveled too much
        if self.__distance_traveled >= self.__max_distance:
            self.__deleted = True

        # Fade out as more distance is traveled
        percentage = self.__distance_traveled / self.__max_distance
        self.__hitbox.alpha = np.interp(percentage, [0, 1], [255, 0])

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    def deleted(self) -> bool:
        return self.__deleted

    @property
    def angle(self) -> float:
        deg = -(int(math.degrees(self.__angle)) - 90) % 360
        return deg if deg > 0 else 360 - deg
