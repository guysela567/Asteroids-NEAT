from __future__ import annotations
from functools import lru_cache

from components.player import Player
from components.asteroid import Asteroid

from utils.constants import Constants
from utils.geometry.vector import PositionVector

from NEAT.genome import Genome

import random, math, copy, json, os


class Model:
    '''Holds all of the data and data-manipulating functions for the main game
    :param ai: whether to use AI for the player agent
    '''

    def __init__(self, ai: bool = False) -> None:
        self.__ai_training = ai
        self.__seed = 0 if self.__ai_training else -1
        self.__ai_playing = False

        # Initialize player
        self.__player = Player(Constants.WINDOW_WIDTH * 0.5, 
                               Constants.WINDOW_HEIGHT * 0.5)

        # Initialize astroids
        self.__asteroid_amount = 4
        self.__asteroids: list[Asteroid] = []
        self.__spawn_asteroids()

        # Score system
        self.__score = 0

        self.__high_score = 0
        # Load highscore from file
        if os.path.exists('data/game_data.json'):
            with open('data/game_data.json', 'r') as f:
                self.__high_score = json.load(f)['highscore']
        else:
            with open('data/game_data.json', 'w') as f:
                f.write(json.dumps({ 'highscore': self.__high_score }))

        # Game logic
        self.__paused = False
        self.__lives = 5
        self.__game_over = False

        # TODO: Implement lives system

        # AI and stats
        self.__shots_fired = 4
        self.__shots_hit = 1
        self.__lifespan = 0
        self.__dead = False

        if self.__ai_training: # Generate neural network only if AI is true
            self.__brain = Genome(Constants.RAY_AMOUNT * 2 + 1, 4)
        else: # Else load pre-trained model
            self.__brain = Genome.load('data/brain_data.json')

    def update(self, delta_time: float) -> None:
        '''Updates the game data
        :param delta_time: the time that has passed since last update, measured in seconds
        '''

        # Make AI move
        if self.__ai_playing:
            self.think()

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
        '''Handles collisions between every game component'''

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

                        # 180 degrees angle from first split
                        self.__asteroids.append(Asteroid(
                            asteroid.x, asteroid.y,
                            random_angle + math.pi,
                            asteroid.hits + 1))

                    # Add points to score
                    self.__score += Constants.SCORE_SYSTEM[asteroid.hits]

                    # High score beat
                    if self.__score > self.__high_score \
                        and not self.__ai_playing and not self.__ai_training:
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
            
            if not self.__ai_training:
                # Proceed to next life cycle
                self.__lives -= 1
                if self.__lives > 0:
                    self.reset(true_reset=False)
                else:
                    # Game over
                    self.__game_over = True
                    self.__paused = True

    def think(self) -> int:
        '''Makes the vision list and acts according to the neural network predictions'''

        vision = self.__player.ray_set.cast(self.__asteroids)
        vision.append(int(self.__player.can_shoot and vision[0] != 0))
        results = self.__brain.feed_forward(vision)
        
        if results[0] > .8:
            self.__player.boost()

        if results[1] > .8: 
            self.__player.rotate(1)
        elif results[2] > .8:
            self.__player.rotate(-1)

        if results[3] > .8:
            self.__player.shoot()
            self.__shots_fired += 1
    
    @staticmethod
    def generate_asteroid() -> Asteroid:
        '''Generates a random asteroid'''

        spawn_gap = 50

        # Inside screen
        x = random.uniform(-Constants.WINDOW_WIDTH * .5, Constants.WINDOW_WIDTH * 1.5)
        x_inside = x > spawn_gap and x < Constants.WINDOW_WIDTH - spawn_gap

        y = random.choice([random.uniform(-spawn_gap * 2, -spawn_gap),  # Below screen
                    # Above screen
                   random.uniform(spawn_gap, spawn_gap * 2) + Constants.WINDOW_HEIGHT]) if x_inside \
            else random.uniform(spawn_gap, Constants.WINDOW_HEIGHT - spawn_gap)  # Inside sreen

        # Pick a random point on screen
        random_point = PositionVector(Constants.WINDOW_WIDTH * .5, Constants.WINDOW_HEIGHT * .5)

        # Get the angle between asteroid's position and random point
        angle = PositionVector(x, y).angle_between(random_point)

        return Asteroid(x, y, angle=angle)

    def __spawn_asteroids(self) -> None:
        '''Spawns new asteroids on screen'''
        
        if self.__ai_training:
            self.__asteroids = copy.deepcopy(Model.generate_wave_by_seed(self.__seed, self.__asteroid_amount))
        else: 
            self.__asteroids = [Model.generate_asteroid()
                                for _ in range(self.__asteroid_amount)]

    @staticmethod
    @lru_cache(maxsize=1000)
    def generate_wave_by_seed(seed: int, length: int) -> None:
        '''Generates a seeded wave of asteroids based on the wave length and seed value
        :param seed: the seed in which to generate the wave by
        :param length: the wave length of the asteroids'''
        return [Model.generate_asteroid() for _ in range(length)]

    def toggle_pause(self) -> None:
        '''Toggles between play/pause'''
        self.__paused = not self.__paused

    def dump_highscore(self) -> None:
        '''Saves the highscore to a file'''
        with open('data/game_data.json', 'w') as f:
            f.write(json.dumps({ 'highscore': self.__high_score }))

    def reset(self, true_reset: bool = True) -> None:
        '''Resets all of the data of the game'''

        # Reset player
        self.__player = Player(Constants.WINDOW_WIDTH * 0.5, Constants.WINDOW_HEIGHT * 0.5)

        # Reset astroids
        self.__asteroid_amount = 4
        self.__asteroids = []
        self.__spawn_asteroids()

        # Reset score and lives on true reset
        if true_reset: 
            self.__score = 0
            self.__lives = 5

        # Reset game logic
        self.__paused = False
        self.__game_over = False

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

    @property
    def ai_playing(self) -> bool:
        return self.__ai_playing

    @property
    def ai_training(self) -> bool:
        return self.__ai_training
    
    @property
    def game_over(self) -> bool:
        return self.__game_over

    @property
    def lives(self) -> int:
        return self.__lives

    @brain.setter
    def brain(self, brain: Genome) -> None:
        self.__brain = brain

    @seed.setter
    def seed(self, seed: int) -> None:
        self.__seed = seed

    @ai_playing.setter
    def ai_playing(self, ai: bool) -> None:
        self.__ai_playing = ai

    @score.setter
    def score(self, score: int) -> None:
        self.__score = score