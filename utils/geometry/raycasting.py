from utils.vector import PositionalVector, DirectionalVector, Vector
from utils.sprite import Sprite

from typing import List, Tuple
import numpy as np
import math


class Ray:
    def __init__(self, pos: PositionalVector, angle: float) -> None:
        self.__pos = pos
        self.__angle = angle
        self.__dir = DirectionalVector(1, self.__angle)
        self.__intersection = None

    def __iter__(self) -> iter:
        return iter((*self.__pos, *self.end))

    def intersects_line(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> PositionalVector:
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
        numerator_u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))

        # Calculate t and u
        t = numerator_t / denominator
        u = numerator_u / denominator

        # Check for intersection with u and t
        return PositionalVector(x1 + t * (x2 - x1), y1 + t * (y2 - y1)) \
            if u >= 0 and 0 <= t <= 1 else None
    
    def intersects_polygon(self, verts: List[Tuple[float, float]]) -> PositionalVector:
        closest = None
        closest_dist = 0

        # Iterate through each polygon segment
        for i in range(len(verts)):
            pos1 = verts[i]
            pos2 = verts[i + 1] if i < len(verts) - 1 else verts[0]

            point = self.intersects_line(pos1, pos2)
            if point is not None:
                dist = Vector.distance(self.__pos, point)
                if dist < closest_dist or closest is None:
                    closest = point
                    closest_dist = dist

        return closest

    def intersect_sprite_list(self, sprite_list: List[Sprite]) -> PositionalVector:
        closest = None
        closest_dist = 0

        # Get closest point
        for sprite in sprite_list:
            point = self.intersects_polygon(sprite.rect_verts)
            if point is not None:
                dist = Vector.distance(self.__pos, point)
                if dist < closest_dist or closest is None:
                    closest = point
                    closest_dist = dist

        self.__intersection = closest
        return closest

    def rotate(self, angle: float) -> None:
        self.__dir.angle += angle

    @property
    def angle(self) -> float:
        return self.__angle

    @property
    def pos(self) -> PositionalVector:
        return self.__pos

    @property
    def end(self) -> PositionalVector:
        return self.__pos + self.__dir if self.__intersection is None else self.__intersection

    @pos.setter
    def pos(self, pos: PositionalVector) -> None:
        self.__pos = pos
        

class RaySet:
    def __init__(self, pos: PositionalVector, angle: float, amount: int) -> None:
        self.__pos = pos

        angle_gap = math.pi * 2 / amount
        self.__rays = [Ray(self.__pos, angle + angle_gap * i) for i in range(amount)]

    def __iter__(self) -> iter:
        return iter(self.__rays)

    def intersects_line(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> bool:
        return any(self.__rays.intersects_line(pos1, pos2))
    
    def intersects_polygon(self, verts: List[Tuple[float, float]]) -> bool:
        return any(self.__rays.intersects_polygon(verts))

    def intersecting_sprite_dist(self, sprite_list: List[Sprite]) -> List[float]:
        return [Vector.distance(self.__pos, ray.intersect_sprite_list(sprite_list)) for ray in self.__rays]

    def rotate(self, angle: float) -> None:
        for ray in self.__rays:
            ray.rotate(angle)

    @property
    def pos(self) -> PositionalVector:
        return self.__pos

    @pos.setter
    def pos(self, pos: PositionalVector) -> None:
        self.__pos = pos
        
        for ray in self.__rays:
            ray.pos = pos