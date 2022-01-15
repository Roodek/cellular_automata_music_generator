import os
from enum import Enum

import music21
from music21 import *

from MatrixGenerator import MatrixGenerator

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
    FIS_MAJOR = ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#', 'F#']
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


DURATIONS = [4.0, 2.0, 1.0, 0.5, 0.25, 2.0, 1.0, 0.5, 1.0]


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


class Chords_Generator():
    def __init__(self):
        pass

    def get_I(self, scale):
        if len(scale) == 8:
            return [scale[0], scale[2], scale[4]]
        return scale

    def get_II(self, scale):
        if len(scale) == 8:
            return [scale[1], scale[3], scale[5]]
        return scale

    def get_III(self, scale):
        if len(scale) == 8:
            return [scale[2], scale[4], scale[6]]
        return scale

    def get_IV(self, scale):
        if len(scale) == 8:
            return [scale[3], scale[5], scale[7]]
        return scale

    def get_V(self, scale):
        if len(scale) == 8:
            return [scale[4], scale[6], scale[1]]
        return scale

    def get_VI(self, scale):
        if len(scale) == 8:
            return [scale[5], scale[7], scale[2]]
        return scale

    def get_VII(self, scale):
        if len(scale) == 8:
            return [scale[6], scale[1], scale[3]]
        return scale


def binary_to_dec(binary):
    return int(binary, 2)


def lower_by_halfstep(note):
    if len(note) == 1 or note.endswith('-'):
        return note + '-'
    elif note.endswith('#'):
        return note[0]


def raise_by_halfstep(note):
    if len(note) == 1 or note.endswith('#'):
        return note + '#'
    elif note.endswith('-'):
        return note[0]


class MusicGenerator:

    def __init__(self, scale, octave, is_pentatonic, pentatonic, is_zelda):
        self.stream = stream.Stream()
        self.part1 = stream.Part(id='part1')
        self.part2 = stream.Part(id='part2')

        self.current_octave = octave
        self.stream.keySignature = key.KeySignature(0)
        self.scale = scale
        self.scale_notes = scale.value
        self.prev_note = None
        self.sixteen_counter = 0
        self.current_chord = None
        self.is_pentatonic = is_pentatonic
        self.pentatonic = pentatonic
        self.is_zelda = is_zelda

    def set_key_signature(self, scale):
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

    def figure_out_note(self, note_name_val):
        if note_name_val >= len(self.scale_notes) - 1:
            self.current_octave = self.current_octave + 1
        elif note_name_val == 0:
            self.current_octave = self.current_octave - 1

        if self.is_zelda:
            temp = get_zelda_scale(self.scale)
            name = temp[note_name_val % 5] + str(self.current_octave)
        elif self.is_pentatonic:
            if self.pentatonic == 'major':
                temp_pentatonic = get_major_pentatonic_scale(self.scale)
            else:
                temp_pentatonic = get_minor_pentatonic_scale(self.scale)
            name = temp_pentatonic[note_name_val % 5] + str(self.current_octave)
        else:
            name = self.scale_notes[note_name_val] + str(self.current_octave)
        print(name)

        if self.current_octave <= 3:
            self.current_octave = self.current_octave + 1

        if self.current_octave >= 6:
            self.current_octave = self.current_octave-1

        return name

    def figure_out_duration(self, note_length_code):
        if self.prev_note is not None and self.prev_note.duration.quarterLength == 0.25 and self.sixteen_counter<3:
            self.sixteen_counter += 1
            return 0.25
        else:
            self.sixteen_counter = 0
        return DURATIONS[note_length_code]

    def figure_out_chord(self, chord_code, note):
        note_height = self.scale_notes.index(note.name)
        chord_notes = []
        if note_height == 0:
            chord_notes = Chords_Generator().get_I(self.scale_notes)
        elif note_height == 1:
            chord_notes = Chords_Generator().get_II(self.scale_notes)
        elif note_height == 2:
            chord_notes = Chords_Generator().get_III(self.scale_notes)
        elif note_height == 3:
            chord_notes = Chords_Generator().get_IV(self.scale_notes)
        elif note_height == 4:
            chord_notes = Chords_Generator().get_V(self.scale_notes)
        elif note_height == 5:
            chord_notes = Chords_Generator().get_VI(self.scale_notes)
        elif note_height == 6:
            chord_notes = Chords_Generator().get_VII(self.scale_notes)
        elif note_height == 7:
            chord_notes = Chords_Generator().get_I(self.scale_notes)

        new_chord = chord.Chord(chord_notes)
        # if chord_code == 0:
        #     pass

        return new_chord

    def create_note(self, note_name_val, note_length=LENGTHS.QUARTER.value):
        note_name = self.figure_out_note(note_name_val)
        created_note = note.Note(note_name)
        created_note.duration.quarterLength = self.figure_out_duration(note_length)
        return created_note

    def get_note_of_scale(self, index):
        return self.scale[index]

    def append_to_stream(self, decoded_mask):
        new_note = self.create_note(decoded_mask[0], decoded_mask[1])
        if self.current_chord is None or not self.notes_from_same_chord(self.prev_note, new_note):
            new_chord = self.figure_out_chord(decoded_mask[2], new_note)
        else:
            if self.current_chord:
                new_chord = self.current_chord
            else:
                new_chord = self.figure_out_chord(decoded_mask[2], new_note)

        new_chord.quarterLength = new_note.duration.quarterLength
        self.part1.append(new_note)
        self.part2.append(new_chord)
        self.prev_note = new_note
        self.current_chord = new_chord

    def notes_from_same_chord(self, prev_note, new_note):
        if self.current_chord:
            if prev_note in self.current_chord and new_note in self.current_chord:
                return True
            else:
                return False
        return False

    def finalize(self):
        self.stream.insert(0, self.part1)
        self.stream.insert(0, self.part2)

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


def parse_matrix(music_generator, matrix):
    if len(matrix) % 3 != 0 or len(matrix[0]) % 3 != 0:
        print("Matrix dimensions must be multiples of 3")
        return stream.Stream()
    for i in range(0, len(matrix), 3):
        for j in range(0, len(matrix[i]), 3):
            val = [[str(matrix[i][j]), str(matrix[i][j + 1]), str(matrix[i][j + 2])],
                   [str(matrix[i + 1][j]), str(matrix[i + 1][j + 1]), str(matrix[i + 1][j + 2])],
                   [str(matrix[i + 2][j]), str(matrix[i + 2][j + 1]), str(matrix[i + 2][j + 2])]]
            decoded_mask = decode_mask(val)
            # print(decoded_mask)
            music_generator.append_to_stream(decoded_mask)

    return music_generator


if __name__ == '__main__':

    scale = os.getenv('scale')

    if scale is None:
        scale = 'C_MAJOR'

    scale = SCALES[scale]

    octave = os.getenv('octave')

    if octave is None:
        octave = 4

    is_pentatonic = os.getenv('is_pentatonic')

    if is_pentatonic is None:
        is_pentatonic = True

    pentatonic = os.getenv('pentatonic')

    if pentatonic is None:
        pentatonic = 'major'

    is_zelda = os.getenv('is_zelda')

    if is_zelda is None:
        is_zelda = False

    matrix_generator = MatrixGenerator((9, 9), 15, 0.5)

    matrices = matrix_generator.generate_GoF_matrices("2345/4")

    music_generator = MusicGenerator(scale,
                                     int(octave),
                                     bool(is_pentatonic),
                                     pentatonic,
                                     bool(is_zelda))

    for m in matrices:
        parse_matrix(music_generator, m)
    music_generator.finalize()
