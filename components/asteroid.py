from utils.geometry.vector import PositionVector, DirectionVector
from utils.geometry.collision import Hitbox
from utils.constants import Constants

import math
import random


class Asteroid:
    def __init__(self, x: float, y: float, angle: float = None, hits: int = 0) -> None:
        self.__pos = PositionVector(x, y)
        self.__hits = hits

        self.__hitbox = Hitbox(self.__pos, 'asteroid', Constants.ASTEROID_SPRITE_SCALE[self.__hits])

        # Get a random angle for direction
        self.__angle = random.uniform(0, math.pi * 2) if angle is None else angle

        # Set velocity vector in that angle
        self.__vel = DirectionVector(
            Constants.ASTEROID_VELOCITY[self.__hits], self.__angle + math.pi)

        # TODO Add destruction vfx

    def update(self, delta_time: float) -> None:
        self.__pos += self.__vel
        self.__pos.handle_offscreen(self.__hitbox)

        # Update hitbox position
        self.__hitbox.pos = self.__pos

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    def x(self) -> float:
        return self.__pos.x

    @property
    def y(self) -> float:
        return self.__pos.y

    @property
    def hits(self) -> float:
        return self.__hits
    
    @property
    def sprite_index(self) -> None:
        return self.__hitbox.index

    @property
    def angle(self) -> float:
        return -(int(math.degrees(self.__angle)) - 90) % 360

    @property
    def velocity(self) -> float:
        return self.__vel