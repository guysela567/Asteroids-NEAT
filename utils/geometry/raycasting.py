from __future__ import annotations

from utils.geometry.vector import PositionVector, DirectionVector
from utils.geometry.collision import Hitbox
from utils.constants import Constants
from components.asteroid import Asteroid
import numpy as np

import math


class Ray:
    def __init__(self, pos: PositionVector, angle: float) -> None:
        self.__pos = pos
        self.__angle = angle
        self.__dir = DirectionVector(Constants.WINDOW_DIAGONAL, self.__angle)
        self.__intersection = None

        self.__looped = False
        self.__looped_pos: PositionVector = None
        self.__projection_end: PositionVector = None
        self.__hit: Asteroid = None
        self.update()

    def __iter__(self) -> iter:
        return iter((*self.__pos, *self.end))

    def update(self) -> None:
        m = self.__dir.y / self.__dir.x # (y2 - y1) / (x2 - x1)
        b = self.__pos.y - m * self.__pos.x # b = y - mx
        
        # Pointing right: check right border
        if self.__dir.x > 0:
            if self.check_right_intersection(m, b):
                return

        # Pointing left: Check left border
        elif self.check_left_intersection(b):
            return

        # Facing up: check top border
        if self.__dir.y < 0 and self.check_top_intersection(m, b):
            return
            
        # Lastly, check for bottom instersection
        if self.check_bottom_intersection(m, b):
            return

        # No projection and looped points
        self.__projection_end, self.__looped_pos = None, None
    
    def check_bottom_intersection(self, m: float, b: float) -> bool:
        # Border Y = height
        x = (Constants.WINDOW_HEIGHT - b) / m
        if 0 < x < Constants.WINDOW_WIDTH:
            self.__projection_end = PositionVector(x, Constants.WINDOW_HEIGHT)
            self.__looped_pos = PositionVector(x, 0)
            return True
        return False

    def check_top_intersection(self, m: float, b: float) -> bool:
        # Border Y = 0
        x = -b / m
        if 0 < x < Constants.WINDOW_WIDTH:
            self.__projection_end = PositionVector(x, 0)
            self.__looped_pos = PositionVector(x, Constants.WINDOW_HEIGHT)
            return True
        return False

    def check_right_intersection(self, m: float, b: float) -> bool:
        # Border X = width
        y = m * Constants.WINDOW_WIDTH + b
        if 0 < y < Constants.WINDOW_HEIGHT:
            self.__projection_end = PositionVector(Constants.WINDOW_WIDTH, y)
            self.__looped_pos = PositionVector(0, y)
            return True
        return False

    def check_left_intersection(self, b: float) -> bool:
        # Border X = 0
        y = b
        if 0 < y < Constants.WINDOW_HEIGHT:
            self.__projection_end = PositionVector(0, y)
            self.__looped_pos = PositionVector(Constants.WINDOW_WIDTH, y)
            return True
        return False

    def intersects_line(self, pos1: tuple[float, float], pos2: tuple[float, float], looped: bool = False) -> PositionVector:
        ''' Euclidian Line-Line intersection '''

        start_pos = self.__looped_pos if looped else self.__pos

        # Better notation
        x1, y1 = pos1
        x2, y2 = pos2
        x3, y3 = start_pos
        x4, y4 = start_pos + self.__dir

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
    
    def intersects_polygon(self, hitbox: Hitbox, looped: bool = False) -> PositionVector:
        closest = None
        closest_dist = 0

        start_pos = self.__looped_pos if looped else self.__pos

        # Iterate through each polygon segment
        verts = hitbox.rect_verts
        for i in range(len(verts)):
            pos1 = verts[i]
            pos2 = verts[i + 1] if i < len(verts) - 1 else verts[0]

            point = self.intersects_line(pos1, pos2, looped=looped)
            if point is not None:
                dist = start_pos.distance(point)
                if dist < closest_dist or closest is None:
                    closest = point
                    closest_dist = dist
        
        return closest

    def intersects_asteroids(self, asteroids: list[Asteroid], looped: bool = False) -> PositionVector:
        closest = None
        closest_dist = 0

        start_pos = self.__looped_pos if looped else self.__pos

        # Get closest point
        for asteroid in asteroids:
            if point := self.intersects_polygon(asteroid.hitbox, looped=looped):
                dist = start_pos.distance(point)
                if dist < closest_dist or closest is None:
                    closest = point
                    closest_dist = dist

        self.__looped = looped and closest
        self.__intersection = closest

        self.__hit = asteroid if closest else None
        return closest

    def rotate(self, angle: float) -> None:
        self.__dir.angle += angle
        self.update()

    @property
    def angle(self) -> float:
        return self.__angle

    @property
    def pos(self) -> PositionVector:
        return self.__pos

    @property
    def end(self) -> PositionVector:
        infinite_end = self.__projection_end or self.__pos + self.__dir
        return self.__intersection or infinite_end

    @property
    def looped(self) -> tuple[float, float, float, float]:
        return (*self.__looped_pos, *(self.__intersection or self.__looped_pos + self.__dir))
    
    @property
    def infinite(self) -> tuple[float, float, float, float]:
        return (*self.__pos, *(self.__pos + self.__dir))

    @property
    def is_looped(self) -> PositionVector:
        return self.__looped and self.__looped_pos

    @property
    def looped_pos(self) -> PositionVector:
        return self.__looped_pos

    @property
    def length(self) -> float:
        return self.__pos.distance(self.__projection_end)
    
    @property
    def hit(self) -> Asteroid:
        return self.__hit
    
    @property
    def dir(self) -> DirectionVector:
        return self.__dir

    @pos.setter
    def pos(self, pos: PositionVector) -> None:
        self.__pos = pos
        self.update()
        

class RaySet:
    def __init__(self, pos: PositionVector, angle: float, amount: int) -> None:
        self.__pos = pos

        angle_gap = math.pi * 2 / amount
        self.__rays = [Ray(self.__pos, angle + angle_gap * i) for i in range(amount)]

    def __iter__(self):
        return iter(self.__rays)

    def intersects_line(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> bool:
        return any(self.__rays.intersects_line(pos1, pos2))
    
    def intersects_polygon(self, verts: list[tuple[float, float]]) -> bool:
        return any(self.__rays.intersects_polygon(verts))

    def cast(self, asteroids: list[Asteroid]) -> list[float]:
        dists: list[float] = []

        for ray in self.__rays:
            hit = False
            dist = 0

            if point := ray.intersects_asteroids(asteroids):
                dist = ray.pos.distance(point)
                hit = True

            elif ray.looped_pos:
                if point := ray.intersects_asteroids(asteroids, looped=True):
                    dist = ray.looped_pos.distance(point) + ray.length
                    hit = True

            if hit:
                redshift = ray.dir.normalized().dot(ray.hit.velocity.normalized())
                dists.extend((1 / dist, redshift))
            else: dists.extend((0, 0))

        return dists

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