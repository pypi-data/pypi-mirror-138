

import importlib
import os

import pygame
import pygame_menu
from pygame.locals import *
from pygame_menu.widgets import *

from primaryschool.locale import _
from primaryschool.resource import (default_font, default_font_path,
                                    get_default_font)
from primaryschool.settings import *
from primaryschool.subjects import games, subjects

app_description_t = _("app_description_t")


class AboutMenu():

    def __init__(self, win):

        self.win = win
        self.title = _('About')
        self._menu = self.win.get_default_menu(self.title)
        self.app_name_font = get_default_font(50)
        self.app_version_font = get_default_font(20)
        self.app_description_font = get_default_font(22)
        self.app_url_font = get_default_font(20)
        self.app_author_font = get_default_font(22)
        self.app_contributors_font = self.app_author_font

        self.add_widgets()

    def add_widgets(self):
        self._menu.add.label(app_name, max_char=-1,
                             font_name=self.app_name_font)
        self._menu.add.label(app_version, max_char=-1,
                             font_name=self.app_version_font)
        self._menu.add.label(app_description_t, max_char=-1,
                             font_name=self.app_description_font)
        self._menu.add.url(app_url, font_name=self.app_url_font)
        self._menu.add.label(_('Author'), max_char=-1,
                             font_name=get_default_font(32))
        self._menu.add.label(app_author, max_char=-1,
                             font_name=self.app_author_font)
        self._menu.add.label(_('Contributors'), max_char=-1,
                             font_name=get_default_font(32))
        self._menu.add.label('\n'.join(app_contributors[1:]),
                             max_char=-1, font_name=self.app_contributors_font)
        self._menu.add.button(
            _('Return to main menu'),
            pygame_menu.events.BACK,
            font_name=self.win.font_path)


class PlayMenu():
    def __init__(self, win):

        self.win = win
        self.subjects = self.win.subjects
        self.games = self.win.games

        self.win.subject_index = self.get_default_subject_index()
        self.subject_index = self.win.subject_index
        self.game_index = self.win.game_index
        self.difficulty_index = self.win.difficulty_index

        self.title = _('Play Game')
        self._menu = self.win.get_default_menu(self.title)

        self.game_dropselect = ...

        self.add_widgets()

    def add_widgets(self):
        self._menu.add.text_input(
            _('Name :'), default=_('_name_'),
            font_name=self.win.font_path)

        self._menu.add.dropselect(
            title=_('Subject :'),
            items=[(s.name_t, index)for index, s in enumerate(self.subjects)],
            font_name=self.win.font_path,
            default=self.get_default_subject_index(),
            placeholder=_('Select a Subject'),
            onchange=self.set_subject
        )
        self.game_dropselect = self._menu.add.dropselect(
            title=_('Game :'),
            items=[(g.name_t, index) for index, g in enumerate(self.games)],
            font_name=self.win.font_path,
            default=self.game_index,
            placeholder=_('Select a game'),
            onchange=self.set_game
        )

        self._menu.add.dropselect(
            title=_('Difficulty :'),
            items=[(d, index) for index, d in
                   enumerate(self.games[0].difficulties)],
            font_name=self.win.font_path,
            default=self.difficulty_index,
            placeholder=_('Select a difficulty'),
            onchange=self.set_difficulty
        )

        self._menu.add.button(
            _('Play'),
            self.start_the_game,
            font_name=self.win.font_path)

        self._menu.add.button(
            _('Return to main menu'),
            pygame_menu.events.BACK,
            font_name=self.win.font_path)

    def get_default_subject_index(self):
        return self.subjects.index(self.games[0].subject)

    def update_game_dropselect(self):
        self.game_dropselect.update_items(
            [(g.name_t, index) for index, g in enumerate(
                self.subjects[self.subject_index].games)])
        self.game_dropselect.set_default_value(0)

    def start_the_game(self):
        self.games[self.game_index].play(self.win)

    def set_difficulty(self, value, index):
        self.difficulty_index = self.win.difficulty_index = index

    def set_subject(self, item, index):
        self.subject_index = self.win.subject_index = index
        self.game_index = 0
        self.update_game_dropselect()

    def set_game(self, item, index):
        self.game_index = self.win.game_index = index


class MainMenu():
    def __init__(self, win):
        self.win = win
        self.title = _('Primary School')
        self._menu = self.win.get_default_menu(self.title)
        self.play_menu = PlayMenu(self.win)
        self.about_menu = AboutMenu(self.win)

        self.add_widgets()

    def add_widgets(self):
        self._menu.add.button(_('Play'), self.play_menu._menu,
                              font_name=self.win.font_path,)
        self._menu.add.button(_('About'), self.about_menu._menu,
                              font_name=self.win.font_path,)
        self._menu.add.button(_('Quit'), pygame_menu.events.EXIT,
                              font_name=self.win.font_path,)


class Win():
    def __init__(self):

        pygame.init()

        self.running = True

        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.w_width, self.w_height = self.surface.get_size()
        self.w_width_of_2, self.w_height_of_2 = self.w_width / 2, \
            self.w_height / 2
        self.w_centrex_y = [self.w_width_of_2, self.w_height]
        self.FPS = 30
        self.clock = pygame.time.Clock()

        self.subjects = subjects
        self.games = games

        self.subject_index = 0
        self.game_index = 0
        self.difficulty_index = 0

        self.font_path = default_font_path
        self.font = default_font

        self.main_menu = MainMenu(self)

    def get_default_menu(self, title, **kwargs):

        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.title_font = self.font
        return pygame_menu.Menu(title, self.w_width, self.w_height,
                                theme=theme, **kwargs)

    def clear_screen(self):
        self.surface.fill((255, 255, 255))
        pygame.display.update()

    def run(self):

        while self.running:
            self.clock.tick(self.FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            if self.main_menu._menu.is_enabled():
                self.main_menu._menu.mainloop(self.surface)

            pygame.display.flip()


def go():
    Win().run()
    pass
