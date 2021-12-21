import random
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
    G_MAJOR = ['G', 'A', 'B', 'C', 'D', 'E', 'F#', 'G']
    D_MAJOR = ['D', 'E', 'F#', 'G', 'A', 'B', 'C#', 'D']
    A_MAJOR = ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#', 'A']
    E_MAJOR = ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#', 'E']
    B_MAJOR = ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#', 'B']
    FIS_MAJOR=['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#', 'F#']
    F_MAJOR = ['F', 'G', 'A', 'B-', 'C', 'D', 'E', 'F']
    BFLAT_MAJOR = ['B-', 'C', 'D', 'E-', 'F', 'G', 'A', 'B-']
    EFLAT_MAJOR = ['E-', 'F', 'G', 'A-', 'B-', 'C', 'D', 'E-']
    AFLAT_MAJOR = ['A-', 'B-', 'C', 'D-', 'E-', 'F', 'G', 'A-']
    DFLAT_MAJOR = ['D-', 'E-', 'F', 'G-', 'A-', 'B-', 'C', 'D-']
    GFLAT_MAJOR = ['G-', 'A-', 'B-', 'C-', 'D-', 'E-', 'F', 'G-']
    A_MINOR = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'A']
    E_MINOR = ['E', 'F#', 'G', 'A', 'B', 'C', 'D', 'E']
    B_MINOR = ['B', 'C#', 'D', 'E', 'F#', 'G', 'A', 'B']
    FIS_MINOR = ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E', 'F#']
    CIS_MINOR = ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B', 'C#']
    GIS_MINOR = ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#', 'G#']
    DIS_MINOR = ['D#', 'E#', 'F#', 'G#', 'A#', 'B', 'C#', 'D#']
    D_MINOR = ['D', 'E', 'F', 'G', 'A', 'B-', 'C', 'D']
    G_MINOR = ['G', 'A', 'B-', 'C', 'D', 'E-', 'F', 'G']
    C_MINOR = ['C', 'D', 'E-', 'F', 'G', 'A-', 'B-', 'C']
    F_MINOR = ['F', 'G', 'A-', 'B-', 'C', 'D-', 'E-', 'F']
    BFLAT_MINOR = ['B-', 'C', 'D-', 'E-', 'F', 'G-', 'A-', 'B-']
    EFLAT_MINOR = ['E-', 'F', 'G-', 'A-', 'B-', 'C-', 'D-', 'E-']


class LENGTHS(Enum):
    FULL = 4.0
    HALF = 2.0
    QUARTER = 1.0
    EIGHTH = 0.5
    SIXTEENTH = 0.25


DURATIONS = [4.0, 2.0, 1.0, 0.5, 0.25, 2.0, 1.0, 0.5, 0.25]


class Chords_Generator():
    def __init__(self):
        pass

    def get_I(self,scale):
        if len(scale)==8:
            return [scale[0],scale[2],scale[4]]
        return scale

    def get_IV(self,scale):
        if len(scale)==8:
            return [scale[3],scale[5],scale[7]]
        return scale

    def get_V(self,scale):
        if len(scale)==8:
            return [scale[4],scale[6],scale[1]]
        return scale


def get_major_pentatonic_scale(scale_name):
    scale_arr = scale_name.value
    pentatonic = [scale_arr[0], scale_arr[1],
                  scale_arr[2], scale_arr[4],
                  scale_arr[5], scale_arr[0]]
    return pentatonic


def get_zelda_scale():
    return [SCALES.C_MAJOR.value[1], SCALES.C_MAJOR.value[3],
            SCALES.C_MAJOR.value[5], SCALES.C_MAJOR.value[7],
            SCALES.C_MAJOR.value[1]]


def get_minor_pentatonic_scale(scale_name):
    scale_arr = scale_name.value
    pentatonic = [scale_arr[0], scale_arr[2],
                  scale_arr[3], scale_arr[4],
                  scale_arr[6], scale_arr[0]]
    return pentatonic


def binary_to_dec(binary):
    return int(binary, 2)

def lower_by_halfstep(note):
    if len(note) ==1 or note.endswith('-'):
        return note+'-'
    elif note.endswith('#'):
        return note[0]

def raise_by_halfstep(note):
    if len(note) == 1 or note.endswith('#'):
        return note + '#'
    elif note.endswith('-'):
        return note[0]



class MusicGenerator():
    def __init__(self):
        self.stream = stream.Stream()
        self.current_octave = DEFAULT_OCTAVE
        self.stream.keySignature = key.KeySignature(0)

    def set_key_signature(self,scale):
        if scale == SCALES.G_MAJOR or scale == SCALES.E_MINOR:
            self.stream.keySignature = key.KeySignature(1)
        elif scale == SCALES.D_MAJOR or scale == SCALES.B_MINOR:
            self.stream.keySignature = key.KeySignature(2)
        elif scale == SCALES.A_MAJOR or scale == SCALES.FIS_MINOR:
            self.stream.keySignature = key.KeySignature(3)
        elif scale == SCALES.E_MAJOR or scale == SCALES.CIS_MINOR:
            self.stream.keySignature = key.KeySignature(4)
        elif scale == SCALES.B_MAJOR or scale == SCALES.GIS_MINOR:
            self.stream.keySignature = key.KeySignature(5)
        elif scale == SCALES.FIS_MAJOR or scale == SCALES.DIS_MINOR:
            self.stream.keySignature = key.KeySignature(6)
        elif scale == SCALES.F_MAJOR or scale == SCALES.D_MINOR:
            self.stream.keySignature = key.KeySignature(-1)
        elif scale == SCALES.BFLAT_MAJOR or scale == SCALES.G_MINOR:
            self.stream.keySignature = key.KeySignature(-2)
        elif scale == SCALES.EFLAT_MAJOR or scale == SCALES.C_MINOR:
            self.stream.keySignature = key.KeySignature(-3)
        elif scale == SCALES.AFLAT_MAJOR or scale == SCALES.F_MINOR:
            self.stream.keySignature = key.KeySignature(-4)
        elif scale == SCALES.DFLAT_MAJOR or scale == SCALES.BFLAT_MINOR:
            self.stream.keySignature = key.KeySignature(-5)
        elif scale == SCALES.GFLAT_MAJOR or scale == SCALES.EFLAT_MINOR:
            self.stream.keySignature = key.KeySignature(-6)
        else:
            return

    def set_time_signature(self):
        self.stream.timeSignature = meter.TimeSignature('4/4')

    def figure_out_note(self,note_name_val,octave):
        written_octave = octave
        if note_name_val == 7:
            written_octave = octave + 1
        name = SCALES.C_MAJOR.value[note_name_val] + str(written_octave)
        return name

    def figure_out_duration(self, note_length_code):
        return DURATIONS[note_length_code]

    def create_note(self,note_name_val, note_length=LENGTHS.QUARTER.value, octave=DEFAULT_OCTAVE):
        note_name = self.figure_out_note(note_name_val,octave)
        created_note = note.Note(note_name)
        created_note.duration.quarterLength = self.figure_out_duration(note_length)
        return created_note

    def get_note_length(index):
        if index<len(DURATIONS):
            return DURATIONS[index]
        return LENGTHS.EIGHTH.value

    def get_note_of_scale(scale,index):
        pass

    def append_to_stream(self,decoded_mask):
        new_note = self.create_note(decoded_mask[0],decoded_mask[1])
        self.stream.append(new_note)

    def finalize(self):
        self.stream.show()

def decode_mask(mask):
    '''mask in form:
     0|0|0
     0|0|0
     0|0|0'''
    note_name_index = binary_to_dec(''.join(mask[0]))
    note_length = binary_to_dec(''.join(mask[1]))
    mystery_val = binary_to_dec(''.join(mask[2]))

    return note_name_index, note_length, mystery_val

def parse_matrix(music_generator,matrix):
    if len(matrix) % 3 != 0 or len(matrix[0]) % 3 != 0:
        print("Matrix dimensions must be multiples of 3")
        return stream.Stream()
    for i in range(0,len(matrix),3):
        for j in range(0,len(matrix[i]),3):
            val =[[str(matrix[i][j]),str(matrix[i][j+1]),str(matrix[i][j+2])],
                  [str(matrix[i+1][j]),str(matrix[i+1][j+1]),str(matrix[i+1][j+2])],
                  [str(matrix[i+2][j]),str(matrix[i+2][j+1]),str(matrix[i+2][j+2])]]
            decoded_mask = decode_mask(val)
            print(decoded_mask)
            music_generator.append_to_stream(decoded_mask)

    return music_generator


def generate_random_matrix():
    x = []
    for j in range(9):
        y = []
        for i in range(9):
            y.append(random.randint(0, 1))
        x.append(y)
    return x

def music_demo():
    note.Note('G##').show()

if __name__ == '__main__':
    # matrix = [[1, 1, 0, 0, 1, 1, 0, 0, 1],
    #           [1, 0, 1, 0, 0, 1, 1, 0, 1],
    #           [0, 1, 1, 0, 1, 1, 0, 0, 1],
    #           [0, 0, 0, 1, 1, 0, 0, 1, 1],
    #           [1, 1, 0, 0, 1, 0, 0, 0, 1],
    #           [1, 0, 0, 0, 1, 0, 0, 0, 1],
    #           [1, 1, 0, 0, 1, 1, 0, 0, 1],
    #           [1, 1, 0, 0, 1, 1, 0, 0, 1],
    #           [1, 1, 0, 0, 1, 1, 0, 0, 1]]
    #
    # matrix2 = [[1, 1, 0, 0, 1, 1, 0, 0, 1],
    #           [1, 0, 1, 0, 0, 1, 1, 0, 1],
    #           [0, 1, 1, 0, 1, 1, 0, 0, 1],
    #           [0, 0, 0, 1, 1, 0, 0, 1, 1],
    #           [1, 1, 0, 0, 1, 0, 0, 0, 1],
    #           [1, 0, 0, 0, 1, 0, 0, 0, 1],
    #           [1, 1, 0, 0, 1, 1, 0, 0, 1],
    #           [1, 1, 0, 0, 1, 1, 0, 0, 1],
    #           [1, 1, 0, 0, 1, 1, 0, 0, 1]]
    #
    # matrices=[generate_random_matrix(),generate_random_matrix(),generate_random_matrix()]
    # music_generator = MusicGenerator()
    # for m in matrices:
    #     parse_matrix(music_generator,m)
    # music_generator.finalize()
    print(raise_by_halfstep('G'))
    print(raise_by_halfstep('G#'))
    print(raise_by_halfstep('G-'))

    print(lower_by_halfstep('G'))
    print(lower_by_halfstep('G#'))
    print(lower_by_halfstep('G-'))




