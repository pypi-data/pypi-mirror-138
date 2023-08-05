

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
from primaryschool.subjects import get_subjects, get_subjects_t, subject_path


app_description =_( "primary school knowledge games" )

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
        self._menu.add.label(app_description, max_char=-1,
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
        self.title = _('Play Game')

        self._menu = self.win.get_default_menu(self.title)

        # index
        self.difficulty = self.win.difficulty
        self.subject = self.win.subject
        self.subject_game = self.win.subject_game

        # subjects, game, difficulties.
        self.subjects = self.win.subjects
        self.difficulties = self.win.difficulties
        self.subjects_t = self.win.subjects_t
        self.difficulties_t = self.win.difficulties_t
        self.subject_games = self.get_subject_games()
        self.subject_games_t = self.get_subject_games_t()

        self.game_dropselect = ...

        self.add_widgets()

    def add_widgets(self):
        self._menu.add.text_input(
            _('Name :'), default=_('_name_'),
            font_name=self.win.font_path)
        self._menu.add.dropselect(
            title=_('Subject :'),
            items=[(name, index)
                   for index, name in enumerate(self.subjects_t)],
            font_name=self.win.font_path,
            default=self.subject,
            placeholder=_('Select a Subject'),
            onchange=self.set_subject
        )
        self.game_dropselect = self._menu.add.dropselect(
            title=_('Game :'),
            items=[(g, index) for index, g in enumerate(
                self.subject_games_t)],
            font_name=self.win.font_path,
            default=self.subject_game if len(self.subject_games) > 0 else None,
            placeholder=_('Select a game'),
            onchange=self.set_game
        )
        self._menu.add.dropselect(
            title=_('Difficulty :'),
            items=[(d, index) for index, d in enumerate(self.difficulties_t)],
            font_name=self.win.font_path,
            default=self.difficulty,
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

    def update_game_dropselect(self):
        self.game_dropselect.update_items(
            [(g, index) for index, g in enumerate(
                self.get_subject_games_t())])
        self.game_dropselect.set_default_value(0)

    def get_subject_games(self):
        game_path = os.path.join(subject_path, self.subjects[self.subject])
        self.subject_games = [d for d in os.listdir(game_path)
                              if d.startswith('g_')]
        return ['null'] if len(self.subject_games) < 1 \
            else self.subject_games

    def get_subject_games_t(self):

        if len(self.subject_games) < 1:
            self.get_subject_games()

        _subject = self.subjects[self.subject]

        trans = []
        for s in self.subject_games:
            _g = importlib.import_module(
                f'primaryschool.subjects.{_subject}.{s}')
            trans.append(_g.name)
        return [_('null')] if len(trans) < 1 else trans

    def start_the_game(self):
        _subject = self.subjects[self.subject]
        _subject_game = self.subject_games[self.subject_game]
        _game_ = importlib.import_module(
            f'primaryschool.subjects.{_subject}.{_subject_game}')
        _game_.play(self.win)
        pass

    def set_difficulty(self, value, difficulty):
        self.difficulty = difficulty

    def set_subject(self, value, subject):
        self.subject = subject
        self.get_subject_games()
        self.update_game_dropselect()

    def set_game(self, value, subject_game):
        self.subject_game = subject_game


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

        self.difficulty = 2
        self.subject = 0

        self.subjects = get_subjects()
        self.difficulties = ['Crazy', 'Hard', 'Middle', 'Easy']

        self.subjects_t = get_subjects_t()
        self.difficulties_t = [_(d) for d in self.difficulties]

        self.subject_games = []
        self.subject_games_t = []
        self.subject_game = 0

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

    def get_difficulty_by_index(self, index=-1):
        index = self.difficulty if index == -1 else index
        return self.difficulties[index]

    def get_subject_by_index(self, index=-1):
        index = self.subject if index == -1 else index
        return self.subjects[index]

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
