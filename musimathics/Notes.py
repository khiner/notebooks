import numpy as np
import IPython

from constants import SAMPLES_PER_SECOND
from Note import Note

Audio = IPython.display.Audio

class NoteSequence:
    def __init__(self, notes):
        self.notes = [note if isinstance(note, Note) else Note(*note) for note in notes]
        if notes and len(notes) > 0:
            zeros_mono = np.zeros(np.sum([note.duration_samples for note in self.notes]) + self.notes[-1].adsr.release_samples)
            self.samples = np.vstack([zeros_mono, zeros_mono])
            self.mix()

    def mix(self):
        sample_index = 0
        for note in self.notes:
            sample_range = sample_index, (sample_index + note.duration_samples + note.adsr.release_samples)
            samples_mono = note.get_samples()
            self.samples[0][sample_range[0]:sample_range[1]] += samples_mono * (1 - note.pan)
            self.samples[1][sample_range[0]:sample_range[1]] += samples_mono * note.pan
            sample_index += note.duration_samples # release tails can overlap

    def num_samples(self):
        return self.samples.shape[1]

def is_note_like(item):
    return isinstance(item, Note) or isinstance(item, tuple)

def is_list_like(item):
    return isinstance(item, list) or isinstance(item, np.ndarray)

# `notes` can be any of:
#  - a note-like object (a `Note` or tuple representing note arguments)
#    - In this case, a single note is rendered.
#  - an list-like container of note-like objects
#    - In this case, a sequence of notes is rendered monophonically (with release tails overlapping).
#  - a list-like container of list-like containers of note-like objects (including `NoteSequence`s),
#    (in this case, each list is mixed polyphonically)
#    - In this case, each sequence of notes is rendered as above and mixed polyphonically.
def render_notes(notes):
    if is_note_like(notes):
        notes = [[notes]]
    elif is_list_like(notes):
        if is_note_like(notes[0]):
            notes = [notes]
        elif not (isinstance(notes[0], NoteSequence) or is_list_like(notes[0])):
            raise ValueError('Invalid argument given to `render_notes`.')

    note_sequences = [inner_notes if isinstance(inner_notes, NoteSequence) else NoteSequence(inner_notes) for inner_notes in notes]
    zeros_mono = np.zeros(max([note_sequence.num_samples() for note_sequence in note_sequences]))
    mixed = np.vstack([zeros_mono, zeros_mono])
    for notes in note_sequences:
        mixed += np.pad(notes.samples, (0, mixed.shape[1] - notes.num_samples()), 'constant', constant_values=0)
    if mixed.max() > 1:
        mixed /= mixed.max()
    return mixed

def render_notes_ipython(notes):
    return Audio(render_notes(notes), rate=SAMPLES_PER_SECOND)
