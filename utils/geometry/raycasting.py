from utils.vector import PositionalVector, DirectionalVector, Vector
from utils.sprite import Sprite

from typing import List, Tuple
import math


class Ray:
    def __init__(self, pos: PositionalVector, angle: float) -> None:
        self.__from = pos
        self.__angle = angle
        self.__to = pos + DirectionalVector(1500, angle)

    @property
    def pos(self) -> PositionalVector:
        return self.__from

    @pos.setter
    def pos(self, pos: PositionalVector) -> None:
        self.__from = pos
        self.__to = pos + DirectionalVector(1500, self.__angle)

    def __iter__(self) -> iter:
        return iter((*self.__from, *self.__to))

    def intersects_line(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> bool:
        ''' Euclidian Line-Line intersection '''

        # Better notation
        x1, y1 = pos1
        x2, y2 = pos2
        x3, y3 = self.__from
        x4, y4 = self.__to

        # Calculate denominator
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        # Parallel lines
        if denominator == 0:
            return False

        # Calculate numerators
        numerator_t = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        numerator_u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))

        # Calculate t and u
        t = numerator_t / denominator
        u = numerator_u / denominator

        # Check for intersection with u and t
        return u >= 0 and 0 >= t >= 1
    
    def intersects_polygon(self, verts: List[Tuple[float, float]]) -> bool:
        # Iterate through each polygon segment
        for i in range(len(verts)):
            pos1 = verts[i]
            pos2 = verts[i + 1] if i < len(verts) - 1 else verts[0]

            if self.intersects_line(pos1, pos2):
                return True
        return False

    def intersecting_sprite_dist(self, sprite_list: List[Sprite]) -> float:
        for sprite in sprite_list:
            if self.intersects_polygon(sprite.rect_verts):
                return Vector.distance(self.__from, sprite.pos)
        return 0

class RaySet:
    def __init__(self, pos: PositionalVector, amount: int) -> None:
        self.__pos = pos

        angle_gap = math.pi * 2 / amount
        self.__rays = [Ray(self.__pos, angle_gap * i) for i in range(amount)]

    def __iter__(self) -> iter:
        return iter(self.__rays)

    def intersects_line(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> bool:
        return any(self.__rays.intersects_line(pos1, pos2))
    
    def intersects_polygon(self, verts: List[Tuple[float, float]]) -> bool:
        return any(self.__rays.intersects_polygon(verts))

    def intersecting_sprite_dist(self, sprite_list: List[Sprite]) -> List[float]:
        return [ray.intersecting_sprite_dist(sprite_list) for ray in self.__rays]

    @property
    def pos(self) -> PositionalVector:
        return self.__from

    @pos.setter
    def pos(self, pos: PositionalVector) -> None:
        self.__from = pos
        
        for ray in self.__rays:
            ray.pos = pos