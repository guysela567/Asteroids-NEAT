from __future__ import annotations

from utils.constants import Constants
from utils.geometry.raycasting import RaySet
from utils.geometry.collision import SpriteDimensions, Hitbox
from utils.drawing import Button, Screen, Image

from components.player import Player
from components.asteroid import Asteroid

from src.controller import Controller

import random
import math


class GameScreen(Screen):
    '''Graphical screen for viewing the asteroids game'''

    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, Constants.WINDOW_TITLE)
        
        self.__sprites = {
            'asteroid': [Image(f'assets/sprites/asteroid{i}.png') for i in range(1, 4)],
            'player': [Image('assets/sprites/player.png')],
            'projectile': [Image('assets/sprites/projectile.png')]
        }

        self.__title_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 100)
        self.__button_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 50)
        self.__pause_image = Image('assets/sprites/pause.png')
        self.__resume_image = Image('assets/sprites/resume.png')

        self.__pause_pos = (self.width - 100, 50)
        self.__pause_dims = (50, 50)

        self.__resume_button = Button(self, 0, 450, 300, 100, (255, 255, 255), 'Resume')
        self.__quit_button = Button(self, 0, 600, 300, 100, (255, 255, 255), 'Quit')

        self.__animations: dict[str, int] = {}
        self.reset_animations()

        self.__thrust_image = Image.load_by_scale('assets/sprites/thrust.png', 3)

        for sprite, images in self.__sprites.items():
            dims = [image.size for image in images]
            SpriteDimensions.dimensions[sprite] = dims

        self.__controller = Controller()

        # Graphical setup
        self.no_stroke()

        # Generate stars for background
        self.__stars = [(random.uniform(0, self.width),
                         random.uniform(0, self.height),
                         random.uniform(1, 3)) for _ in range(50)]

        self.__score_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 36)

    def draw(self) -> None:
        '''Updates graphics'''

        self.draw_background()
        self.draw_sprites(self.__controller.player, self.__controller.asteroids)
        self.draw_score(self.__controller.score, self.__controller.high_score)

        if self.__controller.paused:
            self.draw_paused()

        self.draw_pause_resume()

    def draw_pause_resume(self) -> None:
        '''Draws the pause/resume button'''
        image = self.__resume_image if self.__controller.paused else self.__pause_image
        self.image(image, *self.__pause_pos, *self.__pause_dims)

    def update(self) -> None:
        '''Updates the game controller'''
        self.__controller.update()

    def on_key_down(self, key: int, unicode: str) -> None:
        '''Handles key down events
        :param key: id of the pressed key
        :param unicode: unicode of the pressed key
        '''
        
        if key == self.keys['ESCAPE']:
            self.redirect('menu')

        # Disabled for AI mode
        if not self.__controller.ai_playing:
            if key == self.keys['p']:
                self.__controller.toggle_pause()
                self.reset_animations()

            elif key == self.keys['UP']:
                self.__controller.start_boost()

            elif key == self.keys['RIGHT']:
                self.__controller.start_rotate(1)

            elif key == self.keys['LEFT']:
                self.__controller.start_rotate(-1)

            elif key == self.keys['SPACE']:
                self.__controller.shoot()

    def on_key_up(self, key: int) -> None:
        '''Handles key release events
        :param key: id of the released key
        '''

        # Disabled for AI mode
        if not self.__controller.ai_playing:
            if key == self.keys['UP']:
                self.__controller.stop_boost()

            elif key == self.keys['RIGHT'] and self.__controller.player.rotate_dir == 1 \
                    or key == self.keys['LEFT'] and self.__controller.player.rotate_dir == -1:
                self.__controller.stop_rotate()

    def on_mouse_down(self) -> None:
        '''Handles mouse down events'''
        if self.__pause_pos[0] < self.mouse_pos[0] < self.__pause_pos[0] + self.__pause_dims[0] \
            and self.__pause_pos[1] < self.mouse_pos[1] < self.__pause_pos[1] + self.__pause_dims[1]:
            self.__controller.toggle_pause()
            self.reset_animations()

        if self.__controller.paused:
            if self.__resume_button.mouse_hover():
                self.__controller.toggle_pause()
                self.reset_animations()

            if self.__quit_button.mouse_hover():
                self.redirect('menu')

    def draw_background(self) -> None:
        '''Draws the background, including the stars'''

        # Clear screen to background color
        self.background(0)

        # Draw stars
        self.fill(255)
        for x, y, size in self.__stars:
            self.circle(x, y, size)

    def draw_sprites(self, player: Player, asteroids: list[Asteroid]) -> None:
        '''Draws the player and the asteroid sprites on the screen
        :param player: the game player
        :param asteroids: list of the game asteroids
        '''

        self.draw_sprite('player', player.hitbox, player.angle)  # Draw player

        # Draw asteroids
        for asteroid in asteroids:
            self.draw_sprite('asteroid', asteroid.hitbox, asteroid.angle)

        # Draw projectiles
        for projectile in player.projectiles:
            self.draw_sprite('projectile', projectile.hitbox, projectile.angle, projectile.alpha)

        # Draw thrust
        self.draw_thurst(player)

        # # Draw rays
        # self.draw_rays(player.ray_set)
        # self.fill(255)

    def draw_thurst(self, player: Player) -> None:
        '''Draws the thrust image behind the player
        :param player: the game player
        '''

        if player.boosting:
            r = player.hitbox.height * .5 + 7.5
            x = player.hitbox.pos.x + r * math.cos(player.angle_radians)
            y = player.hitbox.pos.y + r * math.sin(player.angle_radians)

            thrust = Image.rotate(self.__thrust_image, player.angle)
            self.image(thrust, *thrust.get_rect((x, y)))

    def draw_score(self, score: int, high_score: int) -> None:
        '''Draws score and high score on the screen
        :param score: the current score
        :param high_score: all-time high score'''
        self.set_font(self.__score_font)

        # Draw score
        self.text(f'SCORE: {score}', 25, 100)

        # Draw high score
        self.text(f'HIGH SCORE: {high_score}', 25, 25)
    
    def reset_animations(self) -> None:
        '''Resets all animations'''
        self.__animations = {
            'blur': 0,
            'pause_title': -200,
            'pause_buttons': -800,
        }

    def apply_pause_animation(self) -> None:
        '''Starts the pause animation'''
        if self.__animations['blur'] < 200: 
            self.__animations['blur'] += 50
        if self.__animations['pause_title'] < 200:
            self.__animations['pause_title'] += 50
        if self.__animations['pause_buttons'] < self.width * .5 - 150:
            self.__animations['pause_buttons'] += 50

    def draw_paused(self) -> None:
        '''Draws the screen in paused mode'''
        self.apply_pause_animation()
        self.blur(self.__animations['blur'])
        self.fill(255)

        self.set_font(self.__title_font)
        self.text('GAME PAUSED', self.width * .5, self.__animations['pause_title'], center=True)

        self.set_font(self.__button_font)
        self.__resume_button.x = self.__animations['pause_buttons']
        self.__quit_button.x = self.__animations['pause_buttons']
        self.__resume_button.draw()
        self.__quit_button.draw()

    def draw_sprite(self, component: str, hitbox: Hitbox, angle: float, alpha: int = 255) -> None:
        '''Draws a given sprite on the screen
        :param component: name of the sprite
        :param hitbox: the hitbox of the sprite
        :param angle: the angle in which to rotate the sprite
        :param alpha: the opacity for the sprite'''

        raw_image = self.__sprites[component][hitbox.index]
        image = Image.rotate(Image.resize(raw_image, hitbox.width, hitbox.height), angle)

        temp = image.alpha
        image.alpha = alpha
        self.image(image, *image.get_rect(tuple(hitbox.pos)))
        image.alpha = temp # Revert to normal opacity to prevent affecting cached images

    def draw_rays(self, ray_set: RaySet) -> None:
        '''Draws the vision rays on screen'''
        for ray in ray_set:
            if ray.is_looped:
                self.fill(200, 150, 0)
                self.line(*ray.looped, 5)
                self.fill(100, 255, 255)
                self.line(*ray.infinite, 5)
            else:
                if ray.hit: self.fill(255, 0, 255)
                else: self.fill(0, 255, 0)
                self.line(*ray, 5)


    def draw_poly(self, verts: list[tuple[float, float]]) -> None:
        '''Draws a polygon from given list of vertecies
        :param verts: list of coordinate tuples representing the polygon vertecies
        '''

        for i in range(len(verts)):
            pos1 = verts[i]
            pos2 = verts[i + 1] if i < len(verts) - 1 else verts[0]
            self.line(*pos1, *pos2, 5)

    def switch_reset(self) -> None:
        '''Resets the screen for every screen-switch'''
        self.__controller.reset()

    def recieve_data(self, data: dict) -> None:
        '''Handles data sent by other screens and sets the AI mode accordingly'''
        self.__controller.set_ai(data['ai_playing'])

    @property
    def controller(self) -> Controller:
        return self.__controller

    @controller.setter
    def controller(self, controller: Controller) -> None:
        self.__controller = controller