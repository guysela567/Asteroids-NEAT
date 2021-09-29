from components.player import Player
from components.asteroid import Asteroid

from utils.constants import Constants
from utils.vector import Vector, PositionalVector

from typing import List
from random import uniform, choice
import math

import arcade


class Model:
    def __init__(self) -> None:
        # Initialize player
        self.__player = Player(Constants.WINDOW_WIDTH *
                               0.5, Constants.WINDOW_HEIGHT * 0.5)

        # Initialize astroids
        self.__asteroid_amount = 4
        self.__asteroids = []
        self.__spawn_asteroids()

        # Score system
        self.__score = 0
        self.__high_score = 0

        # Game logic
        self.__paused = False

        self.__sounds = {
            'thrust': arcade.load_sound('assets/sounds/thrust.wav'),
            'fire': arcade.load_sound('assets/sounds/fire.wav'),
            'explosion0': arcade.load_sound('assets/sounds/bangLarge.wav'),
            'explosion1': arcade.load_sound('assets/sounds/bangMedium.wav'),
            'explosion2': arcade.load_sound('assets/sounds/bangSmall.wav'),
        }

    def update(self, delta_time: float) -> None:
        # Update player
        self.__player.update(delta_time)

        # Update Asteroids
        for asteroid in self.__asteroids:
            asteroid.update(delta_time)

        # Asteroid with projectile collision
        for projectile in reversed(self.__player.projectiles):
            for asteroid in reversed(self.__asteroids):
                # Check for any projectile with astroid collision
                if arcade.check_for_collision(asteroid.sprite, projectile.sprite):
                    # Play explosion sound
                    self.play_sound(f'explosion{asteroid.hits}')
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

                    # Add points to score
                    self.__score += Constants.SCORE_SYSTEM[asteroid.hits]

                    # High score beat
                    if self.__score > self.__high_score:
                        self.__high_score = self.__score

                    # Delete old asteroid
                    self.__asteroids.remove(asteroid)

                    # Delete the projectile that hit the astroid
                    projectile.delete()

                    # Respawn asteroids if none exist
                    if len(self.__asteroids) == 0:
                        self.__asteroid_amount += 1
                        self.__spawn_asteroids()

        # Asteroid with player collision
        if any(arcade.check_for_collision(asteroid.sprite, self.__player.sprite)
               for asteroid in self.__asteroids):
            self.__spawn_asteroids()
            self.__score = 0

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

    def play_sound(self, sound: str) -> None:
        arcade.play_sound(self.__sounds[sound])

    @property
    def player(self) -> Player:
        return self.__player

    @property
    def asteroids(self) -> List[Asteroid]:
        return self.__asteroids

    @property
    def score(self) -> int:
        return self.__score

    @property
    def high_score(self) -> int:
        return self.__high_score

    @property
    def paused(self) -> bool:
        return self.__paused

    def toggle_pause(self) -> None:
        self.__paused = not self.__paused
