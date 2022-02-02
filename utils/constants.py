import math


class Constants:
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

    # AI
    TRAINING = True
    RAY_AMOUNT = 8
    POPULATION_SIZE = 50 if TRAINING else 1
    STARTING_CONNECTIONS = 0

    # COLORS
    TEXT_COLOR = (240, 240, 192)
