
import os
import sys
from importlib import import_module

from primaryschool.locale import _

subject_module_prefix = 'primaryschool.subjects.'
subject_dir_path = os.path.abspath(os.path.dirname(__file__))


def get_subject_names():
    subjects = []
    for _subject in os.listdir(subject_dir_path):
        _subject_path = os.path.join(subject_dir_path, _subject)
        if not os.path.isdir(_subject_path):
            continue
        if _subject.startswith('_'):
            continue
        subjects.append(_subject)
    return subjects


subject_names = get_subject_names()


def get_game_modules():
    modules = []
    for _subject_name in subject_names:
        _subject_path = os.path.join(subject_dir_path, _subject_name)
        for _game in os.listdir(_subject_path):
            if not _game.startswith('g_'):
                continue
            modules.append(f'{subject_module_prefix+_subject_name}.{_game}')
    return modules


game_modules = get_game_modules()


class Game():
    def __init__(self, module_str, subject):
        self.module_str = module_str
        self.subject = subject
        self.module = import_module(self.module_str)
        self.name = self.get_name()
        self.name_t = self.get_name_t()
        self.difficulties = self.get_difficulties()

    def get_difficulties(self):
        return self.module.difficulties

    def get_name_t(self):
        return self.module.name_t

    def get_name(self):
        return self.module_str.split('.')[-1]

    def play(self, win):
        from primaryschool.ready import Win
        assert isinstance(win, Win)

        self.module.play(win)


class Subject():
    def __init__(self, name):
        self.name = name
        self.module = import_module(subject_module_prefix + name)
        self.name_t = self.get_name_t()
        self.games = self.get_games()

    def get_games(self):
        games = []
        for g in game_modules:
            if g.startswith(subject_module_prefix + self.name):
                games.append(Game(g, self))
        return games

    def get_name_t(self):
        return self.module.name_t


class SubjectGame():
    def __init__(self, win):
        pass

    def update():
        pass


subjects = [Subject(n) for n in subject_names]

games = sum([s.games for s in subjects], [])
