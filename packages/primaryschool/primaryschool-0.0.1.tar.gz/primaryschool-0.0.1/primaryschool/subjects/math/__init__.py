
import os
import sys

from primaryschool.locale import _
from primaryschool.subjects import *

name = _('Math')


class MathGame(SubjectGame):
    pass


def start(win):
    MathGame(win)
    pass
