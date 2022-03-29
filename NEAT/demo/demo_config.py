from utils.drawing import Image, Screen, TextBox, Button
from utils.constants import Constants


class DemoConfigScreen(Screen):
    '''Graphical screen for selecting options and sending them to the demo screen'''

    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, 'Topology Demo Configuration')
        
        self.__title_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 100)
        self.__regular_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 40)

        self.__inputs_box = TextBox(self, self.width - 200, 475, 50, 50)
        self.__outputs_box = TextBox(self, self.width - 180, 575, 50, 50)
        self.__button = Button(self, 50, self.height - 130, 250, 100, (255, 255, 255), 'Continue')

        self.__back_image = Image('assets/sprites/back.png')

    def draw(self) -> None:
        '''Updates graphics'''

        self.background(0)
        self.fill(255)

        self.image(self.__back_image, *Constants.BACK_RECT)

        self.set_font(self.__title_font)
        self.text('Configure', self.width * .5, 100, center=True)
        self.text('Genome Shape', self.width * .5, 200, center=True)

        self.set_font(self.__regular_font)
        self.text('Please Enter Number Of Inputs:', 50, 475)
        self.text('Please Enter Number Of Outputs:', 50, 575)

        self.__inputs_box.draw()
        self.__outputs_box.draw()
        self.__button.draw()

    def on_key_down(self, key: int, unicode: int) -> None:
        '''Handles key dowm events
        :param key: id of the pressed key
        :param unicode: unicode of the key
        '''

        self.__inputs_box.handle_keydown(key, unicode)
        self.__outputs_box.handle_keydown(key, unicode)

        if key == self.keys['ESCAPE']:
            self.redirect('demo-select')

    def on_mouse_down(self) -> None:
        '''Handles mouse press events'''

        self.__inputs_box.handle_mousedown(self.mouse_pos)
        self.__outputs_box.handle_mousedown(self.mouse_pos)

        x, y, w, h = Constants.BACK_RECT
        if x < self.mouse_pos[0] < x + w and y < self.mouse_pos[1] < y + h:
            self.redirect('demo-select')

        ins, outs = self.__inputs_box.value, self.__outputs_box.value
        if self.__button.mouse_hover():
            if ins.isdigit() and outs.isdigit():
                self.redirect('topology-demo', { 'inputs': int(ins), 'outputs': int(outs) })

    def switch_reset(self) -> None:
        '''Resets the screen for every screen-switch'''
        self.__inputs_box.clear()
        self.__outputs_box.clear()