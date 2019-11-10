import math
import numpy as np

SEMITONES_IN_OCTAVE = 12
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def semitones_above_reference_frequency(reference_frequency, num_semitones):
    return reference_frequency * 2 ** (num_semitones / SEMITONES_IN_OCTAVE)

def note_label_for_pitch_number(pitch_number):
    octave = pitch_number // SEMITONES_IN_OCTAVE
    note_degree = pitch_number % SEMITONES_IN_OCTAVE
    return NOTE_NAMES[note_degree] + str(octave)

def note_label_for_frequency(frequency):
    pitch_number = round(SEMITONES_IN_OCTAVE * math.log2(frequency / C0))
    return note_label_for_pitch_number(pitch_number)

A4 = 440
C0 = semitones_above_reference_frequency(A4, -9 - 4 * SEMITONES_IN_OCTAVE)

FREQUENCY_FOR_PITCH_NUMBER = { pitch_number: semitones_above_reference_frequency(C0, pitch_number) for pitch_number in range(128) }
PITCH_NUMBER_FOR_NOTE_LABEL = { note_label_for_pitch_number(pitch_number): pitch_number for pitch_number in range(128) }
NOTE_LABEL_FOR_PITCH_NUMBER = { pitch_number: note_label_for_pitch_number(pitch_number) for pitch_number in range(128) }
FREQUENCY_FOR_NOTE_LABEL = { note_label_for_frequency(frequency): frequency for frequency in [semitones_above_reference_frequency(C0, pitch_number) for pitch_number in range(128)] }
# alias all '{NOTE}' to '{NOTE}0', e.g. 'C' => 'C0'
for note_name in NOTE_NAMES:
    PITCH_NUMBER_FOR_NOTE_LABEL[note_name] = PITCH_NUMBER_FOR_NOTE_LABEL[note_name + '0']
    FREQUENCY_FOR_NOTE_LABEL[note_name] = FREQUENCY_FOR_NOTE_LABEL[note_name + '0']

def note_labels_for_pitch_numbers(pitch_numbers):
    return [NOTE_LABEL_FOR_PITCH_NUMBER[pitch_number] for pitch_number in pitch_numbers]

def pitch_numbers_for_note_labels(note_labels):
    return np.array([PITCH_NUMBER_FOR_NOTE_LABEL[note_label] for note_label in note_labels])

def frequency_for_note_label(note_label):
    return FREQUENCY_FOR_NOTE_LABEL[note_label]

def frequencies_for_note_labels(note_labels):
    return [frequency_for_note_label(note_label) for note_label in note_labels]
