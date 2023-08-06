
import os
import sys
from importlib import import_module

from primaryschool.dirs import *
from primaryschool.locale import _

subject_module_prefix = 'primaryschool.subjects.'
subject_dir_path = os.path.abspath(os.path.dirname(__file__))


def get_subject_tree():
    subject_names = []
    game_modules = []
    for _subject in os.listdir(subject_dir_path):
        _subject_path = os.path.join(subject_dir_path, _subject)

        if not os.path.isdir(_subject_path):
            continue
        if _subject.startswith('_'):
            continue

        no_game = True
        for _game in os.listdir(_subject_path):
            if not _game.startswith('g_'):
                continue
            no_game = False
            game_modules.append(subject_module_prefix + _subject + '.' + _game)
        # Subject without game is ignored.
        if not no_game:
            subject_names.append(_subject)
    return subject_names, game_modules


subject_names, game_modules = get_subject_tree()


class Game():
    def __init__(self, module_str, subject):
        self.module_str = module_str
        self.subject = subject
        self.module = import_module(self.module_str)
        self._game = None
        self.name = self.module_str.split('.')[-1]
        self.name_t = self.module.name_t
        self.difficulties = self.module.difficulties

    def get_game(self, win):
        if not self._game:
            self._game = self.module.enjoy(win)
        return self._game

    def play(self, win):
        win.play_menu._menu.disable()
        win.play_menu._menu.full_reset()
        self.get_game(win).play()

    def save(self, win):
        self.get_game(win).save()

    def load(self, win):
        win.play_menu._menu.disable()
        win.play_menu._menu.full_reset()
        self.get_game(win).load()

    def has_copy(self):
        return os.path.exists(get_copy_path(self.module_str))


class Subject():
    def __init__(self, name):
        self.name = name
        self.module = import_module(subject_module_prefix + name)
        self.name_t = self.module.name_t
        self.games = []

    def set_games(self):
        for g in game_modules:
            if g.startswith(subject_module_prefix + self.name):
                self.games.append(Game(g, self))

    def get_games(self):
        if len(self.games) < 1:
            self.set_games()
        return self.games

    def get_name_t(self):
        self.name_t = self.module.name_t
        return self.name_t


class SubjectGame():
    def __init__(self, win):
        pass

    def update():
        pass


subjects = [Subject(n) for n in subject_names]

all_games = sum([s.get_games() for s in subjects], [])
