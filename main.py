from enum import Enum

import music21
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools
from IPython.display import HTML
from music21 import *

us = music21.environment.UserSettings()
us['musicxmlPath'] = "C:\\Program Files\\MuseScore 3\\bin\\MuseScore3.exe"
us['musescoreDirectPNGPath'] = "C:\\Program Files\\MuseScore 3\\bin\\MuseScore3.exe"


class SCALES(Enum):
    C_MAJOR = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']


def get_major_pentatonic_scale(scale):
    scale_arr = scale.value
    pentatonic = [scale_arr[0], scale_arr[1], scale_arr[2], scale_arr[4], scale_arr[5]]
    return pentatonic


def music21demo():
    f = note.Note('F5')
    f.show('midi')
    # f.show()


if __name__ == '__main__':
    print(get_major_pentatonic_scale(SCALES.C_MAJOR))
