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

DEFAULT_OCTAVE = 4


class SCALES(Enum):
    C_MAJOR = ['C', 'D', 'E', 'F', 'G', 'A', 'B']


class GeneratedNote:
    def __init__(self, note_name, octave=DEFAULT_OCTAVE, accidental=''):
        self.note = note_name
        self.octave = octave
        self.accidental = accidental

    def get_note(self):
        return note.Note(self.note + self.accidental + str(self.octave))

    def set_accidental(self, accidental):
        self.accidental = accidental

    def set_octave(self, octave):
        self.octave = octave


def get_major_pentatonic_scale(scale_name):
    scale_arr = scale_name.value
    pentatonic = [scale_arr[0], scale_arr[1], scale_arr[2], scale_arr[4], scale_arr[5]]
    return pentatonic


def get_minor_pentatonic_scale(scale_name):
    scale_arr = scale_name.value
    pentatonic = [scale_arr[0], scale_arr[2], scale_arr[3], scale_arr[4], scale_arr[6]]
    return pentatonic


def music21demo():
    f = GeneratedNote('G').get_note()
    f.show('midi')
    # f.show()


if __name__ == '__main__':
    music21demo()
