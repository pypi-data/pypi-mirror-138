
import importlib
import os

import pygame
import pygame_menu
from pygame.locals import *
from pygame_menu.widgets import *

project_path = os.path.abspath(os.path.dirname(__file__))


def victory():
    from primaryschool import ready
    ready.go()
    pass
