
import os
import sys

import pygame

from primaryschool import project_path
from primaryschool.locale import _, sys_lang_code

resource_path = os.path.abspath(os.path.dirname(__file__))
project_font_path = os.path.join(resource_path, 'fonts')


class Resource():
    def __init__(self):

        self.default_font_size = 25
        self.sys_font_names = pygame.font.get_fonts()
        self.locale_font_paths = self.get_locale_font_paths()
        self.material_dir_names = ['imgs', 'audios', 'fonts']
        self.material_file_names = self.get_material_file_names()

    def get_sys_font_name_like(self, _like_name):
        for f in self.sys_font_names:
            if _like_name.lower() in f.lower():
                return f
        return self.sys_font_names[0]

    def get_font_path(self, lang_code='', show_not_found=False):
        lang_code = sys_lang_code if len(lang_code) < 1 else lang_code
        for k, v in self.locale_font_paths.items():
            if lang_code == k:
                return v

        if show_not_found:
            from tkinter import Tk, messagebox

            root = Tk()
            messagebox.showerror(
                _('No font found'),
                _('Could not find font of %s.') % lang_code)
            root.destroy()

        return self.locale_font_paths['default']

    def get_material_file_names(self):
        material_file_names = []
        for root, _, files in os.walk(project_path, topdown=False):
            for n in self.material_dir_names:
                if root.endswith(n):
                    for name in files:
                        material_file_names.append(os.path.join(root, name))
        return sorted(material_file_names, key=len)

    def get_material(self, name):
        for f in self.material_file_names:
            locale_material = f'{sys_lang_code}/{name}'
            if f.endswith(locale_material):
                return f

    def get_locale_font_paths(self):
        return {
            'default': pygame.font.match_font(
                self.get_sys_font_name_like('mono')),
            'zh_CN': pygame.font.match_font(
                self.get_sys_font_name_like('cjk')),
        }


pygame.font.init()

r = Resource()
font_path = r.get_font_path()
font = pygame.font.Font(font_path, r.default_font_size)


def get_font_path(lang_code, show_not_found=False):
    return r.get_font_path(lang_code, show_not_found=False)


def get_material(name):
    return r.get_material(name)
