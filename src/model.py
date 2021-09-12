from components.player import Player
from components.asteroid import Asteroid

from utils.constants import Constants

from typing import List
from random import uniform
import arcade
import math


class Model:
    def __init__(self) -> None:
        # Initialize player
        self.__player = Player(Constants.WINDOW_WIDTH *
                               0.5, Constants.WINDOW_HEIGHT * 0.5)

        # Initialize astroids
        self.__asteroids = [Asteroid(uniform(0, Constants.WINDOW_WIDTH),
                                     uniform(0, Constants.WINDOW_HEIGHT)) for _ in range(4)]

    def update(self, delta_time: float) -> None:
        # Update player
        self.__player.update()

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

                    # Respawn all 4 asteroids if none exist
                    if len(self.__asteroids) == 0:
                        self.__asteroids = [Asteroid(uniform(0, Constants.WINDOW_WIDTH),
                                                     uniform(0, Constants.WINDOW_HEIGHT)) for _ in range(4)]

        # TODO Add collision check and handle collisions of player with astroids

    @property
    def player(self) -> Player:
        return self.__player

    @property
    def asteroids(self) -> List[Asteroid]:
        return self.__asteroids
