from utils.geometry.vector import PositionVector, DirectionVector
from utils.geometry.collision import Hitbox
from utils.constants import Constants

import math
import random


class Asteroid:
    '''Physical component for a single asteroid
    :param x: X coordinate of the asteroid's position
    :param y: Y coordinate of the asteroid's position
    :param angle: direction angle of the asteroid, measured in radians
    :param hits: number of hits took to split this asteroid (0 for default size)'''

    def __init__(self, x: float, y: float, angle: float = None, hits: int = 0) -> None:
        self.__pos = PositionVector(x, y)
        self.__hits = hits

        self.__hitbox = Hitbox(self.__pos, 'asteroid', Constants.ASTEROID_SPRITE_SCALE[self.__hits])

        # Get a random angle for direction
        self.__angle = random.uniform(0, math.pi * 2) if angle is None else angle

        # Set velocity vector in that angle
        self.__vel = DirectionVector(
            Constants.ASTEROID_VELOCITY[self.__hits], self.__angle + math.pi)

    def update(self, delta_time: float) -> None:
        '''Updates the asteroid
        :param delta_time: the time that has passed since last update, measured in seconds'''
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
    def hits(self) -> int:
        return self.__hits
    
    @property
    def sprite_index(self) -> int:
        return self.__hitbox.index

    @property
    def angle(self) -> float:
        return -(int(math.degrees(self.__angle)) - 90) % 360

    @property
    def velocity(self) -> DirectionVector:
        return self.__vel