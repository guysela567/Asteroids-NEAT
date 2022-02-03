from __future__ import annotations
from functools import lru_cache

from components.player import Player
from components.asteroid import Asteroid

from utils.constants import Constants
from utils.geometry.vector import PositionVector

from NEAT.genome import Genome

import random
import math
import copy

class Model:
    def __init__(self, ai: bool = False) -> None:    
        self.__ai = ai
        self.__seed = 0 if self.__ai else -1

        # Initialize player
        self.__player = Player(Constants.WINDOW_WIDTH * 0.5, 
                               Constants.WINDOW_HEIGHT * 0.5)

        # Initialize astroids
        self.__asteroid_amount = 4
        self.__asteroids = []
        self.__spawn_asteroids()

        # Score system
        self.__score = 0
        self.__high_score = 0

        # Game logic
        self.__paused = False

        # AI and stats
        self.__shots_fired = 4
        self.__shots_hit = 1
        self.__lifespan = 0
        self.__dead = False

        if self.__ai: # Generate neural network only if ai is true
            self.__brain = Genome(Constants.RAY_AMOUNT * 2 + 1, 4)

    def update(self, delta_time: float) -> None:
        # Update player
        self.__player.update(delta_time)

        # Update Asteroids
        for asteroid in self.__asteroids:
            asteroid.update(delta_time)

        # Sprite Collisions
        self.handle_collisions()
        
        # Add frame to lifespan
        self.__lifespan += 1

    def handle_collisions(self) -> None:
        # Asteroid with projectile collision
        for projectile in reversed(self.__player.projectiles):
            for asteroid in reversed(self.__asteroids):
                # Check for any projectile with astroid collision
                if asteroid.hitbox.collides(projectile.hitbox):
                    self.__shots_hit += 1

                    if asteroid.hits < Constants.ASTEROID_HITS - 1:
                        # Split asteroids into two parts

                        random_angle = random.uniform(-math.pi * .5, math.pi * .5)
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
        if any(asteroid.hitbox.collides(self.__player.hitbox) for asteroid in self.__asteroids):
            self.__dead = True
            self.__score = 0

            if not self.__ai:
                self.__spawn_asteroids()

    def think(self) -> int:
        if not self.__ai:
            return

        vision = self.__player.ray_set.cast(self.__asteroids)
        vision.append(int(self.__player.can_shoot))
        results = self.__brain.feed_forward(vision)
        
        if results[0] > .5:
            self.__player.boost()

        if results[1] > .5: 
            self.__player.rotate(1)
        elif results[2] > .5:
            self.__player.rotate(-1)

        if results[3] > .5:
            self.__player.shoot()
            self.__shots_fired += 1
    
    @staticmethod
    def generate_asteroid() -> Asteroid:
        # TODO Needs more refactoring

        spawn_gap = 50

        # Inside screen
        x = random.uniform(-Constants.WINDOW_WIDTH * .5, Constants.WINDOW_WIDTH * 1.5)
        x_inside = x > spawn_gap and x < Constants.WINDOW_WIDTH - spawn_gap

        y = random.choice([random.uniform(-spawn_gap * 2, -spawn_gap),  # Below screen
                    # Above screen
                   random.uniform(spawn_gap, spawn_gap * 2) + Constants.WINDOW_HEIGHT]) if x_inside \
            else random.uniform(spawn_gap, Constants.WINDOW_HEIGHT - spawn_gap)  # Inside sreen

        # Pick a random point on screen
        # random_point = PositionVector(random.uniform(
        #     spawn_gap, Constants.WINDOW_WIDTH - spawn_gap),
        #     random.uniform(spawn_gap, Constants.WINDOW_HEIGHT - spawn_gap))
        random_point = PositionVector(Constants.WINDOW_WIDTH * .5, Constants.WINDOW_HEIGHT * .5)

        # Get the angle between asteroid's position and random point
        angle = PositionVector(x, y).angle_between(random_point)

        return Asteroid(x, y, angle=angle)

    def __spawn_asteroids(self) -> None:
        if self.__ai:
            self.__asteroids = copy.deepcopy(Model.generate_wave_by_seed(self.__seed, self.__asteroid_amount))
        else: 
            self.__asteroids = [Model.generate_asteroid()
                                for _ in range(self.__asteroid_amount)]

    @staticmethod
    @lru_cache(maxsize=100)
    def generate_wave_by_seed(seed: int, length: int) -> None:
        return [Model.generate_asteroid()
                for _ in range(length)]

    def toggle_pause(self) -> None:
        self.__paused = not self.__paused

    def reset(self) -> None:
        # Reset player
        self.__player = Player(Constants.WINDOW_WIDTH * 0.5, Constants.WINDOW_HEIGHT * 0.5)

        # Reset astroids
        self.__asteroid_amount = 4
        self.__asteroids = []
        self.__spawn_asteroids()

        # Reset score system
        self.__score = 0
        self.__high_score = 0

        # Reset game logic
        self.__paused = False

        # Reset genetic information
        self.__shots_fired = 4
        self.__shots_hit = 1
        self.__lifespan = 0
        self.__dead = False

    @property
    def player(self) -> Player:
        return self.__player

    @property
    def asteroids(self) -> list[Asteroid]:
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

    @property
    def shots_fired(self) -> int:
        return self.__shots_fired
    
    @property
    def shots_hit(self) -> int:
        return self.__shots_hit

    @property
    def lifespan(self) -> int:
        return self.__lifespan

    @property
    def dead(self) -> bool:
        return self.__dead

    @property
    def brain(self) -> Genome:
        return self.__brain

    @property
    def seed(self) -> int:
        return self.__seed

    @brain.setter
    def brain(self, brain: Genome) -> None:
        self.__brain = brain

    @seed.setter
    def seed(self, seed: int) -> None:
        self.__seed = seed