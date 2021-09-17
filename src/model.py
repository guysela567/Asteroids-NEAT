from components.player import Player
from components.asteroid import Asteroid

from utils.constants import Constants
from utils.vector import Vector, PositionalVector

from typing import List
from random import uniform, choice
import arcade
import math


class Model:
    def __init__(self) -> None:
        # Initialize player
        self.__player = Player(Constants.WINDOW_WIDTH *
                               0.5, Constants.WINDOW_HEIGHT * 0.5)

        # Initialize astroids
        self.__asteroid_amount = 5
        self.__asteroids = []
        self.__spawn_asteroids()

    def update(self, delta_time: float) -> None:
        # Update player
        self.__player.update(delta_time)

        # Update Asteroids
        for asteroid in self.__asteroids:
            asteroid.update(delta_time)

        # Collision Check:

        for bullet in reversed(self.__player.bullets):
            for asteroid in reversed(self.__asteroids):
                # Check for any bullet with astroid collision
                if arcade.check_for_collision(asteroid.sprite, bullet.sprite):
                    if asteroid.hits < Constants.ASTEROID_HITS - 1:
                        # Split asteroids into two parts

                        random_angle = uniform(-math.pi * .5, math.pi * .5)
                        self.__asteroids.append(Asteroid(
                            asteroid.x, asteroid.y,
                            random_angle,
                            asteroid.hits + 1))

                        self.__asteroids.append(Asteroid(
                            asteroid.x, asteroid.y,
                            random_angle + math.pi,
                            asteroid.hits + 1))

                    # Delete old asteroid
                    self.__asteroids.remove(asteroid)

                    # Delete the bullet that hit the astroid
                    bullet.delete()

                    # Respawn asteroids if none exist
                    if len(self.__asteroids) == 0:
                        self.__asteroid_amount += 1
                        self.__spawn_asteroids()

        # Asteroid with player collision
        if any(arcade.check_for_collision(asteroid.sprite, self.__player.sprite)
               for asteroid in self.__asteroids):
            self.__spawn_asteroids()

    @staticmethod
    def generate_asteroid() -> Asteroid:
        # TODO Needs more refactoring

        spawn_gap = 50

        # Inside screen
        x = uniform(-Constants.WINDOW_WIDTH * .5, Constants.WINDOW_WIDTH * 1.5)
        x_inside = x > spawn_gap and x < Constants.WINDOW_WIDTH - spawn_gap

        y = choice([uniform(-spawn_gap * 2, -spawn_gap),  # Below screen
                    # Above screen
                    uniform(spawn_gap, spawn_gap * 2) + Constants.WINDOW_HEIGHT]) if x_inside \
            else uniform(spawn_gap, Constants.WINDOW_HEIGHT - spawn_gap)  # Inside sreen

        # Pick a random point on screen
        random_point = PositionalVector(uniform(
            spawn_gap, Constants.WINDOW_WIDTH - spawn_gap),
            uniform(spawn_gap, Constants.WINDOW_HEIGHT - spawn_gap))

        # Get the angle between asteroid's position and random point
        angle = Vector.angle_between(PositionalVector(x, y), random_point)

        return Asteroid(x, y, angle=angle)

    def __spawn_asteroids(self) -> None:
        self.__asteroids = [self.generate_asteroid()
                            for _ in range(self.__asteroid_amount)]

    @property
    def player(self) -> Player:
        return self.__player

    @property
    def asteroids(self) -> List[Asteroid]:
        return self.__asteroids
