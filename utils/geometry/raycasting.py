from __future__ import annotations

from utils.geometry.vector import PositionVector, DirectionVector
from utils.geometry.collision import Hitbox
from utils.constants import Constants
from components.asteroid import Asteroid

import math


class Ray:
    '''A geometrical Ray with a given positon and angle
    :pos: position of the ray
    :angle: angle of the ray
    '''

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
        '''Updates the ray's looped position and projection end'''

        m = self.__dir.y / self.__dir.x # m = (y2 - y1) / (x2 - x1)
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
        '''Checks for intersection with the bottom of the screen,
        sets the looped position and projection end
        :param m: slope of the ray
        :param b: intersection with Y axis of the ray
        :returns: whether the Ray intersects with the bottom of the screen
        '''
        
        x = (Constants.WINDOW_HEIGHT - b) / m # Substitute Y = height
        if 0 < x < Constants.WINDOW_WIDTH: # Check if point is inside the screen
            # Update projection end and looped position accordingly
            self.__projection_end = PositionVector(x, Constants.WINDOW_HEIGHT)
            self.__looped_pos = PositionVector(x, 0)
            return True
        return False

    def check_top_intersection(self, m: float, b: float) -> bool:
        '''Checks for intersection with the top of the screen,
        sets the looped position and projection end
        :param m: slope of the ray
        :param b: intersection with Y axis of the ray
        :returns: whether the Ray intersects with the top of the screen
        '''

        x = -b / m # Substitute Y = 0
        if 0 < x < Constants.WINDOW_WIDTH: # Check if point is inside the screen
            # Update projection end and looped position accordingly
            self.__projection_end = PositionVector(x, 0)
            self.__looped_pos = PositionVector(x, Constants.WINDOW_HEIGHT)
            return True
        return False

    def check_right_intersection(self, m: float, b: float) -> bool:
        '''Checks for intersection with the right edge of the screen,
        sets the looped position and projection end
        :param m: slope of the ray
        :param b: intersection with Y axis of the ray
        :returns: whether the Ray intersects with the right edge of the screen
        '''

        y = m * Constants.WINDOW_WIDTH + b # Substitute X = width
        if 0 < y < Constants.WINDOW_HEIGHT: # Check if point is inside the screen
            # Update projection end and looped position accordingly
            self.__projection_end = PositionVector(Constants.WINDOW_WIDTH, y)
            self.__looped_pos = PositionVector(0, y)
            return True
        return False

    def check_left_intersection(self, b: float) -> bool:
        '''Checks for intersection with the left edge of the screen,
        sets the looped position and projection end
        :param m: slope of the ray
        :param b: intersection with Y axis of the ray
        :returns: whether the Ray intersects with the left edge of the screen
        '''

        y = b # Substitute X = 0
        if 0 < y < Constants.WINDOW_HEIGHT: # Check if point is inside the screen
            # Update projection end and looped position accordingly
            self.__projection_end = PositionVector(0, y)
            self.__looped_pos = PositionVector(Constants.WINDOW_WIDTH, y)
            return True
        return False

    def intersects_line(self, pos1: tuple[float, float], pos2: tuple[float, float], looped: bool = False) -> PositionVector:
        '''Applies Euclidian Line-Line intersection with a given line segment
        :param pos1: beginning position of the line segment
        :param pos2: end position of the line segment
        :returns: intersection point with the line segment,
        returns None if there is no intersection
        '''

        # Use the looped position if looped is True
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

        # Check for intersection using the values of t and u
        return PositionVector(x1 + t * (x2 - x1), y1 + t * (y2 - y1)) \
            if u >= 0 and 0 <= t <= 1 else None
    
    def intersects_polygon(self, hitbox: Hitbox, looped: bool = False) -> PositionVector:
        '''Returns the intersection point of the ray with the given polygon,
        returns None if there is no intersection
        :param hitbox: the hitbox of the polygon
        :looped: whether or not to use the looped version of the ray
        '''

        # Seek for closest intersection
        closest = None
        closest_dist = 0

        # Use the looped positon if looped is True
        start_pos = self.__looped_pos if looped else self.__pos

        # Iterate through every polygon segment
        verts = hitbox.rect_verts
        for i in range(len(verts)):
            pos1 = verts[i] # Get the first vertex in the line segment
            # Last vertex connects to the first vertex
            pos2 = verts[i + 1] if i < len(verts) - 1 else verts[0]

            # Check for intersection with that line segment
            point = self.intersects_line(pos1, pos2, looped=looped)
            if point is not None: # Check if there is an intersection point
                # Calculate distance between that point and the ray origin point
                dist = start_pos.distance(point)
                # Update position if distance is the smallest
                if dist < closest_dist or closest is None:
                    closest = point
                    closest_dist = dist
        
        return closest

    def intersects_asteroids(self, asteroids: list[Asteroid], looped: bool = False) -> PositionVector:
        '''Returns the intersection point of the ray with closest asteroid in the list,
        returns None if there is no intersection
        :param asteroids: list of the asteroids
        :looped: whether or not to use the looped version of the ray
        '''
        
        # Seek for closest intersection
        closest = None
        closest_dist = 0

        # Use the looped position if looped is True
        start_pos = self.__looped_pos if looped else self.__pos

        # Iterate through every asteroid
        for asteroid in asteroids:
            # Check for intersection with hitbox
            point = self.intersects_polygon(asteroid.hitbox, looped=looped)
            if point:
                # Calculate distance between that point and the ray origin point
                dist = start_pos.distance(point)
                # Update position if distance is the smallest
                if dist < closest_dist or closest is None:
                    closest = point
                    closest_dist = dist

        # If looped is True and there is an intersection
        # set the ray as a looped ray
        self.__looped = looped and closest
        self.__intersection = closest # Update intersection point
        # Set the asteroid that the ray intersects with
        self.__hit = asteroid if closest else None
        return closest

    def rotate(self, angle: float) -> None:
        '''Rotates the ray by a given angle
        :param angle: angle to rotate by, measured in radians
        '''

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
    '''A set of multiple rays, whom origins start at the origin of the set
    :param pos: origin position of the ray set
    :angle: offset angle of the ray set
    :amount: the amount of rays in the ray set
    '''

    def __init__(self, pos: PositionVector, angle: float, amount: int) -> None:
        self.__pos = pos

        angle_gap = math.pi * 2 / amount
        self.__rays = [Ray(self.__pos, angle + angle_gap * i) for i in range(amount)]

    def __iter__(self):
        return iter(self.__rays)

    def cast(self, asteroids: list[Asteroid]) -> list[float]:
        '''Casts each ray in ray set on the environment,
        Results processed into the inputs of the neural network
        :param asteroids: list of asteroids on the screen
        :returns: list of distances and redshift values of the asteroids
        '''

        # Start with an empty list
        vision: list[float] = []

        # Iterate through every ray
        for ray in self.__rays:
            hit = False
            dist = 0

            # Check for intersection with asteroids
            point = ray.intersects_asteroids(asteroids)
            if point:
                # Calculate distance and set hit to True
                dist = ray.pos.distance(point)
                hit = True

            elif ray.looped_pos: # Else check if ray has a looped position
                # Check for intersection with looped ray
                point = ray.intersects_asteroids(asteroids, looped=True)
                if point:
                    # Calculate distance and set hit to True
                    dist = ray.looped_pos.distance(point) + ray.length
                    hit = True

            if hit: # If there is an intersection
                # Calculate the cosine of the deviation angle using the dot product
                redshift = (ray.dir.dot(ray.hit.velocity)) / (ray.dir.mag * ray.hit.velocity.mag)
                # Normalize distance and append it with the redshift value
                vision.extend((1 / dist, redshift))
            else: vision.extend((0, 0)) # Zero if there is no intersection

        return vision

    def rotate(self, angle: float) -> None:
        '''Rotates every ray in the ray set by a given angle
        :param angle: angle to rotate by, measured in radians
        '''
        
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