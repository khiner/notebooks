import math

SEMITONES_IN_OCTAVE = 12

def semitones_above_reference_frequency(reference_frequency, num_semitones):
    return reference_frequency * 2 ** (num_semitones / SEMITONES_IN_OCTAVE)


def note_label_for_frequency(frequency):
    num_half_steps = round(SEMITONES_IN_OCTAVE * math.log2(frequency / C0))
    octave = num_half_steps // SEMITONES_IN_OCTAVE
    note_degree = num_half_steps % SEMITONES_IN_OCTAVE
    return note_names[note_degree] + str(octave)

A4 = 440
C0 = semitones_above_reference_frequency(A4, -9 - 4 * SEMITONES_IN_OCTAVE)

note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

FREQUENCY_FOR_NOTE_LABEL = { note_label_for_frequency(frequency): frequency for frequency in [semitones_above_reference_frequency(C0, semitones) for semitones in range(128)] }
