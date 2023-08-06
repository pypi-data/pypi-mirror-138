
import os
import sys

from primaryschool.locale import _
from primaryschool.subjects import *

name_t = _('Math')


class MathGame(SubjectGame):
    pass


def start(win):
    MathGame(win)
    pass
