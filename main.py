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
    C_MAJOR = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']


class LENGTHS(Enum):
    FULL = 4.0
    HALF = 2.0
    QUARTER = 1.0
    EIGHTH = 0.5
    SIXTEENTH = 0.25


DURATIONS = [4.0, 2.0, 1.0, 0.5, 0.25, 2.0, 1.0, 0.5, 0.25]


def get_major_pentatonic_scale(scale_name):
    scale_arr = scale_name.value
    pentatonic = [scale_arr[0] + str(DEFAULT_OCTAVE), scale_arr[1] + str(DEFAULT_OCTAVE),
                  scale_arr[2] + str(DEFAULT_OCTAVE),
                  scale_arr[4] + str(DEFAULT_OCTAVE), scale_arr[5] + str(DEFAULT_OCTAVE),
                  scale_arr[0] + str(DEFAULT_OCTAVE + 1)]
    return pentatonic


def get_zelda_scale():
    return [SCALES.C_MAJOR.value[1] + str(DEFAULT_OCTAVE), SCALES.C_MAJOR.value[3] + str(DEFAULT_OCTAVE),
            SCALES.C_MAJOR.value[5] + str(DEFAULT_OCTAVE), SCALES.C_MAJOR.value[7] + str(DEFAULT_OCTAVE),
            SCALES.C_MAJOR.value[1] + str(DEFAULT_OCTAVE + 1)]


def get_minor_pentatonic_scale(scale_name):
    scale_arr = scale_name.value
    pentatonic = [scale_arr[0] + str(DEFAULT_OCTAVE), scale_arr[2] + str(DEFAULT_OCTAVE),
                  scale_arr[3] + str(DEFAULT_OCTAVE), scale_arr[4] + str(DEFAULT_OCTAVE),
                  scale_arr[6] + str(DEFAULT_OCTAVE), scale_arr[0] + str(DEFAULT_OCTAVE + 1)]
    return pentatonic


def binary_to_dec(binary):
    return int(binary, 2)


def create_note(note_name, note_length=LENGTHS.QUARTER.value, accidental='', octave=DEFAULT_OCTAVE):
    created_note = note.Note(note_name + accidental + str(octave))
    created_note.duration.quarterLength = note_length
    return created_note


def decode_mask(mask):
    '''mask in form:
     0|0|0
     0|0|0
     0|0|0'''
    note_name_index = binary_to_dec(''.join(mask[0]))
    note_length = DURATIONS[binary_to_dec(''.join(mask[1]))]
    mystery_val = binary_to_dec(''.join(mask[2]))

    return note_name_index, note_length, mystery_val


def music21demo():
    f = create_note('G')
    # f.show('midi')
    f.show()


if __name__ == '__main__':
    # music21demo()
    # print(binary_to_dec('111'))
    matrix = [[1, 1, 0, 0, 1, 1, 0, 0, 1],
              [1, 0, 1, 0, 0, 1, 1, 0, 1],
              [0, 1, 1, 0, 1, 1, 0, 0, 1],
              [0, 0, 0, 1, 1, 0, 0, 1, 1],
              [1, 1, 0, 0, 1, 0, 0, 0, 1],
              [1, 0, 0, 0, 1, 0, 0, 0, 1],
              [1, 1, 0, 0, 1, 1, 0, 0, 1],
              [1, 1, 0, 0, 1, 1, 0, 0, 1],
              [1, 1, 0, 0, 1, 1, 0, 0, 1]]
    stream1=stream.Stream()
    for i in range(0,len(matrix),3):
        print('next decoded row:')
        for j in range(0,len(matrix[i]),3):
            val =[[str(matrix[i][j]),str(matrix[i][j+1]),str(matrix[i][j+2])],
                  [str(matrix[i+1][j]),str(matrix[i+1][j+1]),str(matrix[i+1][j+2])],
                  [str(matrix[i+2][j]),str(matrix[i+2][j+1]),str(matrix[i+2][j+2])]]
            decoded_mask=decode_mask(val)
            print("next note")
            print(decoded_mask)
            stream1.append(create_note(SCALES.C_MAJOR.value[decoded_mask[0]],decoded_mask[1]))

    stream1.show()

