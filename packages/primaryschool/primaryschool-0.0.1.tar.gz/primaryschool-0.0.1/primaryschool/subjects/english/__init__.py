

import os
import sys

from primaryschool.locale import _
from primaryschool.subjects import *

name = _("English")


class EnglishGame(SubjectGame):
    pass


def start(win):
    EnglishGame(win)
    pass
