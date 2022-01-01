from __future__ import annotations

from utils.geometry.vector import PositionVector, DirectionVector
from utils.geometry.collision import Hitbox
from utils.constants import Constants

import math


class Ray:
    def __init__(self, pos: PositionVector, angle: float) -> None:
        self.__pos = pos
        self.__angle = angle
        self.__dir = DirectionVector(Constants.WINDOW_DIAGONAL, self.__angle)
        self.__intersection = None

        self.__looped_pos = self.__loop()

    def __iter__(self) -> iter:
        return iter((*self.__pos, *self.end))

    def __loop(self) -> PositionVector:
        # Not a function
        if self.__dir.x == 0:
            return None

        m = self.__dir.y / self.__dir.x # (y2 - y1) / (x2 - x1)
        b = self.__pos.y - m * self.__pos.x # b = y - mx

        # Border Y = 0
        x = -b / m
        if 0 < x  < Constants.WINDOW_WIDTH:
            return PositionVector(x, Constants.WINDOW_HEIGHT)
        
        # Border Y = height
        x = (Constants.WINDOW_HEIGHT -b) / m
        if 0 < x < Constants.WINDOW_WIDTH:
            return PositionVector(x, 0)

        # Border X = 0
        y = b
        if 0 < y < Constants.WINDOW_HEIGHT:
            return PositionVector(Constants.WINDOW_WIDTH, y)

        # Border X = width
        y = m * Constants.WINDOW_WIDTH + b
        if 0 < y < Constants.WINDOW_HEIGHT:
            return PositionVector(0, y)


    def intersects_line(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> PositionVector:
        ''' Euclidian Line-Line intersection '''

        # Better notation
        x1, y1 = pos1
        x2, y2 = pos2
        x3, y3 = self.__pos
        x4, y4 = self.__pos + self.__dir

        # Calculate denominator
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        # Parallel lines
        if math.isclose(denominator, 0):
            return None

        # Calculate numerators
        numerator_t = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        numerator_u = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)

        # Calculate t and u
        t = numerator_t / denominator
        u = numerator_u / denominator

        # Check for intersection with u and t
        return PositionVector(x1 + t * (x2 - x1), y1 + t * (y2 - y1)) \
            if u >= 0 and 0 <= t <= 1 else None
    
    def intersects_polygon(self, verts: list[tuple[float, float]]) -> PositionVector:
        closest = None
        closest_dist = 0

        # Iterate through each polygon segment
        for i in range(len(verts)):
            pos1 = verts[i]
            pos2 = verts[i + 1] if i < len(verts) - 1 else verts[0]

            point = self.intersects_line(pos1, pos2)
            if point is not None:
                dist = self.__pos.distance(point)
                if dist < closest_dist or closest is None:
                    closest = point
                    closest_dist = dist

        return closest

    def intersect_sprite_list(self, sprite_list: list[Hitbox]) -> PositionVector:
        closest = None
        closest_dist = 0

        # Get closest point
        for sprite in sprite_list:
            point = self.intersects_polygon(sprite.rect_verts)
            if point is not None:
                dist = self.__pos.distance(point)
                if dist < closest_dist or closest is None:
                    closest = point
                    closest_dist = dist

        self.__intersection = closest
        return closest

    def rotate(self, angle: float) -> None:
        self.__dir.angle += angle
        self.__looped_pos = self.__loop()

    @property
    def angle(self) -> float:
        return self.__angle

    @property
    def pos(self) -> PositionVector:
        return self.__pos

    @property
    def end(self) -> PositionVector:
        return self.__pos + self.__dir if self.__intersection is None else self.__intersection

    @property
    def looped(self) -> tuple[float, float, float, float]:
        return (*self.__looped_pos, *(self.__looped_pos + self.__dir))

    @property
    def looped_pos(self) -> PositionVector:
        return self.__looped_pos

    @pos.setter
    def pos(self, pos: PositionVector) -> None:
        self.__pos = pos
        

class RaySet:
    def __init__(self, pos: PositionVector, angle: float, amount: int) -> None:
        self.__pos = pos

        angle_gap = math.pi * 2 / amount
        self.__rays = [Ray(self.__pos, angle + angle_gap * i) for i in range(amount)]

    def __iter__(self) -> iter:
        return iter(self.__rays)

    def intersects_line(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> bool:
        return any(self.__rays.intersects_line(pos1, pos2))
    
    def intersects_polygon(self, verts: list[tuple[float, float]]) -> bool:
        return any(self.__rays.intersects_polygon(verts))

    def intersecting_sprite_dist(self, sprite_list: list[Hitbox]) -> list[float]:
        return [self.__pos.distance(ray.intersect_sprite_list(sprite_list)) for ray in self.__rays]

    def rotate(self, angle: float) -> None:
        for ray in self.__rays:
            ray.rotate(angle)

    @property
    def pos(self) -> PositionVector:
        return self.__pos

    @pos.setter
    def pos(self, pos: PositionVector) -> None:
        self.__pos = pos
        
        for ray in self.__rays:
            ray.pos = pos