import math


class Constants:
    '''The constants class holds constant data and configuration for the game'''
    
    # Window config
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    WINDOW_TITLE = 'Asteroids'
    FPS = 30

    WINDOW_DIAGONAL = math.sqrt(math.pow(WINDOW_WIDTH, 2) + math.pow(WINDOW_HEIGHT, 2))

    # Player config
    PLAYER_SPRITE_SCALE = .5
    PLAYER_BOOST_SPEED = 15
    PLAYER_TURN_SPEED = math.pi * .02
    PLAYER_AIR_FRICTION = .05
    PLAYER_SHOOT_KNOCKBACK = .5

    # Asteroid config
    ASTEROID_HITS = 3
    ASTEROID_SPRITE_SCALE = (1.4, 1, 0.8)
    ASTEROID_VELOCITY = (4, 6, 8)

    # Projectile config
    PROJECTILE_SPRITE_SCALE = .25
    PROJECTILE_SPEED = 45
    SHOOT_COOLDOWN = .4  # Seconds

    # Score
    SCORE_SYSTEM = (20, 50, 100)

    # Neural Network and Training parameters
    TRAINING = False
    RAY_AMOUNT = 16
    POPULATION_SIZE = 300
    BATCH_SIZE = 50
    ITERATIONS = 1
    
    # File system
    GEN_TAKEN = 52
    SPEC_TAKEN = 1

    # GRAPHICS
    TEXT_COLOR = (240, 240, 192)
    BACK_RECT = (10, 10, 60, 60)
