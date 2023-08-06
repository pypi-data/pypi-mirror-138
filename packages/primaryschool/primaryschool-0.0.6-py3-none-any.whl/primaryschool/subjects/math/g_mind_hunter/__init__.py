import copy
import os
import pickle
import random
import sys
from datetime import datetime, timedelta
from operator import *
from typing import Any, List, Optional, Sequence, Text, Tuple, Union, overload

import pygame
import pygame_menu
from pygame.key import key_code
from pygame.locals import *

from primaryschool.dirs import *
from primaryschool.locale import _
from primaryschool.resource import (default_font, default_font_path,
                                    get_default_font, get_font_path)
from primaryschool.subjects import *
from primaryschool.subjects._templates_ import GameBase

# primaryschool.subjects.yuwen.g_mind_hunter
module_str = __name__

name_t = _('Mind hunter')

difficulties = [
    _('< 10 + 10'),  # 0
    _('< 50 + 50'),  # 1
    _('< 100 + 100'),  # 2
    _('< 10 - 10'),  # 3
    _('< 50 - 50'),  # 4
    _('< 100 - 100'),  # 5
    _('< 10 * 10'),  # 6
    _('< 50 * 50'),  # 7
    _('< 100 * 100'),  # 8
    _('< 10 / 10'),  # 9
    _('< 50 / 50'),  # 10
    _('< 100 / 100'),  # 11
    _('< 10 ? 10'),  # 12
    _('< 50 ? 50'),  # 13
    _('< 100 ? 100'),  # 14
]


class Word():

    def __init__(self, mh):
        self.mh = mh
        self.win = self.mh.win
        self.count = 0
        pass

    def get_pmt_formulas(self, _max, _oper, count=None):  # for plus/minus/time
        f = []
        count = count if count else self.count
        if isinstance(_oper, list):
            for _ in range(self.count + 1):
                f.append(
                    str(random.randint(0, _max)) + ' ' + random.choice(_oper) +
                    ' ' + str(random.randint(0, _max)))
        else:
            for _ in range(self.count + 1):
                f.append(
                    str(random.randint(0, _max)) +
                    ' ' +
                    _oper +
                    ' ' +
                    str(random.randint(0, _max)))

        return f

    def get_division_formulas(self, _max, count=None):
        _d = []
        count = count if count else self.count
        for i in range(_max + 1):
            for j in range(1, _max + 1):
                if i % j == 0:
                    _d.append((i, j))
        return [str(a) + ' / ' + str(b)
                for a, b in random.choices(_d, k=self.count)]

    def set_count(self, count):
        self.count = count

    def get_words(self, d: int = 0, count=20):
        self.set_count(count)
        if d < 15:
            _rem, _quo = d % 3, d // 3

            _max = \
                10 if _rem == 0 else \
                50 if _rem == 1 else \
                100
            _oper = \
                '+' if _quo == 0 else \
                '-' if _quo == 1 else \
                '*' if _quo == 2 else \
                '/' if _quo == 3 else \
                '?'

            if _oper in ['+', '-', '*']:
                return self.get_pmt_formulas(_max, _oper)
            elif _oper == '/':
                return self.get_division_formulas()
            else:
                _d_opers_count = random.choices(
                    ['+', '-', '*', '/'], k=self.count).count('/')

                return self.get_pmt_formulas(_max, ['+', '-', '*']) + \
                    self.get_division_formulas(_max, _d_opers_count)


class Wave():
    def __init__(self, mh):
        self.mh = mh
        self.win = self.mh.win
        self.intercept_interval = \
            self.mh.wordsurfaces_manager.intercept_interval
        self.surface = self.mh.surface
        self.w_height = self.mh.w_height
        self.w_height_of_2 = self.mh.w_height_of_2
        self.w_width_of_2 = self.mh.w_width_of_2
        self.w_centrex_y = self.mh.w_centrex_y
        self.color = (0, 255, 0, 20)
        self.width = 5

        self.max_radius = self.get_max_radius()

    def set_color(self, color):
        self.color = color

    def get_max_radius(self):
        return (self.w_height**2 + self.w_width_of_2**2)**0.5

    def set_width(self, width):
        assert isinstance(width, int)
        self.width = widgets

    def draw(self, frame_counter):
        if frame_counter >= self.intercept_interval:
            return
        _radius = self.max_radius / (self.intercept_interval - frame_counter)
        pygame.draw.circle(self.surface, self.color,
                           self.w_centrex_y, _radius, width=self.width)


class InputSurface():
    def __init__(self, mh):
        self.mh = mh
        self.win = self.mh.win
        self.font_size = 55
        self.font = get_default_font(self.font_size)
        self.font_color = (200, 22, 98)
        self.surface = None
        self.frame_counter = 0

        self.font.set_bold(True)

    def _update(self):
        self.surface = self.font.render(
            self.mh._input, False, self.font_color)

    def blit(self):
        if self.surface is None:
            return
        w, h = self.surface.get_size()
        self.mh.surface.blit(
            self.surface,
            (self.mh.w_width_of_2 - w / 2,
             self.mh.w_height - h))


class WallSurface():
    def __init__(self, mh):
        self.mh = mh
        self.win = self.mh.win
        self.h = self.mh.w_height / 20
        self.surface = pygame.Surface((self.mh.w_width, self.h))
        self.color = (255, 200, 99)
        self.emitter_radius = self.h / 2
        self.emitter_color = None

        self.center = self.get_center()

    def set_emitter_color(self, color=(255, 0, 0, 50)):
        self.emitter_color = color

    def get_emitter_color(self):
        return self.emitter_color

    def get_center(self):
        return [self.win.w_width_of_2, self.win.w_height - self.h / 2]

    def draw_emitter(self):
        self.emitter_color = self.set_emitter_color() \
            if self.mh.wordsurfaces_manager is None \
            else self.mh.wordsurfaces_manager.laser_color
        pygame.draw.circle(self.win.surface, self.emitter_color,
                           self.center, self.emitter_radius)

    def blit(self):
        self.surface.fill(self.color)
        self.mh.surface.blit(self.surface, (0, self.mh.w_height - self.h))
        self.draw_emitter()


class WordSurfacesManager():
    def __init__(self, mh, frame_counter=0):
        self.mh = mh
        self.win = self.mh.win
        self.moving_surfaces = []
        self.frame_counter = frame_counter
        self.difficulty_index_p1  = self.mh.difficulty_index+1
        self.interval = 1.8 * self.mh.FPS # * \
            # (self.difficulty_index_p1 + 5) / len(difficulties)
        self.intercept_interval = 0.3 * self.mh.FPS
        self.moving_speed = 1
        self.intercepted_color = (175, 10, 175, 100)
        self.laser_color = (0, 0, 255, 90)
        self.laser_width = 2
        self.font_size = 50
        self.lang_code = 'zh_CN'
        self.font_path = get_font_path(self.lang_code, show_not_found=True)
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.surfaces = []

    def set_font_size(self, size):
        assert isinstance(size, int)
        self.font_size = size

    def get_font_size(self):
        return self.font_size

    def set_surfaces(self):
        assert len(self.mh.words) > 0
        self.surfaces = [WordSurface(self.mh, self, w) for w in self.mh.words]

    def get_surfaces(self):
        if not self.surfaces:
            self.set_surfaces()
        return self.surfaces

    def count(self):
        return len(self.surfaces)

    def get_random_surface(self):
        random_ws = self.surfaces[
            random.randint(0, self.count - 1)]
        return random_ws.copy()

    def pop_surface(self):
        return self.surfaces.pop()

    def add_moving_surfaces(self):
        ws = self.pop_surface()
        self.moving_surfaces.append(ws)
        self.frame_counter = 0

    def save(self, _copy):
        _copy['0x0'] = [s.word for s in self.surfaces]
        _copy['0x1'] = [(ms.word, ms.dest) for ms in self.moving_surfaces]
        return _copy

    def load(self, _copy):
        for w in _copy['0x0']:
            self.surfaces.append(WordSurface(self.mh, self, w))
        for w, d in _copy['0x1']:
            self.moving_surfaces.append(WordSurface(self.mh, self, w, d))

    def blit(self):
        if len(self.surfaces) > 0:
            if len(self.moving_surfaces) < 1:
                self.add_moving_surfaces()

            if self.frame_counter >= self.interval:
                self.add_moving_surfaces()

        for w in self.moving_surfaces:

            if w.intercepted:
                if w.intercept_frame_counter >= self.intercept_interval:
                    self.moving_surfaces.remove(w)
                self.mh.wave.draw(w.intercept_frame_counter)
                w.surface = w.font.render(
                    w.word, False, self.intercepted_color)
                self.mh.surface.blit(w.surface, w.dest)
                w.circle()
                w.draw_laser_line()
                w.intercept_frame_counter += 1
                continue

            if w.intercept(self.mh._input):
                self.mh._input = ''
                self.mh.input_surface._update()
                self.mh.surface.blit(w.surface, w.dest)
                self.mh.win_count += 1
                continue

            if w.arrived():
                self.moving_surfaces.remove(w)
                self.mh.lose_count += 1
                continue

            w.add_dest((0, self.moving_speed))
            self.mh.surface.blit(w.surface, w.dest)

        self.frame_counter += 1


class InfoSurface():
    def __init__(self, mh):
        self.mh = mh
        self.win = mh.win
        self.surface = self.win.surface
        self.game_info_dest = (10, 10)
        self.game_info = name_t + \
            '/' + difficulties[self.win.difficulty_index]
        self.game_info_color = (255, 0, 255, 10)
        self.font_size = 25
        self.font = get_default_font(self.font_size)

        self.score_font_size = 66
        self.score_font = get_default_font(self.score_font_size)

        self.datetime_diff_font_size = 50
        self.datetime_diff_font = get_default_font(
            self.datetime_diff_font_size)
        self.datetime_diff_font_color = ...

        self.font = get_default_font(self.font_size)

        self.game_info_surface = self.font.render(
            self.game_info, False, self.game_info_color)

        self.score = 0
        self._pass = False
        self.win_info_surface = ...

        self.score_surface = ...
        self.datetime_diff_surface = ...
        self.greeting_surface = ...

        self.end_time = self.win.end_time = None

    def get_score_font_color(self):
        return (20, 255, 0) if self._pass else (255, 20, 0)

    def get_win_info(self):
        return _('win: ') + str(self.mh.win_count) + '|' + _('lose: ') +\
            str(self.mh.lose_count) + '|' + _('remain: ') +\
            str(self.mh.wordsurfaces_manager.count()) + '|' +\
            _('total: ') + str(self.mh.word_count)

    def get_win_info_dest(self):
        _w, _ = self.win_info_surface.get_size()
        return [self.win.w_width - _w, 0]

    def get_datetime_diff_str(self):
        if self.end_time is None:
            self.end_time = self.win.end_time = datetime.now()
        diff = self.end_time - self.pm.start_time + self.pm.last_timedelta
        _h, _rem = divmod(diff.seconds, 3600)
        _min, _sec = divmod(_rem, 60)
        return _('Cost: ') + f'{_h}:{_min}:{_sec}'

    def blit(self):
        self.win_info_surface = self.font.render(
            self.get_win_info(), False, self.game_info_color)

        self.surface.blit(self.game_info_surface, self.game_info_dest)
        self.surface.blit(self.win_info_surface, self.get_win_info_dest())

    def get_score(self):
        self.score = int(100 * self.mh.win_count / self.mh.word_count)
        return self.score

    def get_score_pass(self):
        self._pass = self.score > 60
        return self._pass

    def get_greeting(self):
        return _('Success!') if self._pass \
            else _('Practice makes perfect, keep trying!')

    def get_score_str(self):
        return _('Score: ') + str(self.score)

    def get_greeting_dest(self):
        _w, _h = self.greeting_surface.get_size()
        _, _s_h = self.score_surface.get_size()
        return [
            self.win.w_width_of_2 - _w / 2,
            self.win.w_height_of_2 - _h - _s_h
        ]

    def get_score_surface_dest(self):
        _w, _h = self.score_surface.get_size()
        return [
            self.win.w_width_of_2 - _w / 2,
            self.win.w_height_of_2 - _h
        ]

    def get_datetime_diff_surface_dest(self):
        _w, _h = self.datetime_diff_surface.get_size()
        return [
            self.win.w_width_of_2 - _w / 2,
            self.win.w_height_of_2 + _h
        ]

    def score_blit(self):
        self.score = self.get_score()
        self.get_score_pass()

        self.greeting_surface = self.score_font.render(
            self.get_greeting(),
            False,
            self.get_score_font_color()
        )

        self.score_surface = self.score_font.render(
            self.get_score_str(),
            False,
            self.get_score_font_color())

        self.datetime_diff_surface = self.datetime_diff_font.render(
            self.get_datetime_diff_str(),
            False,
            self.get_score_font_color())

        self.surface.blit(
            self.greeting_surface,
            self.get_greeting_dest())

        self.surface.blit(
            self.score_surface,
            self.get_score_surface_dest())

        self.surface.blit(
            self.datetime_diff_surface,
            self.get_datetime_diff_surface_dest())


class WordSurface():
    def __init__(self, mh, _manager, word, dest=None):
        self.mh = mh
        self.win = self.mh.win
        self.manager = _manager
        self.wall_surface = None
        self.word = word
        self.font_color = (200, 22, 98)
        self.font = self.manager.font
        self.circle_color = (100, 20, 25, 20)
        self.circle_width = 4
        self.intercepted = False
        self.intercept_frame_counter = 0
        self.laser_color = self.manager.laser_color
        self.laser_width = self.manager.laser_width

        self.surface = self.get_surface()
        self.size = self.get_size()
        self.dest = dest if dest else self.get_random_dest()
        self.center = self.get_center()
        self.result = self.get_result()

    def set_circle_color(self, color):
        self.circle_color = color

    def set_circle_width(self, width):
        assert isinstance(width, int)
        self.circle_width = width

    def arrived(self):
        return self.get_y() + self.get_h() >= \
            self.mh.w_height - self.mh.wall_surface.h

    def get_surface(self):
        return self.font.render(self.word, False, self.font_color)

    def set_dest(self, dest):
        self.dest = dest

    def get_x(self):
        return self.dest[0]

    def get_y(self):
        return self.dest[1]

    def get_w(self):
        return self.size[0]

    def get_h(self):
        return self.size[1]

    def add_dest(self, _add):
        self.dest[0] += _add[0]
        self.dest[1] += _add[1]
        self.center = self.get_center()

    def set_laser_color(self, laser_color):
        self.laser_color = laser_color

    def get_laser_color():
        return self.laser_color

    def draw_laser_line(self):
        if self.wall_surface is None:
            self.wall_surface = self.mh.wall_surface
        assert self.wall_surface is not None
        pygame.draw.line(
            self.win.surface, self.laser_color,
            self.wall_surface.center, self.center,
            self.laser_width)

    def get_center(self):
        return [
            self.get_x() + self.get_w() / 2,
            self.get_y() + self.get_h() / 2
        ]

    def get_circle_radius(self):
        return self.get_w() / 2

    def circle(self):
        pygame.draw.circle(self.mh.surface, self.circle_color,
                           self.center, self.get_circle_radius(),
                           width=self.circle_width)

    def intercept(self, _result):
        self.intercepted = str(self.result) == _result
        return self.intercepted

    def get_result(self):
        a, oper, b = self.word.split(' ')
        return \
            int(a) + int(b) if oper == '+' else \
            int(a) - int(b) if oper == '-' else \
            int(a) * int(b) if oper == '*' else \
            int(int(a) / int(b))

    def get_size(self):
        return self.surface.get_size()

    def set_random_dest(self):
        self.dest = self.get_random_dest()

    def get_random_dest(self):
        return [random.randint(0, self.mh.w_width - self.get_w()), 0]

    def copy(self):
        _new = copy.copy(self)
        _new.surface = self.surface.copy()
        _new.set_random_dest()
        return _new


class MindHunter(GameBase):
    def __init__(self, win):

        self.win = win

        # window
        self.w_width = self.win.w_width
        self.w_height = self.win.w_height
        self.w_height_of_2 = self.win.w_height_of_2
        self.w_width_of_2 = self.win.w_width_of_2
        self.w_centrex_y = self.win.w_centrex_y
        self.running = True
        self.FPS = self.win.FPS
        self.clock = self.win.clock
        self._load = False

        self.subject = self.win.subject
        self.subject_index = self.win.subject_index
        self.subject_game_index = self.win.subject_game_index
        self.difficulty_index = self.win.difficulty_index

        self.main_menu = self.win.main_menu
        self.play_menu = self.win.play_menu
        self.save_menu = self.win.save_menu
        self.surface = self.win.surface

        self._input = ''
        self.font = get_default_font(45)
        self.info_surface = InfoSurface(self)
        self.wall_surface = WallSurface(self)
        self.input_surface = InputSurface(self)

        # word surface
        self.word = Word(self)
        self.words = self.word.get_words(self.difficulty_index)
        self.wordsurfaces_manager = WordSurfacesManager(self)

        self.wave = Wave(self)

        self.win_count = 0
        self.lose_count = 0
        self.word_count = len(self.words)

        self.copy_path = get_copy_path(module_str)

        self.print_game_info()

        self.last_timedelta = timedelta(0)

        self.start_time = datetime.now()
        self.end_time = None

    def print_game_info(self):
        print(self.subject.name_t, name_t, difficulties[self.difficulty_index])

    def ascii_is_num(self, code):
        return 48 <= code <= 57 or code == 45

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.save_menu._menu.enable()
                    self.save_menu._menu.mainloop(self.surface)
                    return
                elif e.key == pygame.K_BACKSPACE:
                    self._input = self._input[0:-1]
                    self.input_surface._update()
                    return
                elif self.ascii_is_num(e.key):
                    self._input += pygame.key.name(e.key)
                    self.input_surface._update()
                    return

    def load(self):
        try:
            self._load = True
            with open(self.copy_path, 'rb') as f:
                _copy = pickle.load(f)
            self.wordsurfaces_manager.load(_copy)
            self.word_count, self.win_count, self.lose_count = _copy['0x2']
            self.last_timedelta = _copy['0x3']
            self.start()
        except e:
            print(e)

    def save(self):
        _copy = {}
        self.wordsurfaces_manager.save(_copy)
        _copy['0x2'] = (self.word_count, self.win_count, self.lose_count)
        _copy['0x3'] = (datetime.now() - self.start_time) + self.last_timedelta

        # https://docs.python.org/3/library/pickle.html?highlight=pickle
        # Warning:
        # The pickle module is not secure. Only unpickle data you trust.
        with open(self.copy_path, 'wb') as f:
            pickle.dump(_copy, f)

    def _start(self):

        if not self._load:
            self.wordsurfaces_manager.set_surfaces()

    def play(self):
        self._load = False
        self.wordsurfaces_manager.surfaces = []
        self.wordsurfaces_manager.set_surfaces()
        self.start()

    def start(self):

        self._start()

        while self.running:
            self.clock.tick(self.FPS)

            self.surface.fill((0, 0, 0))

            events = pygame.event.get()
            self.handle_events(events)
            if self.main_menu._menu.is_enabled():
                self.main_menu._menu.update(events)

            if self.play_menu._menu.is_enabled():
                self.play_menu._menu.update(events)

            if self.win_count + self.lose_count < self.word_count:
                self.info_surface.blit()
                self.wall_surface.blit()
                self.wordsurfaces_manager.blit()
                self.input_surface.blit()
            else:
                self.info_surface.score_blit()

            pygame.display.update()


def enjoy(win):
    return MindHunter(win)
