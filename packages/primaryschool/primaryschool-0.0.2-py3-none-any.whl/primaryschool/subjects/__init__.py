
import importlib
import os
import sys

from primaryschool.locale import _

subject_path = os.path.abspath(os.path.dirname(__file__))


def get_subjects():
    return [p for p in os.listdir(subject_path) if not p.startswith('__')]


def get_subjects_t():
    return [
        importlib.import_module(f'primaryschool.subjects.{m}').name
        for m in get_subjects()
    ]


class SubjectGame():
    def __init__(self, win):
        # print(win.subject, win.difficulty, win.subject_game)
        ...

    def update():
        pass
