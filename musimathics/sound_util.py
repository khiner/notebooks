import numpy as np
import IPython
Audio = IPython.display.Audio

MAX_NOTE_DURATION_SECONDS = 20
SAMPLE_RATE = 44_100
# share this 0:MAX_N range
TIME_RANGE = np.linspace(0, MAX_NOTE_DURATION_SECONDS, SAMPLE_RATE * MAX_NOTE_DURATION_SECONDS)

class Note:
    # freq of 0 is interpreted as rest
    def __init__(self, frequency=880, duration_seconds=0.5, attack_seconds=0.1, decay_seconds=0.1, sustain_level=0.7, release_seconds=0.2):
        self.frequency = frequency
        self.duration_samples = int(duration_seconds * SAMPLE_RATE)
        if attack_seconds + decay_seconds >= duration_seconds:
            remainder = attack_seconds + decay_seconds - duration_seconds
            attack_seconds -= remainder / 2
            decay_seconds -= remainder / 2
        self.set_adsr(attack_seconds, decay_seconds, sustain_level, release_seconds)

    # uses simple linear ramps
    def set_adsr(self, attack_seconds, decay_seconds, sustain_level, release_seconds):
        self.attack_samples = int(attack_seconds * SAMPLE_RATE)
        self.decay_samples = int(decay_seconds * SAMPLE_RATE)
        self.sustain_level = sustain_level
        self.release_samples = int(release_seconds * SAMPLE_RATE)
        self.dirty = True

    def get_data(self):
        if self.dirty or self.data == None:
            if self.frequency == 0:
                self.data = np.zeros(self.duration_samples + self.release_samples)
            else:
                self.data = np.sin(2*np.pi*self.frequency*TIME_RANGE[:(self.duration_samples + self.release_samples)])
                self.data[:self.attack_samples] *= np.linspace(0, 1, self.attack_samples)
                self.data[self.attack_samples:(self.attack_samples + self.decay_samples)] *= np.linspace(1, self.sustain_level, self.decay_samples)
                self.data[(self.attack_samples + self.decay_samples):self.duration_samples] *= self.sustain_level
                self.data[self.duration_samples:] *= np.linspace(self.sustain_level, 0, self.release_samples)
        return self.data

# responsible for mixing notes
class Notes:
    def __init__(self, notes):
        self.notes = [note if isinstance(note, Note) else Note(*note) for note in notes]
        if notes and len(notes) > 0:
            self.data = np.zeros(np.sum([note.duration_samples for note in self.notes]) + self.notes[-1].release_samples)
            self.mix()


    def mix(self):
        data_index = 0
        for note in self.notes:
            self.data[data_index:(data_index + note.duration_samples + note.release_samples)] += note.get_data()
            data_index += note.duration_samples # release tails can overlap

def render_notes(notes):
    return Audio((notes if isinstance(notes, Notes) else Notes(notes)).data, rate=SAMPLE_RATE)

def render_overlapping_notes(notess):
    notess = [notes if isinstance(notes, Notes) else Notes(notes) for notes in notess]
    mixed = np.ndarray(max([notes.data.size for notes in notess]))

    for notes in notess:
        mixed += np.pad(notes.data, (0, mixed.size - notes.data.size), 'constant', constant_values=0)
    return Audio(mixed, rate=SAMPLE_RATE)
