from __future__ import annotations

from components.player import Player
from components.asteroid import Asteroid

from utils.constants import Constants
from utils.vector import Vector, PositionalVector

from NEAT.genome import Genome

from random import uniform, choice
import math


class Model:
    def __init__(self, ai: bool = False) -> None:
        # Initialize player
        self.__player = Player(Constants.WINDOW_WIDTH * 0.5, Constants.WINDOW_HEIGHT * 0.5)

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
        self.__ai = ai
        self.__shots_fired = 4
        self.__shots_hit = 1
        self.__lifespan = 0
        self.__dead = False

        if self.__ai: # Generate neural network only if ai is true
            self.__brain = Genome(Constants.RAY_AMOUNT + 1, 4)

    def update(self, delta_time: float, ai=False) -> None:
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
                if asteroid.sprite.collides(projectile.sprite):
                    self.__shots_hit += 1

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
        if any(asteroid.sprite.collides(self.__player.sprite) for asteroid in self.__asteroids):
            self.__dead = True
            self.__spawn_asteroids()
            self.__score = 0

    def think(self) -> int:
        if not self.__ai:
            return

        asteroid_sprite_list = [a.sprite for a in self.__asteroids]
        vision = self.__player.ray_set.intersecting_sprite_dist(asteroid_sprite_list)

        can_shoot = 1 if self.__player.can_shoot else 0
        inputs = [1 / v if v != 0 else 0 for v in vision]
        inputs.append(can_shoot)

        results = self.__brain.feed_forward(inputs)
        
        if results[0] > .5:
            if results[1] > .5: 
                self.__player.rotate(1)
            else: self.__player.rotate(-1)

        if results[2] > .5:
            self.__player.boost()

        if results[3] > .5:
            self.__player.shoot()
            self.__shots_fired += 1

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
        self.__asteroids = [Model.generate_asteroid()
                            for _ in range(self.__asteroid_amount)]

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
        self.__shots_fired = 0
        self.__shots_hit = 0
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

    @brain.setter
    def brain(self, brain: Genome) -> None:
        self.__brain = brain