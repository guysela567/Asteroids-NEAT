from __future__ import annotations
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # Get rid of pygame support message

# Import modules for easier access
from utils.drawing.canvas import Canvas
from utils.drawing.image import Image
from utils.drawing.screen import Screen
from utils.drawing.screen_manager import ScreenManager
from utils.drawing.widgets import Button, TextBox