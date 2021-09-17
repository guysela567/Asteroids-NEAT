import math


class Constants:
    # Window config
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    WINDOW_TITLE = 'Asteroids'

    # Player config
    PLAYER_SPRITE_SCALE = .5
    PLAYER_BOOST_SPEED = 7
    PLAYER_TURN_SPEED = math.pi * .02
    PLAYER_AIR_FRICTION = .05
    PLAYER_SHOOT_KNOCKBACK = .5

    # Asteroid config
    ASTEROID_HITS = 3
    ASTEROID_SPRITE_SCALE = (.4, .3, .2)
    ASTEROID_VELOCITY = (2, 3, 5)

    # Bullet config
    BULLET_SPRITE_SCALE = 0.5
    BULLET_SPEED = 15
    SHOOT_COOLDOWN = .25  # Seconds

    # Score
    SCORE_SYSTEM = (20, 50, 100)
